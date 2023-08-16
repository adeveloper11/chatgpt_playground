from django.core import validators
from django import forms
from .models import QueryOption, Feedbackdata

class QueryForms(forms.ModelForm):
    class Meta:
        model = QueryOption
        fields = ['option_name', 'option_value']  #for showing in frontend html

class DataFeedback(forms.ModelForm):
    class Meta:
        model = Feedbackdata
        fields = ['Name', 'Mobile', 'Email', 'Feedback']