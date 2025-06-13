from .models import Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name']
        labels={
            'email':'Email адрес',
            'first_name':'Имя', 
            'last_name':'Фамилия',
            'username':'Имя пользователя'
        }

class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    delete_avatar = forms.BooleanField(
        required=False,
        label='Удалить текущий аватар',
        widget=forms.CheckboxInput(attrs={'class': 'delete-avatar-checkbox'})
    )

    class Meta:
        model = Profile
        fields = ['address', 'avatar',  'delete_avatar','about']
        labels = {
            'address': 'Адрес',
            'about':"О себе"
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Если чекбокс отмечен — удаляем файл и сбрасываем поле
        if self.cleaned_data.get('delete_avatar') and profile.avatar:
            profile.avatar.delete(save=False)
            profile.avatar = 'img/sbcf-default-avatar.png'
        if commit:
            profile.save()
        return profile




class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
