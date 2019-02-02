from django.db import models
from django.conf import settings
from enum import Enum

class DifficultyChoice(Enum):
    Beginner = "Beginner"
    Intermediate = "Intermediate"
    Difficult = "Difficult"
    VeryDifficult = "Very Difficult"

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

class Course(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=256)
    description = models.TextField(null=True)
    status = models.SmallIntegerField(null=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.PROTECT, null=True)
    subcategory = models.ForeignKey(CourseSubCategory, on_delete=models.PROTECT, null=True)
    difficulty = models.CharField( max_length=16, choices=[(tag, tag.value) for tag in DifficultyChoice], null=True)
    duration = models.DurationField(null=True)
    provider = models.ForeignKey(CourseProvider, on_delete=models.PROTECT, null=True)


  


