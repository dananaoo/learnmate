from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name    

class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) #null=True allowing to have empty field in database
    name=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True) #allows to create an empty room
    participants=models.ManyToManyField(User, related_name='participants', blank=True)
    updated=models.DateTimeField(auto_now=True) #date will be stored everytime when we save new changes
    created=models.DateTimeField(auto_now_add=True)  #initial time when room was created

    class Meta:
        ordering=['-updated', '-created']
        
    def __str__(self):
        return self.name
    

class Messages(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)  #if room will be deleted then messeages will be also deleted, we can use SET_Null to save messages in database
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True) 
    created=models.DateTimeField(auto_now_add=True) 
    class Meta:
        ordering=['-updated', '-created']
    
    def __str__(self):
        return self.body[0:50]