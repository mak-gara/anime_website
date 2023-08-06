from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import Review, CustomUser, Communication


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text',)


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    profile_pic = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = CustomUser
        fields = ('profile_pic', 'username', 'email', 'first_name', 'last_name')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Communication
        fields = ('name', 'email', 'message')
