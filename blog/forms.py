from django import forms
from .models import Blog1
from django.core.exceptions import ValidationError
class Blog_Form(forms.ModelForm):
    class Meta:
        model = Blog1
        fields = '__all__'
        exclude =['user']
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title)>200: 
            raise ValidationError("Your title must have less than 200 characters")
        return title
        
        