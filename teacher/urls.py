from django.urls import path
from . import views
urlpatterns = [
    path('post_analysis/', views.post_analysis, name='post_analysis'),
    path('posting_analysis_success/', views.posting_analysis_success, name='posting_analysis_success'),
    path('student/', views.student, name='student'),
    path('performance/', views.performance, name='performance'),
    path('exam_report/<str:sub_code>/', views.exam_report, name='exam_report'),
    path('exam_report_page/', views.exam_report_page, name='exam_report_page'),
    path('details/<int:regno_id>',views.details,name='details'),
    path('perf_details/<int:regno>/<int:teac_id>/',views.perf_details,name='perf_details'),
    path('sco_details/<int:regno_id>',views.sco_details,name='sco_details'),
    path('teac_register/',views.teac_register,name='teac_register'),
    path('teac_login/',views.teac_login_view,name='teac_login'),
    path('login_rej/',views.login_rejected,name='login_rej'),
    path('teac_info/',views.index2,name='index2'),
    path('register/', views.register, name='register'),
    path('post_report/<str:sub>/<int:reg>/<str:exam>/<int:year>/',views.post_report, name='post_report'),
    path('post_report_success/',views.post_report_success, name='post_report_success'),
    path('post_report_page/', views.post_report_page, name='post_report_page'),
    path('perf_report_page/', views.perf_report_page, name='perf_report_page'),

]
