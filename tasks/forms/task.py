# forms.py
from django import forms
from tasks.models import Task
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'due_date',
            'priority', 
            'photos',
            'is_complete'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(
                attrs={'class': 'form-control',
                'type': 'date'}),
            'priority': forms.Select(
                attrs={'class': 'form-control'}),
            'photos': forms.ClearableFileInput(
                attrs={'class': 'form-control'}),
            'is_complete': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}),
        }


    def clean_due_date(self):
        # Ensure that the due date is not in the past
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError(
                "Due date cannot be in the past."
            )
        return due_date



class TaskFilterForm(forms.Form):
    title = forms.CharField(
        label=_('Title'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control mr-2'})
    )
    created_at_start = forms.DateField(
        label=_('Created At (Start)'),
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mr-2'})
    )
    created_at_end = forms.DateField(
        label=_('Created At (End)'),
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mr-2'})
    )
    due_date_start = forms.DateField(
        label=_('Due Date (Start)'),
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mr-2'})
    )
    due_date_end = forms.DateField(
        label=_('Due Date (End)'),
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mr-2'})
    )
    priority = forms.ChoiceField(
        label=_('Priority'),
        choices=Task.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control mr-2'})
    )
    is_complete = forms.NullBooleanField(
        label=_('Is Complete'),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input mr-2'})
    )
