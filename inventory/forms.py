from django import forms

class ExperimentForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    text = forms.CharFIeld(max_length=100)
    