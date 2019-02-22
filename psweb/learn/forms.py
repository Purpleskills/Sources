from django import forms
from .models import *

class CourseFilterForm(forms.Form):
    class Meta:
        # model = Course
        fields = ('difficulty', 'provider')

    topic = forms.CharField(label='Course topic', widget=forms.TextInput( attrs={ 'class': 'form-control', 'class': 'basicAutoComplete'}))
    difficulty = forms.ChoiceField(label='Difficulty level', required=False,
                                         initial=DifficultyChoice.All.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    provider = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=CourseProvider.objects.all())