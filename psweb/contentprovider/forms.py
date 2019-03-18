from django import forms
from learn.models import Course, CourseProvider, Instructor
from core.models import DifficultyChoice
from djmoney.models.fields import MoneyField

class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.

    >>> from django.core.files.uploadedfile import SimpleUploadedFile
    >>>
    >>> t = ExtFileField(ext_whitelist=(".pdf", ".txt"))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.pdf', 'Some File Content'))
    >>> t.clean(SimpleUploadedFile('filename.txt', 'Some File Content'))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.exe', 'Some File Content'))
    Traceback (most recent call last):
    ...
    ValidationError: [u'Not allowed filetype!']
    """
    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        import os
        from django.template.defaultfilters import filesizeformat
        data = super(ExtFileField, self).clean(*args, **kwargs)
        if data:
            filename = data.name
            file = data.file
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()
            if ext not in self.ext_whitelist:
                raise forms.ValidationError("Not allowed filetype!")
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
        elif not data and self.required:
            raise forms.ValidationError("Required file not found for %s" % self.label)
        return data


class OfflineContentloadForm(forms.Form):
    course_file = ExtFileField(label='course file', required=False, max_upload_size=5242880, ext_whitelist=(".xlsx",), content_types="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

class BulkCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('course_id','status', 'provider', 'thumbnail', 'instructors', 'tags', 'extractor_version', 'mode')

    title = forms.CharField(label='Course title', widget=forms.TextInput( attrs={ 'class': 'form-control'}))
    url = forms.URLField(label='Course url', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'cols': 60, 'rows': 3, 'class':'form-control'}), required=False)
    difficulty = forms.ChoiceField(label='Difficulty level', required=True, initial=DifficultyChoice.Beginner.value, choices=[(tag.value, tag.name) for tag in DifficultyChoice],
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    duration = forms.DurationField(label='Duration (hours)', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    instructor_name = forms.CharField(label='Instructor Name', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    instructor_company = forms.CharField(label='Instructor Company', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    instructor_web = forms.CharField(label='Instructor Website', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = MoneyField()

    max_students = forms.IntegerField(label='Max Students', required=False, min_value=2, initial=5, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    min_students = forms.IntegerField(label='Min Students', required=False, min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    session_count = forms.IntegerField(label='No of sessions', required=False, min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    prerequisites = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))