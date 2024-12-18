from django import forms
from .models import Task
from django.forms import DateTimeInput

class formTask(forms.ModelForm):
    is_personal = forms.BooleanField(initial=True, required=False, label='Es tarea personal')

    class Meta:
        model = Task
        fields = ['title', 'description', 'important', 'category', 'tags', 'status', 'priority', 'date_completed', 'is_personal']  

    banner_color = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color'})
    )
    date_completed = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'date'})
    )
