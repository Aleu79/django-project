from django import forms
from .models import *
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

class formTaskComment(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['comment']  

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if not comment:
            raise forms.ValidationError("El comentario no puede estar vacío.")
        return comment