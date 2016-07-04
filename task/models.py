from django.db import models
from django.contrib.auth.models import User



class task(models.Model):
    author = models.ForeignKey(User)
    task_name = models.CharField(max_length=200)
    task_description = models.TextField()
    task_is_done = models.BooleanField(default=False)

    def edit_name(self, new_name):
        self.task_name =new_name

    def __str__(self):
        return self.task_name
