from django.db import models

# Create your models here.
class Teacher(models.Model):
    user_id=models.IntegerField()
    teac_id=models.IntegerField()
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    dept_id = models.IntegerField()
    def __str__(self):
        return self.teac_id
