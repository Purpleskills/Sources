from enum import Enum, IntEnum
from django.db import models

class DifficultyChoice(IntEnum):
    Beginner = 1
    Intermediate = 2
    Advanced = 3

class DurationChoice(Enum):
    All = 0
    CrashCourse = 1
    GiveMeAFeel = 2
    FullLength = 3

class Duration(Enum):
    Short = ('short', 2)
    Medium = ('medium', 5)
    Long = ('long', 12)
    ExtraLong = ('extraLong', 22)

class CourseStatus(Enum):
    Active = "Active"
    Complete = "Complete"

class CourseTag(models.Model):
    name = models.TextField()
    priority = models.PositiveSmallIntegerField(default=0)
