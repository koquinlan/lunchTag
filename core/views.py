from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def homepage(request):
	return render(request=request, template_name='core/home.html')



def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)

		if form.is_valid():
			newUser = form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			newUser = authenticate(username=username, password=password)

			login(request, newUser)
			messages.success(request, f"Registration successful, You are now logged in as {username}.")

			return redirect("core:homepage")

		messages.error(request, "Unsuccessful registration. Invalid information.")  

	form = NewUserForm()
	return render (request=request, template_name="core/register.html", context={"register_form":form})



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)

			if user is not None:
				login(request, user)
				messages.success(request, f"You are now logged in as {username}.")

				return redirect("core:homepage")

		messages.error(request,"Invalid username or password.")

	form = AuthenticationForm()
	return render(request=request, template_name="core/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.success(request, f"You are now logged out.")
	return redirect("core:homepage")