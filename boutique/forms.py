# boutique/forms.py
from django import forms
from .models import Women, Men, Kids, Accessory
# Authentication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class WomenForm(forms.ModelForm):
    class Meta:
        model = Women
        fields = '__all__'  # Include all fields

class MenForm(forms.ModelForm):
    class Meta:
        model = Men
        fields = '__all__'  # Include all fields

class KidsForm(forms.ModelForm):
    class Meta:
        model = Kids
        fields = '__all__'  # Include all fields

class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = '__all__'  # Include all fields

# Authentication
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



