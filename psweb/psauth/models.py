from django.db import models
from django.core.validators import RegexValidator,MinLengthValidator,MaxLengthValidator
from django.conf import settings
from django.contrib.auth.models import Group, AbstractUser


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512)
    logo = models.ImageField(upload_to='company/')

    def __str__(self):
        return self.name

class Department(models.Model):
   id = models.AutoField(primary_key=True)
   name = models.CharField(max_length=512)

class CourseUser(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    gender = models.CharField(max_length=1, null=True)
    phone = models.CharField(
                max_length=15, validators=[
                    RegexValidator(regex=r'^\+?[\d]*', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
                    MinLengthValidator(9),
                    MaxLengthValidator(15),
                ], null=True, blank=True, default = None)
