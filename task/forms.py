from django import forms
from task.models import task
from django.forms import ModelForm


class TaskForm(ModelForm):
    class Meta:
        model = task
        fields = ['task_name','task_description','task_is_done','author']
        widgets = {'author': forms.HiddenInput}
