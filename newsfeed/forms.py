from .models import Product
from .models import Profile
from django import forms
from .models import Rating
from django.core.exceptions import ValidationError


class PostProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'image', 'mobile_number', 'location', 'category')

    def __init__(self, *args, **kwargs):
        super(PostProductForm, self).__init__(*args, **kwargs)
        self.fields['mobile_number'].widget.attrs['placeholder'] = '+63 9123456789'
        self.fields['image'].widget.attrs['multiple'] = True

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if not mobile_number.isdigit():
            raise ValidationError('Phone number must be a 10-digit number')
        if len(mobile_number) != 10:
            raise ValidationError('Phone number must be 10 digits long')
        if mobile_number[0] != '9':
            raise ValidationError('Phone number must start with 9')
        return mobile_number


class ProfileForm(forms.ModelForm):
    mobile_number = forms.CharField(max_length=10)

    class Meta:
        model = Profile
        fields = ('address', 'mobile_number', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['mobile_number'].widget.attrs['placeholder'] = '+63 9123456789'

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if not mobile_number.isdigit():
            raise ValidationError('Phone number must be a 10-digit number')
        if len(mobile_number) != 10:
            raise ValidationError('Phone number must be 10 digits long')
        if mobile_number[0] != '9':
            raise ValidationError('Phone number must start with 9')
        return mobile_number


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)])
        }
