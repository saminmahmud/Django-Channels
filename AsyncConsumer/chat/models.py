from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Chat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

