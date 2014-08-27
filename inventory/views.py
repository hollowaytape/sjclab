from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from inventory.models import Experiment, Material, Text, Room, Tag
from inventory.forms import ExperimentForm, RoomForm, MaterialForm, UserForm, UserProfileForm
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.forms.models import inlineformset_factory

def url_safe(string):
    """ Replaces spaces with underscores, making a string safer for urls."""
    return string.replace(' ', '_').replace("'", "").replace(".", "")

def eye_safe(string):
    """ Undoes the operation of url_safe()."""
    return string.replace('_', ' ')

def experiment_index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    
    fr_experiments, jr_experiments, sr_experiments, tags = [], [], [], []
    
    for e in Experiment.objects.filter(text__year="Freshman").order_by('session'):
        fr_experiments.append(e)
    
    for e in Experiment.objects.filter(text__year="Junior").order_by('session'):
        jr_experiments.append(e)
    
    for e in Experiment.objects.filter(text__year="Senior").order_by('session'):
        sr_experiments.append(e)

    for t in Tag.objects.order_by('name'):
        tags.append(t)
    
    context_dict = {}
    context_dict['fr_experiments'] = fr_experiments
    context_dict['jr_experiments'] = jr_experiments
    context_dict['sr_experiments'] = sr_experiments
    context_dict['tags'] = tags
    
    # Sanitize experiment names for use in urls.
    for year in (fr_experiments, jr_experiments, sr_experiments):
        for experiment in year:
            experiment.url = url_safe(experiment.title)
    
    # Render the response and send it back!
    return render_to_response('inventory/experiment_index.html', context_dict, context)

    
def experiment(request, experiment_name_url):
    context = RequestContext(request)
    
    # Change underscores in the experiment name to spaces.
    experiment_name = eye_safe(experiment_name_url)
    
    # Context dictionary to pass to the template.
    # Contain the name of the experiment passed by the user.
    context_dict = {'experiment_name': experiment_name}
    
    experiment = get_object_or_404(Experiment, title=experiment_name)
    
    # materials: each kind of material necessary for the experiment.
    materials = experiment.materials.all()
    
    # material_locations: dict with entries {material: [instance, instance]}.
    material_locations = {}
    
    for m in materials:
        locations = Material.objects.filter(name=m)
        material_locations[m] = locations
    
    print materials    
    print material_locations
    context_dict['experiment'] = experiment
    context_dict['materials'] = materials
    context_dict['material_locations'] = material_locations
    context_dict['tags'] = experiment.tags
    context_dict['procedure'] = experiment.procedure
    context_dict['resources'] = experiment.resources
    context_dict['main_photo'] = experiment.main_photo
    context_dict['id'] = experiment.id
    context_dict['text'] = experiment.text

    # Go render the response and return it to the client.
    return render_to_response('inventory/experiment.html', context_dict, context)

    
def tag(request, tag_name):
    context = RequestContext(request)
    
    # Context dictionary to pass to the template.
    # Contain the name of the room passed by the user.
    context_dict = {'tag_name': tag_name}
    
    # Can we find an experiment with the given name?
    # If we can't, the .get() raises DoesNotExist.
    # So the .get() method returns one model or raises an exception.
    tag = get_object_or_404(Tag, name = tag_name)
    
    # Retrieve all of the Experiment objects with this tag.
    # Maybe there is a more idiomatic way of doing this...
    experiments = []
    for e in Experiment.objects.all():
        if tag in e.tags.all():
            e.url = url_safe(e.title)
            experiments.append(e)
    
    # Add experiments to the context dictionary.
    context_dict['experiments'] = experiments
    
    # Also add the tag, so we can check if it exists.
    context_dict['tag'] = tag
    
    # Go render the response and return it to the client.
    return render_to_response('inventory/tag.html', context_dict, context)
    
def room_index(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    
    # Query the database for a list of all rooms.
    # Order the rooms by number.
    # Place the list in our context_dict dictionary,
    # which will be passed to the template engine.
    room_list = Room.objects.order_by('number')
    context_dict = {'rooms': room_list}
    
    # Render the response and send it back!
    return render_to_response('inventory/room_index.html', context_dict, context)

def room(request, room_number):
    context = RequestContext(request)
    
    # Context dictionary to pass to the template.
    # Contain the name of the room passed by the user.
    context_dict = {'room_number': room_number}
    
    # Can we find an experiment with the given name?
    # If we can't, the .get() raises DoesNotExist.
    # SO the .get() method returns one model or raises an exception.
    room = get_object_or_404(Room, number=room_number)
    
    # Retrieve all of the materials in the room.
    materials = Material.objects.filter(room=room).order_by('location')
    context_dict['materials'] = materials
    
    # Go render the response and return it to the client.
    return render_to_response('inventory/room.html', context_dict, context)
    
def rooms_all(request):
    # Obtain the context from the HTTP request.
    context = RequestContext(request)
    context_dict = {}
    
    # Then, get each type of Material and add it to the dict.
    # By using values_list w/flat parameter, we get a list instead of an unhashable dict.
    material_types = Material.objects.values_list('name', flat=True).distinct()
    material_locations = {}
    for m in material_types:
        locations = Material.objects.filter(name=m)
        material_locations[m] = locations
    
    context_dict['material_locations'] = material_locations
    # Render the response and send it back!
    return render_to_response('inventory/rooms_all.html', context_dict, context)

@login_required
def experiment_edit(request, id=None, template_name='inventory/experiment_edit.html'):
    if id:
        experiment = get_object_or_404(Experiment, pk=id)
    else:
        experiment = Experiment()
 
    if request.POST:
        form = ExperimentForm(request.POST, request.FILES, instance=experiment)
        if form.is_valid():
            if 'resources' in request.FILES:
                form.resources = request.FILES['resources']
            if 'main_photo' in request.FILES:
                form.main_photo = request.FILES['main_photo']
            form.save()

            messages.add_message(request, messages.SUCCESS, _('Experiment successfully updated.'))
            # If the save was successful, redirect to another page
            redirect_url = reverse('experiment', args=[url_safe(experiment.title)])
            return HttpResponseRedirect(redirect_url)
        else:
            messages.add_message(request, messages.ERROR, _('There was a problem saving the experiment. Please try again.'))
 
    else:
        form = ExperimentForm(instance=experiment)
 
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

@login_required
def room_edit(request, number):
    room = Room.objects.get(number = number)
    MaterialFormSet = inlineformset_factory(Material, Room, extra=1)
    materials = Material.objects.filter(room = room).values()
    formset = MaterialFormSet(initial=materials)
    
    if request.method == 'POST':
        # deal with posting the data
        formset = MaterialFormSet(request.POST, queryset = qset)
        if formset.is_valid():
            # if it is not valid then the "errors" will fall through and be returned
            formset.save()
            messages.add_message(request, messages.SUCCESS, _('Room successfully updated.'))
            redirect_url = reverse('room', args=[room.number])
            return HttpResponseRedirect(redirect_url)
        else:
            messages.add_message(request, messages.ERROR, _('There was a problem saving the experiment. Please try again.'))
    
    context_dict = {'formset':formset,
                    'room':room}

    return render_to_response('inventory/room_edit.html', {'formset': formset, 'room': room}, RequestContext(request))
    

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            messages.add_message(request, messages.SUCCESS, _('Registration successful. Welcome!'))
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            messages.add_message(request, messages.ERROR, _('There was a problem registering. Please try again.'))
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'inventory/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)
            
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/inventory/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            messages.add_message(request, messages.ERROR, _('Invalid login details supplied, please try again.'))
            print "Invalid login details: {0}, {1}".format(username, password)
            return render_to_response('inventory/login.html', {}, context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('inventory/login.html', {}, context)
        
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    messages.add_message(request, messages.SUCCESS, _('You have logged out.'))
    return HttpResponseRedirect('/inventory/')