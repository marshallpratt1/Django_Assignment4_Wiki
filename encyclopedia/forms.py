
from turtle import title
from django import forms
class NewTaskForm(forms.Form):
    entry_title = forms.CharField()
    entry_content = forms.CharField(widget=forms.Textarea())

    