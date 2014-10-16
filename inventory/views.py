from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from inventory.models import Experiment, Material, Text, Room, Tag, Image, Resource, Link
from inventory.forms import ExperimentForm, RoomForm, MaterialForm, UserForm, UserProfileForm, TextForm, ResourceForm, ImageForm, LinkForm
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory
import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User, Permission

def url_safe(string):
    """ Replaces spaces with underscores, making a string safer for urls."""
    return string.replace(' ', '_').replace(".", "")

def eye_safe(string):
    """ Undoes the operation of url_safe()."""
    return string.replace('_', ' ')

def experiment_index(request):
    context_dict = {}
    
    # Grab a list of all appropriate experiments to each year.
    context_dict['fr_experiments'] = Experiment.objects.filter(text__year="Freshman").order_by('title')
    context_dict['jr_experiments'] = Experiment.objects.filter(text__year="Junior").order_by('title')
    context_dict['sr_experiments'] = Experiment.objects.filter(text__year="Senior").order_by('title')
    context_dict['ot_experiments'] = Experiment.objects.filter(text__year="Other").order_by('title')
    
    # Sanitize experiment names for use in urls.
    for year in (context_dict['fr_experiments'], context_dict['jr_experiments'], context_dict['sr_experiments'], context_dict['ot_experiments']):
        for experiment in year:
            experiment.url = url_safe(experiment.title)

    # Grab a list of all tags and sanitize their names for urls.
    tags = Tag.objects.order_by('name').exclude(name="none")
    for t in tags:
        t.url = url_safe(t.name)
    context_dict['tags'] = tags
        
    none_tag = Tag.objects.get(name="none")
    none_tag.url = "none"
    context_dict['none_tag'] = none_tag
    
    # Render the response and send it back.
    return render(request, 'inventory/experiment_index.html', context_dict)

    
def experiment(request, experiment_name_url):
    # Change underscores in the experiment name to spaces.
    experiment_name = eye_safe(experiment_name_url)
    
    # Context dictionary to pass to the template.
    # Contain the name of the experiment passed by the user.
    context_dict = {'experiment_name': experiment_name}
    
    experiment = get_object_or_404(Experiment, title=experiment_name)
    
    # materials: each kind of material necessary for the experiment.
    materials = experiment.materials.all()
    
    tags = experiment.tags.all()
    
    # material_locations: dict with entries {material: [instance1, instance2]}.
    material_locations = {}
    
    for m in materials:
        material_locations[m] = Material.objects.filter(name=m)
    
    for t in tags:
        t.url = url_safe(t.name)

    context_dict['experiment'] = experiment
    context_dict['materials'] = materials
    context_dict['material_locations'] = material_locations
    context_dict['tags'] = tags
    context_dict['procedure'] = experiment.procedure
    context_dict['main_photo'] = experiment.main_photo
    context_dict['id'] = experiment.id
    context_dict['text'] = experiment.text
    context_dict['images'] = Image.objects.filter(experiment=experiment)
    context_dict['resources'] = Resource.objects.filter(experiment=experiment)
    context_dict['links'] = Link.objects.filter(experiment=experiment)

    # Go render the response and return it to the client.
    return render(request, 'inventory/experiment.html', context_dict)

    
def tag(request, tag_name_url):
    # Change underscores in the experiment name to spaces.
    tag_name = eye_safe(tag_name_url)
    context_dict = {'tag_name': tag_name}
    
    tag = get_object_or_404(Tag, name = tag_name)
    context_dict['tag'] = tag
    
    # Retrieve all of the Experiment objects with this tag.
    # Maybe there is a more idiomatic way of doing this...
    #experiments = []
    #for e in Experiment.objects.all():
        #if tag in e.tags.all():
            #e.url = url_safe(e.title)
            #experiments.append(e)
            
    #context_dict['experiments'] = experiments  
            
    context_dict['experiments'] = Experiment.objects.filter(tags__name=tag.name).order_by('title')
    for e in context_dict['experiments']:
        e.url = url_safe(e.title)
    
    return render(request, 'inventory/tag.html', context_dict)
    
def room_index(request):
    context_dict = {}
    
    context_dict['first_bio'] = Room.objects.filter(hall="Biology").order_by('number')
    context_dict['first_phys'] = Room.objects.filter(hall="Physics").order_by('number')
    context_dict['second'] = Room.objects.filter(floor="Second Floor").order_by('number')
    context_dict['ground'] = Room.objects.filter(floor="Ground Floor").order_by('number')
    
    for hall in (context_dict['first_bio'], context_dict['first_phys'], context_dict['second'], context_dict['ground']):
        for room in hall:
            room.url = url_safe(room.number)
    
    return render(request, 'inventory/room_index.html', context_dict)

def room(request, room_url):
    room_number = eye_safe(room_url)
    room = get_object_or_404(Room, number=room_number)
    room.url = url_safe(room_number)
    
    context_dict = {'room_number': room_number}
    
    # Retrieve all of the materials in the room.
    materials = Material.objects.filter(room=room).order_by('location')
    context_dict['room'] = room
    context_dict['materials'] = materials
    
    return render(request, 'inventory/room.html', context_dict)
    
def rooms_all(request):
    context_dict = {}
    
    # Then, get each type of Material and add it to the dict.
    # By using values_list w/"flat" param, we get a list instead of an unhashable dict.
    material_types = Material.objects.values_list('name', flat=True).distinct()
    material_locations = {}
    for m in material_types:
        locations = Material.objects.filter(name=m)
        material_locations[m] = locations
    
    context_dict['material_locations'] = material_locations
    # Render the response and send it back!
    return render(request, 'inventory/rooms_all.html', context_dict)

@login_required
def experiment_edit(request, id=None, template_name='inventory/experiment_edit.html'):
    context_dict = {}
    ResourceFormSet = modelformset_factory(Resource, form = ResourceForm)
    ImageFormSet = modelformset_factory(Image, form = ImageForm)
    LinkFormSet = modelformset_factory(Link, form=LinkForm)
    
    if id:
        experiment = get_object_or_404(Experiment, pk=id)
        experiment.url = url_safe(experiment.title)
        
        resource_qset = Resource.objects.filter(experiment = experiment)
        resource_formset = ResourceFormSet(queryset = resource_qset, prefix='resources')
        
        image_qset = Image.objects.filter(experiment=experiment)
        image_formset = ImageFormSet(queryset=image_qset, prefix='images')
        
        link_qset = Link.objects.filter(experiment=experiment)
        link_formset = LinkFormSet(queryset=link_qset, prefix='links')
        
    else:
        experiment = Experiment()
        
        resource_formset = ResourceFormSet(queryset=Resource.objects.none(), prefix='resources')
        image_formset = ImageFormSet(queryset=Image.objects.none(), prefix='images')
        link_formset = LinkFormSet(queryset=Link.objects.none(), prefix='links')
 
    if request.POST:
        form = ExperimentForm(request.POST, request.FILES, instance=experiment)
        resource_formset = ResourceFormSet(request.POST, request.FILES, prefix='resources')
        image_formset = ImageFormSet(request.POST, request.FILES, prefix='images')
        link_formset = LinkFormSet(request.POST, prefix='links')
        
        if form.is_valid() and resource_formset.is_valid() and image_formset.is_valid():
            if 'main_photo' in request.FILES:
                form.main_photo = request.FILES['main_photo']
            
            form.save()
            
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
            # If the save was successful, redirect to another page
            redirect_url = reverse('experiment', args=[url_safe(experiment.title)])
            return HttpResponseRedirect(redirect_url)
        else:
            messages.add_message(request, messages.ERROR, _('There was a problem saving the experiment. See errors below and please try again.'))
 
    else:
        form = ExperimentForm(instance=experiment)
    
    context_dict['experiment'] = experiment
    context_dict['form'] = form
    context_dict['resource_formset'] = resource_formset
    context_dict['image_formset'] = image_formset
    context_dict['link_formset'] = link_formset
 
    return render(request, template_name, context_dict)

"""@login_required
def text_edit(request):
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
        
    context_dict['form'] = form
    return render(request, template_name, context_dict)"""
    
@login_required
def room_edit(request, room_url):
    number = eye_safe(room_url)
    room = Room.objects.get(number = number)
    MaterialFormSet = modelformset_factory(Material, form = MaterialForm)
    qset = Material.objects.filter(room = room)
    # Not sure why it is reassigned in this way - test as one assignment statement later?
    formset = MaterialFormSet(queryset = qset)
    
    if request.method == 'POST':
        # deal with posting the data
        formset = MaterialFormSet(request.POST, queryset = qset)
        if formset.is_valid():
            # if it is not valid then the "errors" will fall through and be returned
            fset = formset.save(commit=False)
            room.date_modified = datetime.datetime.now()
            room.save()
            for material in fset:
                material.room = room
                material.save()
            
            messages.add_message(request, messages.SUCCESS, _('Room successfully updated.'))
            redirect_url = reverse('room', args=[room.number])
            return HttpResponseRedirect(redirect_url)
        else:
            messages.add_message(request, messages.ERROR, _('There was a problem saving the experiment. Please try again.'))

    return render(request, 'inventory/room_edit.html', {'formset': formset, 'room': room})
    

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

            messages.add_message(request, messages.SUCCESS, _('Registration successful. The administrator has been notified, and will activate your account.'))
            registered = True
            send_mail('Pending user registration', 'A user has registered with the name %s and email %s. Please check the registration page.' % (user.username, user.email), 'accounts@sjclab.herokuapp.com', ['max.silbiger@gmail.com', 'thatkidsam@gmail.com'], fail_silently=False)

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            messages.add_message(request, messages.ERROR, _('There was a problem registering. Please try again.'))
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 
            'registration/registration_form.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
            
def user_login(request):
    next = ""
    username = ""

    if 'next' in request.GET:
        next = request.GET['next']

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, _('Welcome, %s!' % username))
                if next == "":
                    return HttpResponseRedirect('/inventory/experiments/')
                else:
                    request.user = user
                    return HttpResponseRedirect(request.POST.get('next'))
            else:
                messages.add_message(request, messages.ERROR, _('Your account is not active yet. Please wait for the administrator to approve your registration.'))
                return render(request, 'registration/login.html', {})
        else:
            messages.add_message(request, messages.ERROR, _('Invalid login details supplied, please try again.'))
            return render(request, 'registration/login.html', {})

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response(
        'registration/login.html',
        {
        'username': username,
        'next': next,
        },
        context_instance=RequestContext(request)
        )

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    messages.add_message(request, messages.SUCCESS, _('You have logged out.'))
    return HttpResponseRedirect('/inventory/')
    
@permission_required('is_superuser')
def admin_user_approval(request):
     users = User.objects.filter(is_active=False)
     
     return render_to_response('inventory/user_approval.html', {'users': users}, context_instance=RequestContext(request))
     
@permission_required('is_superuser')
def approve_user(request, id):
    user = User.objects.get(id=id)
    
    user.is_active = True
    
    messages.add_message(request, messages.SUCCESS, _('User %s successfully activated.' % user.username))
    return redirect('admin_user_approval')