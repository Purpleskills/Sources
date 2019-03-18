from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CourseUser, UserGoals
from core.models import DifficultyChoice

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = CourseUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'company')


class ProfileForm (forms.Form):
    goal_1 = forms.CharField(label='Skill goal', max_length=128, required=False, help_text='Optional.')
    level_1 = forms.ChoiceField(label='Difficulty level', required=False,
                                         initial=DifficultyChoice.All.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    goal_2 = forms.CharField(label='Skill goal', max_length=128, required=False, help_text='Optional.')
    level_2 = forms.ChoiceField(label='Difficulty level', required=False,
                                         initial=DifficultyChoice.All.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    goal_3 = forms.CharField(label='Skill goal', max_length=128, required=False, help_text='Optional.')
    level_3 = forms.ChoiceField(label='Difficulty level', required=False,
                                         initial=DifficultyChoice.All.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
                                         widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        ugs = UserGoals.objects.filter(user=self.user)
        index = 1
        for ug in ugs:
            if index > 3:   # currently only 3 are allowed
                break
            self.fields['goal_' + str(index)].initial = ug.skill_goal
            self.fields['level_' + str(index)].initial = ug.difficulty
            index += 1

    def save(self):
        goal1 = self.data['goal_1']
        level1 = self.data['level_1']
        goal2 = self.data['goal_2']
        level2 = self.data['level_2']
        goal3 = self.data['goal_3']
        level3 = self.data['level_3']
        UserGoals.objects.filter(user=self.user).delete()
        if goal1 != "":
            ug1 = UserGoals(user=self.user, skill_goal=goal1, difficulty=level1)
            ug1.save()
        if goal2 != "":
            ug2 = UserGoals(user=self.user, skill_goal=goal2, difficulty=level2)
            ug2.save()
        if goal3 != "":
            ug3 = UserGoals(user=self.user, skill_goal=goal3, difficulty=level3)
            ug3.save()

        return True