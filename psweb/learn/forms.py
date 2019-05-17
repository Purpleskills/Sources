from django import forms
from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory
from core.models import DifficultyChoice, DurationChoice, Duration
from core.custom_layout_object import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit, Hidden

class CourseFilterForm(forms.Form):
    class Meta:
        # model = Course
        fields = ('difficulty', 'provider')

    topic = forms.CharField(label='Topic', widget=forms.TextInput( attrs={ 'class': 'form-control basicAutoComplete'}))
    difficulty = forms.ChoiceField(label='Difficulty', required=False,
                                         initial=DifficultyChoice.Beginner.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    duration = forms.ChoiceField(label='Duration', required=False,
                                         initial=DurationChoice.All.value, choices=[(tag.value, tag.name) for tag in DurationChoice],
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    provider = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=CourseProvider.objects.all())


# class ObjectiveFormHelper(FormHelper):
#     def __init__(self, *args, **kwargs):
#         super(ObjectiveFormHelper, self).__init__(*args, **kwargs)
#         self.form_tag = True
#         self.form_class = 'form-horizontal'
#         self.form_id = 'obj_form'
#         self.label_class = 'col-md-2 create-label'
#         self.field_class = 'col-md-10'
#         self.layout = Layout(
#             Div(
#                 Field('name'),
#                 Hidden('objid', ""),
#                 Fieldset('Add Key results',
#                          Formset('okrs')),
#                 HTML("<br>"),
#                 ButtonHolder(Submit('submit', 'save', css_class = "savebutton")),
#             )
#         )
#         self.render_required_fields = True


class ObjectiveForm (ModelForm):
    class Meta:
        model = Objective
        exclude = ('user', 'company',)

    id = forms.IntegerField(widget=forms.HiddenInput)
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        # self.company = self.user.org.company
        super(ObjectiveForm, self).__init__(*args, **kwargs)


class KeyresultForm(ModelForm):
    class Meta:
        model = KeyResult
        exclude = ('progressinpercent',)

    difficulty = forms.ChoiceField(label='Difficulty level', required=False,
                                initial=DifficultyChoice.Beginner.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
                                widget=forms.Select(attrs={'class': 'form-control'}))


OKRFormSet = inlineformset_factory(Objective, KeyResult, form=KeyresultForm, extra=1, can_delete=True)



