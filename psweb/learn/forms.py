from django import forms
from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory
from extra_views import  InlineFormSet
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


# class GoalSettingForm (forms.Form):
#     goal_1 = forms.CharField(label='Skill goal', max_length=128, required=False, help_text='Optional.')
#     level_1 = forms.ChoiceField(label='Difficulty level', required=False,
#                                          initial=DifficultyChoice.All.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
#                                          widget=forms.Select(attrs={'class': 'form-control'}))
#     goal_2 = forms.CharField(label='Skill goal', max_length=128, required=False, help_text='Optional.')
#     level_2 = forms.ChoiceField(label='Difficulty level', required=False,
#                                          initial=DifficultyChoice.All.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
#                                          widget=forms.Select(attrs={'class': 'form-control'}))
#     goal_3 = forms.CharField(label='Skill goal', max_length=128, required=False, help_text='Optional.')
#     level_3 = forms.ChoiceField(label='Difficulty level', required=False,
#                                          initial=DifficultyChoice.All.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
#                                          widget=forms.Select(attrs={'class': 'form-control'}))
#
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super(GoalSettingForm, self).__init__(*args, **kwargs)
#         ugs = UserGoals.objects.filter(user=self.user)
#         index = 1
#         for ug in ugs:
#             if index > 3:   # currently only 3 are allowed
#                 break
#             self.fields['goal_' + str(index)].initial = ug.skill_goal
#             self.fields['level_' + str(index)].initial = ug.difficulty
#             index += 1
#
#     def save(self):
#         goal1 = self.data['goal_1']
#         level1 = self.data['level_1']
#         goal2 = self.data['goal_2']
#         level2 = self.data['level_2']
#         goal3 = self.data['goal_3']
#         level3 = self.data['level_3']
#         UserGoals.objects.filter(user=self.user).delete()
#         if goal1 != "":
#             ug1 = UserGoals(user=self.user, skill_goal=goal1, difficulty=level1, company=self.user.company)
#             ug1.save()
#         if goal2 != "":
#             ug2 = UserGoals(user=self.user, skill_goal=goal2, difficulty=level2, company=self.user.company)
#             ug2.save()
#         if goal3 != "":
#             ug3 = UserGoals(user=self.user, skill_goal=goal3, difficulty=level3, company=self.user.company)
#             ug3.save()
#
#         return True

class ObjectiveFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ObjectiveFormHelper, self).__init__(*args, **kwargs)
        self.form_tag = True
        self.form_class = 'form-horizontal'
        self.form_id = 'obj_form'
        self.label_class = 'col-md-2 create-label'
        self.field_class = 'col-md-10'
        self.layout = Layout(
            Div(
                Field('name'),
                Hidden('objid', ""),
                Fieldset('Add Key results',
                         Formset('okrs')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save', css_class = "savebutton")),
            )
        )
        self.render_required_fields = True


class ObjectiveForm (ModelForm):
    class Meta:
        model = Objective
        exclude = ('user', 'company',)

    id = forms.IntegerField(widget=forms.HiddenInput)
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        # self.company = self.user.org.company
        super(ObjectiveForm, self).__init__(*args, **kwargs)
        # self.helper = ObjectiveFormHelper()
        # if "id" in self.initial:
        #     self.helper.layout.fields[0].fields[1].value = self.initial["id"]


class KeyresultForm(ModelForm):
    class Meta:
        model = KeyResult
        exclude = ('progressinpercent',)

    difficulty = forms.ChoiceField(label='Difficulty level', required=False,
                                initial=DifficultyChoice.Beginner.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
                                widget=forms.Select(attrs={'class': 'form-control'}))


OKRFormSet = inlineformset_factory(Objective, KeyResult, form=KeyresultForm, extra=1, can_delete=True)



