from django import forms
from .models import *

class CourseFilterForm(forms.Form):
    class Meta:
        # model = Course
        fields = ('category', 'subcategory', 'provider')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['category'].queryset = CourseCategory.objects.none()

    category = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                          queryset=CourseCategory.objects.all())
    subcategory = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=CourseSubCategory.objects.all())
    provider = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=CourseProvider.objects.all())