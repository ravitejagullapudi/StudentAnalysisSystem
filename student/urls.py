from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('student/', views.student, name='student'),
    path('performance/', views.performance, name='performance'),
    path('exam_report/', views.exam_report, name='exam_report'),
    path('details/<int:regno_id>',views.details,name='details'),
    path('perf_details/<int:regno_id>',views.perf_details,name='perf_details'),
    path('sco_details/<int:regno_id>',views.sco_details,name='sco_details'),
    path('stu_login/',views.stu_login_view,name='stu_login'),
    path('login1/',views.login1,name='login1'),
    path('st/',views.index1,name='index1'),
    path('sco/',views.exam_report1,name='exam_report1'),
    path('per/',views.performance1,name='performance1'),
    path('logout/', views.logout_view, name='logout'),
    path('login_rej/',views.login_rejected,name='login_rej'),
]
