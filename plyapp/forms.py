from django import forms
from .models import QueryOption, Feedbackdata
from django.core.validators import RegexValidator

class QueryForms(forms.ModelForm):
    class Meta:
        model = QueryOption
        fields = ['option_name', 'option_value']  #for showing in frontend html


class DataFeedback(forms.Form):
    Name = forms.CharField(max_length=50)
    Mobile = forms.IntegerField()
    Email = forms.EmailField(max_length=300)
    Feedback = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Feedbackdata
        fields = ['Name', 'Mobile', 'Email', 'Feedback']

