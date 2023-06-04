from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    # To create employee
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        # non active users cannot log in
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)     # hashes password and saves to database
        user.save()
        return user

    # To create superuser (admin)
    def create_superuser(self, email, password, **extra_fields):
        # When admin creates will be permitted everything code below
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **extra_fields)


class Employee(AbstractBaseUser):
    # Required information fro employees
    username = None     # no need for username
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_number = models.CharField(
        max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    job_title = models.CharField(max_length=50, blank=True, null=True)
    work_location = models.CharField(max_length=50, blank=True, null=True)
    date_of_joining = models.DateField(auto_now_add=True)
    reporting_to = models.CharField(max_length=50, blank=True, null=True)
    linkedin_link = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='employee/', blank=True, null=True)

    # instead of username there will be field email that is unique
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.name


class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    apply_date = models.DateField(auto_now_add=True)
    nature_of_leave = models.CharField(max_length=50)
    first_day = models.DateField()
    last_day = models.DateField()
    number_of_days = models.IntegerField()
    is_approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.employee
