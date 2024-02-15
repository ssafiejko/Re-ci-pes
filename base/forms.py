from django.forms import ModelForm
from .models import Recipe, User
from django.contrib.auth.forms import UserCreationForm

class RecipeForm(ModelForm):
    class Meta:
        model= Recipe
        fields= '__all__'
        exclude=['autor']

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['avatar', 'name', 'username', 'email', 'bio']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['name', 'username', 'email', 'password1', 'password2']