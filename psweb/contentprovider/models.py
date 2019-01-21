from django.db import models

class UdemyUser(models.Model):
  birth_date = models.DateField()
  created = models.DateField()
  has_activated = models.NullBooleanField()
  image_100X100 = models.CharField(max_length=1024)
  image_125_H = models.CharField(max_length=1024)
  image_200_H = models.CharField(max_length=1024)
  image_50X50 = models.CharField(max_length=1024)
  image_75X75 = models.CharField(max_length=1024)
  is_disabled = models.NullBooleanField()
  is_followed = models.NullBooleanField()
  is_generated = models.NullBooleanField()
  job_title = models.CharField(max_length=100)
  locale = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  num_subscribed_courses  = models.IntegerField()
  surname = models.CharField(max_length=100)
  time_zone = models.CharField(max_length=100)
  title = models.CharField(max_length=100)
  url = models.CharField(max_length=1024)
  url_title  = models.CharField(max_length=100)


class UdemyInstructedBy(models.Model):
   instructors = models.ForeignKey(UdemyUser, on_delete=models.CASCADE, related_name='instructors')
   course = models.ForeignKey('UdemyCourse', on_delete=models.CASCADE, related_name='course')

class UdemyCourse(models.Model):
    archive_time = models.TimeField()
    avg_rating = models.FloatField()
    completion_ratio = models.FloatField()
    created = models.DateField()
    description = models.TextField()
    favorite_time = models.TimeField()
    headline = models.TextField()
    image_100X100 = models.CharField(max_length=1024)
    image_125_H = models.CharField(max_length=1024)
    image_200_H = models.CharField(max_length=1024)
    image_240X135 = models.CharField(max_length=1024)
    image_304X171 = models.CharField(max_length=1024)
    image_48X27 = models.CharField(max_length=1024)
    image_50X50 = models.CharField(max_length=1024)
    image_75X75 = models.CharField(max_length=1024)
    image_96X54 = models.CharField(max_length=1024)
    is_in_any_ufb_content_collection = models.NullBooleanField()
    is_paid = models.NullBooleanField()
    is_private = models.NullBooleanField()
    is_whitelisted = models.NullBooleanField()
    locale = models.CharField(max_length=100)
    num_lectures = models.IntegerField()
    num_quizzes = models.IntegerField()
    num_reviews = models.IntegerField()
    num_subscribers = models.IntegerField()
    price = models.FloatField()
    primary_category = models.ForeignKey(
        'UdemyCourseCategory',
        on_delete=models.CASCADE,
        related_name='primary_category',
    )
    primary_subcategory =  models.ForeignKey(
          'UdemyCourseCategory',
          on_delete=models.CASCADE,
	  related_name='primary_subcategory',
    )
    status_label = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    url = models.CharField(max_length=1024)
  #  visible_instructors = models.ManyToManyField(
  #      UdemyUser,
  #      through='UdemyInstructedBy',
  #      through_fields=('instructors'),
  #  )



class UdemyCourseCategory(models.Model):
    sort_order = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    title_cleaned = models.CharField(max_length=100)

class UdemyCourseSubcategory(models.Model):
    category = models.ForeignKey(
         'UdemyCourseCategory',
          on_delete=models.CASCADE,
      )
    sort_order = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    title_cleaned = models.CharField(max_length=100)