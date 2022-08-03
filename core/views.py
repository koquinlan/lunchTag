from django import forms
from django.http import HttpResponse

from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.db import IntegrityError

from core.utils import populate_edges, make_pairings, push_pairings
from core.models import Profile, Pairing, Edge

from .forms import NewUserForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required, user_passes_test  
from core.forms import UpdateUserForm, UpdateProfileForm

from cloudinary.forms import cl_init_js_callbacks 
from cloudinary import CloudinaryImage     



def homepage(request):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=request.user)
		if Profile.objects.filter(user=profile.tag_pairing).exists():
			pair_profile = Profile.objects.get(user=profile.tag_pairing)
		else:
			pair_profile = None

		pair_profile2 = None
		if profile.tag_pairing2 != None:
			if Profile.objects.filter(user=profile.tag_pairing2).exists():
				pair_profile2 = Profile.objects.get(user=profile.tag_pairing2)
				

		return render(request=request, template_name='core/userhome.html', context={"pairing":profile.tag_pairing, "pair_profile":pair_profile, "pairing2":profile.tag_pairing2, "pair_profile2":pair_profile2})
	return render(request=request, template_name='core/home.html')



def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)

		if form.is_valid():
			try:
				newUser = form.save()
			except IntegrityError:
				messages.error(request, "Unsuccessful registration. It's likely a user with this First and Last name already exists. Try logging in or contact admin for help if needed.") 
				return redirect("core:login")

			email = form.cleaned_data['username']
			password = form.cleaned_data['password1']

			newUser = authenticate(username=email, password=password)

			profile = Profile.objects.create(user=newUser)
			profile.avatar = CloudinaryImage("default.jpg").image()
			populate_edges(newUser)
			login(request, newUser)
			messages.success(request, f"Registration successful, You are now logged in as {newUser.first_name} {newUser.last_name}.")

			return redirect("core:homepage")

		messages.error(request, "Unsuccessful registration. Invalid information.")  

	form = NewUserForm()
	return render (request=request, template_name="core/register.html", context={"register_form":form})



def login_request(request):
	if request.user.is_authenticated:
		return redirect("core:homepage")
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)

		if form.is_valid():
			if not request.POST.get('remember_me', None):
				request.session.set_expiry(0)
			
			email = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=email, password=password)

			if user is not None:
				login(request, user)
				messages.success(request, f"You are now logged in as {user.first_name} {user.last_name}.")

				return redirect("core:homepage")
		messages.error(request,"Invalid email or password.")

	form = AuthenticationForm()
	return render(request=request, template_name="core/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.success(request, f"You are now logged out.")
	return redirect("core:homepage")


@login_required
def account_request(request):
	profile = Profile.objects.get(user=request.user)
	return render(request, "core/account.html", {'user_profile': profile, 'allusers': User.objects.all(), 'userstrikes': profile.strikes.all()})

@login_required
def edit_account_request(request):
	profile = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		user_form = UpdateUserForm(request.POST, instance=request.user)

		if user_form.is_valid():
			user_form.save()
			messages.success(request, 'Your profile is updated successfully')
			return redirect(to='core:account')
	else:
		user_form = UpdateUserForm(instance=request.user)

	return render(request, 'core/edit_account.html', {'user_form': user_form, 'user_profile': profile, 'userstrikes': profile.strikes.all()})


@login_required
def edit_profile_request(request):
	profile = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		profile_form = UpdateProfileForm(request.POST, instance=profile)

		if profile_form.is_valid():
			profile_form.save()
			messages.success(request, 'Your profile is updated successfully')
			return redirect(to='core:account')
	else:
		profile_form = UpdateProfileForm(instance=profile)

	return render(request, 'core/edit_profile.html', {'profile_form': profile_form, 'user_profile': profile, 'userstrikes': profile.strikes.all()})


@login_required
def strike_request(request, userID):
	req_user = request.user
	req_profile = Profile.objects.get(user=req_user)
	struck_user = User.objects.get(id=userID)

	req_profile.strikes.add(struck_user)
	req_profile.save()

	for edge in req_user.user1.all():
		if edge.user2 == struck_user:
			edge.active = False
			edge.save()
			return redirect(to='core:account')

	for edge in req_user.user2.all():
		if edge.user1 == struck_user:
			edge.active = False
			edge.save()
			return redirect(to='core:account')
	
	messages.error(request, 'Strike may have failed, please contact admin with contact above to confirm or try again')
	return redirect(to='core:account')


@login_required
def crush_request(request, userID):
	req_user = request.user
	req_profile = Profile.objects.get(user=req_user)
	crush_user = User.objects.get(id=userID)

	req_profile.crush = crush_user
	req_profile.save()
		
	for edge in req_user.user1.all():
		if edge.user2 == crush_user:
			edge.weight = edge.weight*2
			edge.save()
			return redirect(to='core:account')

	for edge in req_user.user2.all():
		if edge.user1 == crush_user:
			edge.weight = edge.weight*2
			edge.save()
			return redirect(to='core:account')
	
	messages.error(request, 'Crush may have failed, please contact admin to confirm')
	return redirect(to='core:account')


@login_required
def remove_crush_request(request):
	req_user = request.user
	req_profile = Profile.objects.get(user=req_user)
	old_crush = req_profile.crush

	req_profile.crush = None
	req_profile.save()
		
	for edge in req_user.user1.all():
		if edge.user2 == old_crush:
			edge.weight = edge.weight/2
			edge.save()
			return redirect(to='core:account')

	for edge in req_user.user2.all():
		if edge.user1 == old_crush:
			edge.weight = edge.weight/2
			edge.save()
			return redirect(to='core:account')
	
	messages.error(request, 'Removing crush may have failed, please contact admin to confirm')
	return redirect(to='core:account')


@login_required
def remove_strike_request(request, userID):
	req_user = request.user
	req_profile = Profile.objects.get(user=req_user)
	unstruck_user = User.objects.get(id=userID)

	req_profile.strikes.remove(unstruck_user)
	req_profile.save()

	for edge in req_user.user1.all():
		if edge.user2 == unstruck_user:
			edge.active = True
			edge.save()
			return redirect(to='core:account')

	for edge in req_user.user2.all():
		if edge.user1 == unstruck_user:
			edge.active = True
			edge.save()
			return redirect(to='core:account')
	
	messages.error(request, 'Removing this strike may have failed, please contact admin with contact above to confirm or try again')
	return redirect(to='core:account')

@login_required
def toggle_active_request(request):
	profile = Profile.objects.get(user=request.user)
	profile.active = not profile.active
	profile.save()
	if profile.active:
		messages.success(request, 'You have opted back in and will be included in the next pairing!')
	else:
		messages.warning(request, 'You have opted out and will NOT be included in the next pairing!')
	return redirect(to='core:account')



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Pairer').exists())
def edit_pairs_request(request):
	allpairings = Pairing.objects.all()
	return render(request, 'core/edit_pairings.html', {'allpairings': allpairings})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Pairer').exists())
def create_pairings_request(request):
	code = make_pairings(request)
	if code == -1:
		messages.error(request, 'For whatever reason this pairing tried to match someone with their strike. Could try again but probably need to contact Kyle. Sorry...')
	elif code == 2:
		messages.success(request, 'This worked but a pair of 3 had to be made')
	elif code == 1:	
		messages.success(request, 'Pairings successfully generated')
	return redirect(to='core:edit_pairings')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Pairer').exists())
def push_pairings_request(request):
	code = push_pairings(Pairing.objects.all(), request)
	if code == -1:
		messages.error(request, 'For whatever reason this pairing tried to match someone with their strike. Could try again but probably need to contact Kyle. Sorry...')
	elif code == -2:
		messages.error(request, 'This error code is extra bad!! Pairings were pushed but there may have been a pair that overrode a strike. Contact Kyle or remake and try again.')
	elif code == 1:
		messages.success(request, 'Pairings successfully pushed')
	return redirect(to='core:edit_pairings')