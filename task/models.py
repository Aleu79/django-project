from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TaskCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class TaskTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Tag {self.name}"



class TaskStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class TaskPriority(models.Model):
    level = models.IntegerField()

    def __str__(self):
        return f"Prioridad {self.level}"
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateField(null=True, blank=True) 
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    banner_color = models.CharField(max_length=7, default='#000000')
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(TaskTag, blank=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, default=1)
    priority = models.ForeignKey(TaskPriority, on_delete=models.CASCADE, default=1)
    is_personal = models.BooleanField(default=False) 

    def __str__(self):
        return self.title + '- por ' + self.user.username


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False) 

    def __str__(self):
        return f"Comentario por {self.user.username} - {self.created}"


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)  
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.created}"




class TaskNotification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.user.username} sobre {self.task.title}"

class TaskReminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    message = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Recordatorio para {self.task.title} a las {self.reminder_time}"
