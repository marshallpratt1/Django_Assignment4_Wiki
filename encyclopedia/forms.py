
from turtle import title
from django import forms
class EntryForm(forms.Form):
    entry_title = forms.CharField(label="Title")
    entry_content = forms.CharField(label="Entry", help_text="Write your entry here.", widget=forms.Textarea())

class NewTitle(forms.Form):
    new_title = forms.CharField(label="Title")

class NewEntry(forms.Form):
    new_title = forms.CharField(label="Title")
    new_content = forms.CharField(label="Entry", widget=forms.Textarea())