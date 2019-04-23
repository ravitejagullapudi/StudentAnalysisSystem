from django.db import models

# Create your models here.
class Student_info(models.Model):
    regno = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    dept_id=models.IntegerField()
    year = models.IntegerField()
    section = models.CharField(max_length=3)
    student_mobile = models.IntegerField()
    student_email = models.EmailField()
    parent_email = models.EmailField()
    parent_mobile = models.IntegerField()

    def __str__(self):
        return str(self.regno)

class Performance(models.Model):
    regno = models.IntegerField()
    attendance = models.IntegerField(default=111)
    date = models.DateTimeField()
    sub_name=models.CharField(max_length=15)
    teac_id=models.IntegerField()
    listening_skills = models.IntegerField()
    learning_attitude = models.IntegerField()
    assignment_submission = models.IntegerField()
    communication_skills = models.IntegerField()
    collaboration_with_students = models.IntegerField()
    others_if_mention = models.CharField(max_length=100,default='Nothing')
    def __str__(self):
        return str(self.regno)

class Score(models.Model):
    regno = models.IntegerField()
    exam_type= models.CharField(max_length=25)
    year=models.IntegerField()
    s1 = models.IntegerField()
    s2 = models.IntegerField()
    s3 = models.IntegerField()
    s4 = models.IntegerField()
    s5 = models.IntegerField()
    s6 = models.IntegerField()
    s7 = models.IntegerField()
    s8 = models.IntegerField()
    s9 = models.IntegerField()
    s10 = models.IntegerField()
    avg = models.IntegerField()

    def __str__(self):
        return str(self.regno)