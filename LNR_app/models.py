from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors={}
        email_regex=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name']='First name must be at least 2 characters long'
        if len(postData['last_name'])<2:
            errors['last_name']='Last name must be at least 2 characters long'
        if not email_regex.match(postData['email']):
            errors['email']='Not a valid email address'
        if len(postData['username'])<2:
            errors['username']='Username not long enough, must be at least 2 charcters long'
        if len(postData['password'])<8:
            errors['password']='Password must be at least 8 characters long'
        if postData['password'] != postData['confirm_password']:
            errors['password']='Password and Confirm Password must match'
        return errors
    def login_validator(self, postData):
        errors={}
        checkUser = User.objects.filter(username = postData['logusername'])
        if len(checkUser)<1:
            errors['NoUser'] = 'Invalid username or password'
        elif not bcrypt.checkpw(postData['logpassword'].encode(), checkUser[0].password.encode()):
            errors['passwordNoMatch'] = 'Invalid username or password'
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    objects=UserManager()