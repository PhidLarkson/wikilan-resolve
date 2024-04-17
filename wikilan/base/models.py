from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver   
from django.contrib.auth.models import User
import uuid
import random

# Random avatar key
avatar_key = random.randint(1, 9)

# Create your models here.
# Abstract class for all user profiles
class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    avatar_id = models.IntegerField(default=avatar_key) 
    mail = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contributions = models.ManyToManyField('BookObject', through='Contribution')  # A user can contribute to many books
    contributions_count = models.IntegerField()

    # Returns the username of the user
    def __str__(self):
        return self.user.username
    # Meta class to make the class abstract: This means that the class cannot be instantiated
    class Meta:
        abstract = True

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance, created_at=instance.date_joined)
        except Exception as e:
            print(f"Error creating profile for user {instance.id}: {e}")

# avatar svg object
class Avatar(models.Model):
    id = models.AutoField(primary_key=True)
    avatar = models.ImageField(upload_to='uploads/avatars/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Abstract class for all book objects
class BookObject(models.Model):
    title = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=100)
    level = models.IntegerField(null=True)
    description = models.TextField()
    publisher = models.CharField('Profile', max_length=100, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # category = models.ForeignKey('Category', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', null=False)
    cover = models.ImageField(upload_to='uploads/', null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        abstract = True

# Staff: A user profile for staff
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Student: A user profile for students
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100)    
    department = models.CharField(max_length=100)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contributions_count = models.IntegerField()
    contributor = models.BooleanField(default=False)

# Category: A model for categories
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

# Concrete classes for book objects
class Book(BookObject):
    pass

# Concrete classes for textbook materials
class TextBook(BookObject):
    special_id = '#KT01'
    edition = models.IntegerField(blank=True, null=True)

# Concrete classes for past question materials
class PastQuestion(BookObject):
    special_id = models.CharField(max_length=100)
    year = models.IntegerField()
    course = models.CharField(max_length=100)
    publication_date = models.DateField()

# Concrete classes for journal materials
class Journal(BookObject):
    issue = models.IntegerField()
    volume = models.IntegerField()
    publication_date = models.DateField()

# Concrete classes for project materials
class Thesis(BookObject):
    special_id = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    publication_date = models.DateField()

# Concrete classes for Dissertation materials
class Dissertation(BookObject):
    special_id = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    publication_date = models.DateField()

# Concrete classes for student materials
class Report(BookObject):
    special_id = models.CharField(max_length=100)
    publication_date = models.DateField()

# Concrete classes for teacher materials
class TeacherMaterial(BookObject):
    special_id = models.CharField(max_length=100)
    publication_date = models.DateField()
