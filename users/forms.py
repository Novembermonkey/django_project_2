from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean_email(self):
        email = self.data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'{email} not found')
        return email

    def clean_password(self):
        password = self.data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Passwors must have at least 8 characters')
        return password

class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'{email.title()} already exist ')
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password did not match')

        return confirm_password


# admin forms
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'is_staff', 'is_superuser', 'date_joined')




