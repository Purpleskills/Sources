from django import forms
from .models import *
from core.models import DifficultyChoice

class CourseFilterForm(forms.Form):
    class Meta:
        # model = Course
        fields = ('difficulty', 'provider')

    topic = forms.CharField(label='Topic', widget=forms.TextInput( attrs={ 'class': 'form-control basicAutoComplete'}))
    difficulty = forms.ChoiceField(label='Difficulty', required=False,
                                         initial=DifficultyChoice.All.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    duration = forms.ChoiceField(label='Duration', required=False,
                                         initial=DurationChoice.All.value, choices=[(tag.value, tag.name) for tag in DurationChoice],
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    provider = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=CourseProvider.objects.all())