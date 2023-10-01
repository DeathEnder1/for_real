from django import forms
from .models import Blog1

class Blog_Form(forms.ModelForm):
    class Meta:
        model = Blog1
        fields = '__all__'
        exclude =['user']