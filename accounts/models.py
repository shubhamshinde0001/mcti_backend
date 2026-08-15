from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOISES = (
        ('HEAD', 'Head Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
        ('PARENT', 'Parent'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOISES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username
    
'''
class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    joining_date = models.DateField()
    def __str__(self):
        return self.user.username
'''

class Teacher(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    designation = models.CharField(
        max_length=100
    )

    specialization = models.CharField(
        max_length=100
    )

    qualification = models.CharField(
        max_length=200
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    joining_date = models.DateField()

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username


class Parent(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='parent_profile'
    )

    father_name = models.CharField(
        max_length=150
    )

    mother_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    mobile = models.CharField(
        max_length=15
    )

    alternate_mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    occupation = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    address = models.TextField()

    status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username


'''
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    def __str__(self):
        return self.user.username
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.DateField()
    address = models.TextField()
    def __str__(self):
        return self.user.username
'''

class Student(models.Model):

    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    parent = models.ForeignKey(
        Parent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    student_id = models.CharField(
        max_length=50,
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    mobile = models.CharField(
        max_length=15
    )

    address = models.TextField()

    admission_date = models.DateField()

    profile_image = models.ImageField(
        upload_to='students/',
        blank=True,
        null=True
    )

    status = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student_id} - {self.first_name}"
