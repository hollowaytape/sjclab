from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, render_to_response
from inventory.models import Experiment, Material, Text, Room, Tag, Image, Resource, Link
from inventory.forms import ExperimentForm, MaterialForm, UserForm, UserProfileForm, TextForm, ResourceForm, ImageForm, LinkForm
from django.forms.models import modelformset_factory
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext as _
import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django_wysiwyg import clean_html


def url_safe(string):
    """ Replaces spaces with underscores, making a string safer for urls."""
    return string.replace(' ', '_').replace(".", "")


def eye_safe(string):
    """ Undoes the operation of url_safe()."""
    return string.replace('_', ' ')

def experiment_index(request):
    context_dict = {
        'fr_experiments': Experiment.objects.filter(text__year="Freshman").order_by('title'),
        'jr_experiments': Experiment.objects.filter(text__year="Junior").order_by('title'),
        'sr_experiments': Experiment.objects.filter(text__year="Senior").order_by('title'),
        'ot_experiments': Experiment.objects.filter(text__year="Other").order_by('title')
    }
    
    # Sanitize experiment names for use in urls.
    for experiment_list in context_dict.itervalues():
        for experiment in experiment_list:
            experiment.url = url_safe(experiment.title)

    # Grab a list of all valid tags and sanitize their names for urls.
    tags = Tag.objects.order_by('name').exclude(name="none").exclude(name="")
    for t in tags:
        t.url = url_safe(t.name)
    context_dict['tags'] = tags

    # Render the response and send it back.
    return render(request, 'inventory/experiment_index.html', context_dict)
  
def experiment(request, experiment_name_url):
    # Change underscores in the experiment name to spaces.
    experiment_name = eye_safe(experiment_name_url)
    
    experiment = get_object_or_404(Experiment, title=experiment_name)
    
    # materials: each unique kind of material necessary for the experiment.
    materials = experiment.materials.all()
    
    tags = experiment.tags.all().exclude(name="")
    
    # material_locations: dict with entries {material: [instance1, instance2...]}.
    material_locations = {}
    
    for m in materials:
        material_locations[m] = Material.objects.filter(name=m)
    
    for t in tags:
        t.url = url_safe(t.name)

    context_dict = {
        'experiment':         experiment,
        'materials':          materials,
        'material_locations': material_locations,
        'tags':               tags,
        'procedure':          clean_html(experiment.procedure),
        'images':             Image.objects.filter(experiment=experiment),
        'resources':          Resource.objects.filter(experiment=experiment),
        'links':              Link.objects.filter(experiment=experiment)
    }

    # Go render the response and return it to the client.
    return render(request, 'inventory/experiment.html', context_dict)
   
def tag(request, tag_name_url):
    # Change underscores in the experiment name to spaces.
    tag_name = eye_safe(tag_name_url)
    tag = get_object_or_404(Tag, name = tag_name)

    context_dict = {
        'tag_name':    tag_name,
        'tag':         tag,
        'experiments': Experiment.objects.filter(tags__name=tag.name).order_by('title')
    }

    # Now sanitize experiment names for use in links.
    for e in context_dict['experiments']:
        e.url = url_safe(e.title)
    
    return render(request, 'inventory/tag.html', context_dict)
 
def room_index(request):
    context_dict = {
        'first_bio': Room.objects.filter(hall="Biology").order_by('number'),
        'first_phys': Room.objects.filter(hall="Physics").order_by('number'),
        'second': Room.objects.filter(floor="Second Floor").order_by('number'),
        'ground': Room.objects.filter(floor="Ground Floor").order_by('number')
    }
    
    for hall in context_dict.itervalues():
        for room in hall:
            room.url = url_safe(room.number)
    
    return render(request, 'inventory/room_index.html', context_dict)

def room(request, room_url):
    room_number = eye_safe(room_url)
    room = get_object_or_404(Room, number=room_number)
    room.url = url_safe(room_number)
    
    # Retrieve all of the materials in the room.
    materials = Material.objects.filter(room=room).order_by('location')

    context_dict = {
        'room_number': room_number,
        'room':        room,
        'materials':   materials
    }
    
    return render(request, 'inventory/room.html', context_dict)
 
def rooms_all(request):
    # Get each type of Material and add it to the dict.
    # By using values_list w/"flat" param, we get a list instead of an unhashable dict.
    material_types = Material.objects.values_list('name', flat=True).distinct()

    material_locations = {}
    for m in material_types:
        locations = Material.objects.filter(name=m).order_by('name')
        material_locations[m] = locations
    
    context_dict = {'material_locations': material_locations}

    # Render the response and send it back!
    return render(request, 'inventory/rooms_all.html', context_dict)

def experiment_edit(request, id=None):
    ResourceFormSet = modelformset_factory(Resource, form = ResourceForm)
    ImageFormSet = modelformset_factory(Image, form = ImageForm)
    LinkFormSet = modelformset_factory(Link, form=LinkForm)
    
    if id:
        # Edit experiment form.
        experiment = get_object_or_404(Experiment, pk=id)
        experiment.url = url_safe(experiment.title)

        # Create querysets of the experiment's associated resources/links/images,
        # then populate a modelformset with them.
        resource_qset = Resource.objects.filter(experiment = experiment)
        resource_formset = ResourceFormSet(queryset = resource_qset, prefix='resources')
        
        image_qset = Image.objects.filter(experiment=experiment)
        image_formset = ImageFormSet(queryset=image_qset, prefix='images')
        
        link_qset = Link.objects.filter(experiment=experiment)
        link_formset = LinkFormSet(queryset=link_qset, prefix='links')
        
    else:
        # New experiment form.
        experiment = Experiment()

        # Create empty formsets this time.
        resource_formset = ResourceFormSet(queryset=Resource.objects.none(), prefix='resources')
        image_formset = ImageFormSet(queryset=Image.objects.none(), prefix='images')
        link_formset = LinkFormSet(queryset=Link.objects.none(), prefix='links')
 
    if request.POST:
        # Sort out the experiment and the different formsets just POSTed.
        form = ExperimentForm(request.POST, request.FILES, instance=experiment)
        resource_formset = ResourceFormSet(request.POST, request.FILES, prefix='resources')
        image_formset = ImageFormSet(request.POST, request.FILES, prefix='images')
        link_formset = LinkFormSet(request.POST, prefix='links')
        
        if form.is_valid() and resource_formset.is_valid() and image_formset.is_valid():
            # Fetch the main_photo file.
            if 'main_photo' in request.FILES:
                form.main_photo = request.FILES['main_photo']
            form.save()

            # Associate all the formset data with the experiment.
            # (Not sure if still necessary, but it once kept me from having to fish unassociated resources out of the db.)
            resource_fset = resource_formset.save(commit=False)
            for r in resource_fset:
                r.experiment = experiment
                r.save()
                
            image_fset = image_formset.save(commit=False)
            for i in image_fset:
                i.experiment = experiment
                i.save()
                
            link_fset = link_formset.save(commit=False)
            for l in link_fset:
                l.experiment = experiment
                l.save()
                
            messages.add_message(request, messages.SUCCESS, _('Experiment successfully updated.'))
            redirect_url = reverse('experiment', args=[url_safe(experiment.title)])
            return HttpResponseRedirect(redirect_url)
        else:
            messages.add_message(request, messages.ERROR,
                                 _('There was a problem saving the experiment. See errors below and please try again.'))
 
    else:
        # If not POSTing, just show the form.
        form = ExperimentForm(instance=experiment)

    context_dict = {
        'experiment': experiment,
        'form':       form,
        'resource_formset': resource_formset,
        'image_formset':    image_formset,
        'link_formset':     link_formset
    }
 
    return render(request, 'inventory/experiment_edit.html', context_dict)

def experiment_delete(request, id):
    Experiment.objects.get(pk=id).delete()
    messages.add_message(request, messages.SUCCESS, _('Experiment deleted.'))

    return HttpResponseRedirect('/experiments/')

def text_add(request):
    text = Text()
    
    if request.POST:
        form = TextForm(request.POST, instance=text)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _('Text successfully added.'))
            redirect_url = reverse('experiment_index')
            return HttpResponseRedirect(redirect_url)
        else:
            messages.add_message(request, messages.ERROR, _('There was a problem saving the text. Please try again.'))
            
    else:
        form = TextForm(instance=text)

    context_dict = {
        'form': form,
        'text': text
    }

    return render(request, 'inventory/text_add.html', context_dict)
    
def room_edit(request, room_url):
    number = eye_safe(room_url)
    room = Room.objects.get(number = number)

    MaterialFormSet = modelformset_factory(Material, form = MaterialForm)
    qset = Material.objects.filter(room = room)
    formset = MaterialFormSet(queryset = qset)
    
    if request.POST:
        formset = MaterialFormSet(request.POST, queryset = qset)
        if formset.is_valid():
            # Before saving, update the date_modified.
            fset = formset.save(commit=False)
            room.date_modified = datetime.datetime.now()
            room.save()

            # Make sure the materials are associated with the right room.
            for material in fset:
                material.room = room
                material.save()

            # Notify the user and redirect to the updated room page.
            messages.add_message(request, messages.SUCCESS, _('Room successfully updated.'))
            redirect_url = reverse('room', args=[room.number])
            return HttpResponseRedirect(redirect_url)

        else:
            # Errors occurred.
            messages.add_message(request, messages.ERROR,
                                 _('There was a problem saving the experiment. Please try again.'))

    context_dict = {
        'formset': formset,
        'room':    room
    }

    return render(request, 'inventory/room_edit.html', context_dict)
    

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.is_active = False
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            registered = True

            messages.add_message(request, messages.SUCCESS,
                                 _('Registration successful. The administrator has been notified, and will review your account.'))
            send_mail('Pending user registration', 'A user has registered with the name %s and email %s. Please check the registration page.' % 
                (user.username, user.email), 'accounts@sjclab.herokuapp.com', ['max.silbiger@gmail.com',], fail_silently=False)

        else:
            messages.add_message(request, messages.ERROR, _('There was a problem registering. Please try again.'))
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {
        'user_form':    user_form,
        'profile_form': profile_form,
        'registered':   registered
    }

    return render(request, 'registration/registration_form.html', context_dict)
            
def user_login(request):
    next = ""
    username = ""

    # The page the user came from is stored in the 'next' variable. If it's there, retrieve it.
    if 'next' in request.GET:
        next = request.GET['next']

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            # User has logged into a real account.

            if user.is_active:
                # User has logged into a real, active account.
                login(request, user)
                messages.add_message(request, messages.SUCCESS, _('Welcome, %s!' % username))
                if next == "":
                    return HttpResponseRedirect('/experiments/')
                else:
                    request.user = user
                    return HttpResponseRedirect(request.POST.get('next'))
            else:
                # Account is not activated yet.
                messages.add_message(request, messages.ERROR,
                                     _('Your account is not active yet. Please wait for the administrator to approve your registration.'))
                return render(request, 'registration/login.html', {})
        else:
            # Invalid login.
            messages.add_message(request, messages.ERROR, _('Invalid login details supplied, please try again.'))
            return render(request, 'registration/login.html', {})

    else:
        # Not a POST, so just display the form.
        context_dict = {
            'username': username,
            'next':     next
        }

        #return render_to_response('registration/login.html', context_dict, context_instance=RequestContext(request))
        return render(request, 'registration/login.html', context_dict)

def user_logout(request):
    next = request.GET.get('next')
    logout(request)

    # Take the user back to the homepage.
    messages.add_message(request, messages.SUCCESS, _('You have logged out.'))

    if 'next' in request.GET:
        next = request.GET['next']

    if next == "":
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect(next)
    
def admin_user_approval(request):
     users = User.objects.filter(is_active=False)
     
     return render_to_response('inventory/user_approval.html', {'users': users},
                               context_instance=RequestContext(request))
     
def approve_user(request, id):
    user = User.objects.get(id=id)
    
    if user.is_active == False:
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, _('User %s successfully activated.' % user.username))
        send_mail('Your account has been activated',
                  '%s, the administrator has activated your account. You may now login.' % user.username,
                  'accounts@sjclab.herokuapp.com', [user.email], fail_silently=False)

    else:
        messages.add_message(request, messages.ERROR, _('User %s is already active.' % user.username))

    return HttpResponseRedirect('/approval/')