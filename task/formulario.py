from django import forms
from .models import *
from django.forms import DateTimeInput

from django import forms
from .models import *

class formTask(forms.ModelForm):
    is_personal = forms.BooleanField(initial=True, required=False, label='Es tarea personal')

    class Meta:
        model = Task
        fields = ['title', 'description', 'important', 'category', 'tags', 'status', 'priority', 'date_completed', 'is_personal']  

    banner_color = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'w-full p-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500'})
    )

    date_completed = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500'})
    )

    category = forms.ModelChoiceField(
        queryset=TaskCategory.objects.all(),  
        empty_label="Selecciona una categoría",  
        widget=forms.Select(attrs={'class': 'w-full p-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=TaskTag.objects.all(),  
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'w-full p-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500'})
    )

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full p-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500 resize-none'}))


class formTaskComment(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['comment']  

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if not comment:
            raise forms.ValidationError("El comentario no puede estar vacío.")
        return comment
