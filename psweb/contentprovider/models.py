from django.db import models
from core.models import DifficultyChoice, Duration

class UdemyCourseCategory(models.Model):
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

class UdemyCourseSubcategory(models.Model):
    category = models.ForeignKey(
         'UdemyCourseCategory',
          on_delete=models.CASCADE,
      )
    sort_order = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    title_cleaned = models.CharField(max_length=100)

class UdemyRawData(models.Model):
    category = models.ForeignKey(UdemyCourseCategory, on_delete=models.CASCADE)
    level = models.SmallIntegerField(choices=[(tag, tag.value) for tag in DifficultyChoice])
    duration = models.SmallIntegerField(choices=[(tag, tag.value[1]) for tag in Duration])
    page = models.SmallIntegerField(default=0)
    raw_data = models.TextField()
    retrieved = models.DateTimeField(auto_now_add=True)
    processed = models.DateTimeField(null=True, default=None, blank=True)

class CourseraRawData(models.Model):
    course_id = models.TextField()
    raw_data = models.TextField()
    retrieved = models.DateTimeField(auto_now_add=True)
    processed = models.DateTimeField(null=True, default=None, blank=True)

class LyndaRawData(models.Model):
    raw_data = models.BinaryField()
    retrieved = models.DateTimeField(auto_now_add=True)
    processed = models.DateTimeField(null=True, default=None, blank=True)
