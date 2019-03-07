from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from enum import Enum
from schedule.models import Event
from model_utils.fields import StatusField
from model_utils import Choices
from core.models import DifficultyChoice

class CourseStatus(Enum):
    Active = "Active"
    Complete = "Complete"
class Duration(Enum):
    Short = ('short', 2)
    Medium = ('medium', 5)
    Long = ('long', 12)
    ExtraLong = ('extraLong', 22)

LOGO_UPLOAD_TO = getattr(settings, 'LOGO_UPLOAD_TO', 'logo/')

class CourseProvider(models.Model):
    def GetLogoFilename(instance, filename):
        return LOGO_UPLOAD_TO + filename[-30:]

    name = models.CharField(max_length=256)
    status = models.SmallIntegerField()
    logo = models.ImageField(upload_to=GetLogoFilename)
    url=models.URLField()

    def __str__(self):
        return self.name

class Instructor(models.Model):
    def GetPhotoFilename(self, filename):
        return 'instructor/' + filename + "_" + str(self.id)

    name = models.CharField(max_length=256, unique=True)
    photo = models.URLField()
    url = models.URLField()

class CourseTag(models.Model):
    name = models.TextField()
    priority = models.PositiveSmallIntegerField(default = 0)

class Course(models.Model):
    def GetThumbFilename(self, filename):
        return 'courses/' + filename + "_" + str(self.id)

    def GetDifficultyName(self):
        return {
            1: "Beginner",
            2: "Intermediate",
            3: "Advanced"
        }.get(self.difficulty, "For Everyone")

    course_id = models.TextField()
    url = models.URLField()
    title = models.CharField(max_length=256)
    description = models.TextField(null=True)
    status = models.SmallIntegerField(default=1)
    difficulty = models.SmallIntegerField(choices=[(tag, tag.value) for tag in DifficultyChoice])
    duration = models.DurationField(null=True)
    provider = models.ForeignKey(CourseProvider, on_delete=models.PROTECT, null=True)
    thumbnail = models.URLField(null=True, default=None, blank=True)
    price = MoneyField(max_digits=8, decimal_places=2, default_currency='INR', null=True, default=None, blank=True)
    instructors = models.ManyToManyField(Instructor)
    tags = models.ManyToManyField(CourseTag)


class CourseUserRelation(models.Model):
    STATUS = Choices('Active', 'Complete')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    rating = models.SmallIntegerField(null=True)
    feedback = models.TextField(null=True)
    status = StatusField()

    @property
    def is_complete(self):
        return self.status == "Complete"


