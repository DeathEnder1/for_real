from django import forms
from .models import Blog1
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email

class Blog_Form(forms.ModelForm):
    class Meta:
        model = Blog1
        fields = '__all__'
        exclude =['user']
    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        try: 
            blog=Blog1.objects.get(title = title)
        except Blog1.DoesNotExist:
            return title
        raise ValidationError("This title is already used")
    def clean_content(self):
        data = self.cleaned_data["content"]
        if len(data)<10:
            raise ValidationError("Your must have at least 100 characters")
        return data
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']