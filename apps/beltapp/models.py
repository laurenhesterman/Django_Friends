# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
#NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
  

  def my_validation(self, postdata):
    errors = []
    if len(postdata['first_name']) < 2:
        errors.append("Sorry, first name must be at least 3 characters.")
    if len(postdata['last_name']) < 2:
        errors.append("Sorry, last name must be at least 3 characters.")
    if not re.match(EMAIL_REGEX, postdata['email']):
        errors.append("Hmm, this doesn't look like a valid email. Please try again.")
    if len(postdata['password1']) < 8:
        errors.append("For your own security, your password cannot be less than 8 characters!")
    if postdata['password1'] != postdata['password2']:
        errors.append("Password and password confirmation must match!")
    #if postdata['email'] in User.objects
    if len(errors) == 0:
        hash_pw = bcrypt.hashpw(postdata['password1'].encode(), bcrypt.gensalt())
        new_user = self.create(
            first_name = postdata["first_name"],
            last_name = postdata["last_name"],
            email = postdata["email"],
            password = hash_pw  
        )
        print new_user

        return new_user
    return errors

  def my_validation_2(self, postdata):
    errors = []        
    if len(self.filter(email=postdata['email'])) > 0:           
        user = self.filter(email=postdata['email'])[0]
        if not bcrypt.checkpw(postdata['password'].encode(), user.password.encode()):
            errors.append('email/password incorrect')
    else:
        errors.append('email/password incorrect')

    if errors:
        return errors
    else:
        return user


  
  def add_friend(self, postdata):
    
    self.create(friendship_id=postdata['friend.id'], user_id=postdata['user.id'])
      #? how to get the friendship_id
    return
    

 
   

   
        
class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255, default="none")  
  friendships = models.ManyToManyField('self') 
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)  
  objects = UserManager()


  


  


