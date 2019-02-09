from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from enum import Enum
from schedule.models import Event

class DifficultyChoice(Enum):
    Beginner = "Beginner"
    Intermediate = "Intermediate"
    Difficult = "Difficult"
    VeryDifficult = "Very Difficult"
    All = "All"

LOGO_UPLOAD_TO = getattr(settings, 'LOGO_UPLOAD_TO', 'logo/')

class CourseCategory(models.Model):
    name = models.CharField(max_length=256)
    status = models.SmallIntegerField()

    def __str__(self):
        return self.name

class CourseSubCategory(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    status = models.SmallIntegerField()

    def __str__(self):
        return self.name


class CourseProvider(models.Model):
    def GetLogoFilename(instance, filename):
        return LOGO_UPLOAD_TO + filename[-30:]

    name = models.CharField(max_length=256)
    status = models.SmallIntegerField()
    logo = models.ImageField(upload_to=GetLogoFilename)

    def __str__(self):
        return self.name

class Instructor(models.Model):
    def GetPhotoFilename(self, filename):
        return 'instructor/' + filename + "_" + str(self.id)

    name = models.CharField(max_length=256)
    photo = models.ImageField(upload_to=GetPhotoFilename, null=True, default=None, blank=True)


class Course(models.Model):
    def GetThumbFilename(self, filename):
        return 'courses/' + filename + "_" + str(self.id)

    url = models.URLField()
    title = models.CharField(max_length=256)
    description = models.TextField(null=True)
    status = models.SmallIntegerField(null=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.PROTECT, null=True)
    subcategory = models.ForeignKey(CourseSubCategory, on_delete=models.PROTECT, null=True)
    difficulty = models.CharField( max_length=16, choices=[(tag, tag.value) for tag in DifficultyChoice], null=True)
    duration = models.DurationField(null=True)
    provider = models.ForeignKey(CourseProvider, on_delete=models.PROTECT, null=True)
    thumbnail = models.ImageField(upload_to=GetThumbFilename, null=True, default=None, blank=True)
    price = MoneyField(max_digits=8, decimal_places=2, default_currency='INR', null=True, default=None, blank=True)
    instructors = models.ManyToManyField(Instructor)


class CourseUserRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    rating = models.SmallIntegerField(null=True)
    feedback = models.TextField(null=True)


