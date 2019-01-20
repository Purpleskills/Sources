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

class CourseSubCategory(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    status = models.SmallIntegerField()

class CourseProvider(models.Model):
    def GetLogoFilename(instance, filename):
        return LOGO_UPLOAD_TO + filename[-30:]

    name = models.CharField(max_length=256)
    status = models.SmallIntegerField()
    logo = models.ImageField(upload_to=GetLogoFilename)

class Course(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=256)
    description = models.TextField()
    status = models.SmallIntegerField()
    category = models.ForeignKey(CourseCategory, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(CourseSubCategory, on_delete=models.PROTECT)
    difficulty = models.CharField( max_length=16, choices=[(tag, tag.value) for tag in DifficultyChoice])
    duration = models.DurationField()
    provider = models.ForeignKey(CourseProvider, on_delete=models.PROTECT)

