from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from.models import Student_info,Score,Performance
from .forms import LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import User
from dept.models import Dept, Subjects


# Create your views here.

def index(request):
    return render(request,'index.html')

def login1(request):
    return render(request,'login.html')

#Student Info
@login_required
def student(request):
    si=Student_info.objects.order_by('regno')
    return render(request,'student.html',{'si':si})
@login_required
def details(request,regno_id):
    det = Student_info.objects.get(id=regno_id)
    dept_id= det.dept_id
    dept= Dept.objects.get(id=dept_id)
    return render(request,'details.html',{'det':det,'dept':dept})

#performance
@login_required
def performance(request):
    p = Performance.objects.order_by('regno')
    return render(request,'performance.html',{'perf':p})
@login_required
def perf_details(request,regno_id):
    det = Performance.objects.get(id=regno_id)
    return render(request,'perf_details.html',{'perf_det':det})


#score
@login_required
def exam_report(request):
    e = Score.objects.order_by('regno')
    return render(request,'exam_report.html',{'sco':e})
@login_required
def sco_details(request,regno_id):
    det = Score.objects.get(id=regno_id)
    return render(request,'sco_details.html',{'sco_det':det})


#login
def stu_login_view(request):
    if(request.method=='POST'):
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('index1')
            else:
                return redirect('login_rej')
    else:
        form = LoginForm()
    return render(request,'stu_login.html',{'form':form})


#After student login

@login_required
def index1(request):
    regno=request.user.username
    user_profile=Student_info.objects.get(regno=regno)
    dept_id = user_profile.dept_id
    dept = Dept.objects.get(id=dept_id)
    return render(request,'index1.html',{'user_profile':user_profile,'dept':dept})

@login_required
def performance1(request):
    regno = request.user.username
    user_performance = Performance.objects.order_by('date').filter(regno=regno).reverse()

    paginator = Paginator(user_performance,2)
    page = request.GET.get('page')
    user_performance = paginator.get_page(page)

    return render(request,'performance1.html',{'user_performance': user_performance})

@login_required
def exam_report1(request):
    regno = request.user.username
    user_exam_report1 = Score.objects.filter(regno=regno)
    student=Student_info.objects.get(regno=regno)
    dept_id=student.dept_id
    year=student.year
    subjects=Subjects.objects.filter(dept_id=dept_id).filter(year=year)
    d=[]
    for i in subjects:
        d.append((i.sub_code,i.sub_name))

    '''
        for k in user_exam_report1:
        for i in subjects:
            if(i.sub_code=='s1'):
                d.append((k.s1,i.sub_name,k.exam_type))
            if (i.sub_code == 's2'):
                d.append((k.s2, i.sub_name,k.exam_type))
            if (i.sub_code == 's3'):
                d.append((k.s3, i.sub_name,k.exam_type))
            if (i.sub_code == 's4'):
                d.append((k.s4, i.sub_name,k.exam_type))
            if (i.sub_code == 's5'):
                d.append((k.s5, i.sub_name,k.exam_type))
            if (i.sub_code == 's6'):
                d.append((k.s6, i.sub_name,k.exam_type))
            if (i.sub_code == 's7'):
                d.append((k.s7, i.sub_name,k.exam_type))
            if (i.sub_code == 's8'):
                d.append((k.s8, i.sub_name,k.exam_type))
            if (i.sub_code == 's9'):
                d.append((k.s9, i.sub_name,k.exam_type))
            if (i.sub_code == 's10'):
                d.append((k.s10, i.sub_name,k.exam_type))
    
    '''
    paginator = Paginator(user_exam_report1, 1)
    page = request.GET.get('page')
    user_exam_report1 = paginator.get_page(page)

    return render(request,'exam_report1.html',{'subs':d,'user_exam_report1':user_exam_report1})

def logout_view(request):
    logout(request)
    return redirect('login1')

def login_rejected(request):
    return render(request,'login_rejected.html')