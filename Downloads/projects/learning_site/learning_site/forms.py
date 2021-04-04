from django import forms
from django.core import validators

def must_be_empty(value):
    if value:
        raise forms.ValidationError('Is not empty')

class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Verify Email')
    suggestion = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(required=False,
                               widget=forms.HiddenInput,
                               label="Leave empty",
                               validators=[must_be_empty],)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data.get('verify_email')
        if email != verify:
            raise forms.ValidationError('Emails did not match')