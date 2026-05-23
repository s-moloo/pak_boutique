# boutique/forms.py
from django import forms
from .models import Women, Men, Kids, Accessory
# Authentication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

AVAILABLE_SIZES = [
    ('XS', 'Extra Small (XS)'),
    ('S', 'Small (S)'),
    ('M', 'Medium (M)'),
    ('L', 'Large (L)'),
    ('XL', 'Extra Large (XL)'),
    ('XXL', 'Custom Stitch / XXL'),
]

class WomenForm(forms.ModelForm):
    # Override the default text box with Multiple Choice Checkboxes
    size = forms.MultipleChoiceField(
        choices=AVAILABLE_SIZES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox checkbox-primary'}),
        help_text="Select all sizes available for this item."
    )

    class Meta:
        model = Women
        fields = ['description', 'category', 'color', 'size', 'price', 'image', 'details']

    # This magic function takes the checked boxes and saves them as a clean string ("S, M, L")
    def clean_size(self):
        selected_sizes = self.cleaned_data['size']
        return ", ".join(selected_sizes)
    
class MenForm(forms.ModelForm):
    size = forms.MultipleChoiceField(
        choices=AVAILABLE_SIZES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox checkbox-primary'}),
        help_text="Select all sizes available for this item."
    )

    class Meta:
        model = Men
        fields = '__all__'  # Include all fields

    def clean_size(self):
        selected_sizes = self.cleaned_data['size']
        return ", ".join(selected_sizes)

class KidsForm(forms.ModelForm):
    class Meta:
        model = Kids
        fields = ['description', 'category', 'color', 'size', 'price', 'image', 'details']

class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ['description', 'category', 'color', 'size', 'price', 'image', 'details']

# Authentication
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



