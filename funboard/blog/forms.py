from django import forms
from .models import Comment, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'
        

    class Meta:
        model = Post
        fields = ['title', 'body', 'cat', 'status', 'image', 'video']
        widgets = {
            'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Заголовок поста'
            }),

            'body': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Текст поста'
            }),
            
            'image': forms.FileInput
        }


class RegisterUserForm(UserCreationForm):

    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': "inputPassword"}))
    password2 = forms.CharField(label='Re-enter password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': "inputPassword"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': "inputPassword"}))