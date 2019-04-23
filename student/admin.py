from django.contrib import admin
from .models import Student_info,Performance,Score
# Register your models here.
admin.site.register(Student_info)
admin.site.register(Performance)
admin.site.register(Score)