from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator,MinLengthValidator,MaxLengthValidator
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.postgres.fields import ArrayField

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512)
    logo = models.ImageField(upload_to='company/')
    domains = ArrayField(models.CharField(max_length=200), default=list)

    def __str__(self):
        return self.name

class Organization(MPTTModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='suborg')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class UserRole (models.Model):
    title = models.CharField(max_length=512)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

class CourseUser(AbstractUser):
    org = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, blank=True, default = None)
    gender = models.CharField(max_length=1, null=True)
    phone = models.CharField(
                max_length=15, validators=[
                    RegexValidator(regex=r'^\+?[\d]*', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
                    MinLengthValidator(9),
                    MaxLengthValidator(15),
                ], null=True, blank=True, default = None)
    role = models.ForeignKey (UserRole, on_delete=models.PROTECT)

