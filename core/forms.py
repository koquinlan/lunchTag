from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Profile
from cloudinary.forms import CloudinaryFileField


# Create your forms here.

class NewUserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = user.username
		user.username = user.first_name + '_' + user.last_name
		if commit:
			user.save()
		return user


class UpdateUserForm(forms.ModelForm):
	first_name = forms.CharField(max_length=100, required=True)
	last_name = forms.CharField(max_length=100, required=True)
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']


class UpdateProfileForm(forms.ModelForm):
	# avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
	pronouns = forms.CharField(max_length=100, required=False)
	phone = forms.CharField(max_length=100, required=False)
	image = forms.ImageField(label='', required=False, widget=forms.FileInput)

	class Meta:
		model = Profile
		fields = ['pronouns', 'phone', 'image']
		
