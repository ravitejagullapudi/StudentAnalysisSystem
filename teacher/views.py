from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django import forms
from .forms import LoginForm
from student.models import Student_info, Performance, Score
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserForm, ProfileForm
from .models import Teacher
from dept.models import Dept, Subjects
from django.core.paginator import Paginator
import datetime


# Create your views here.
@login_required
@staff_member_required
def index2(request):
    username = request.user.username
    user_profile = User.objects.get(username=username)
    user_id = request.user.id
    user_profile1 = Teacher.objects.get(user_id=user_id)

    dept_id = user_profile1.dept_id
    dept = Dept.objects.get(id=dept_id)

    teac_id = user_profile1.teac_id
    faculty = Subjects.objects.filter(teac_id=teac_id)
    return render(request, 'index2.html',
                  {'user_profile': user_profile, 'dept': dept, 'user_profile1': user_profile1, 'faculty': faculty,
                   'teac_id': teac_id})


# Posting of analysis

@login_required
@staff_member_required
def post_analysis(request):
    user_id = request.user.id
    user_profile1 = Teacher.objects.get(user_id=user_id)

    teac_id = user_profile1.teac_id
    faculty = Subjects.objects.filter(teac_id=teac_id)

    if (request.method == 'POST'):
        regno = request.POST['regno']

        try:
            student = Student_info.objects.get(regno=regno)
            subject = request.POST['subject']
            date = str(datetime.date.today())
            attendance = request.POST['attendance']
            listening_skills = request.POST['listening_skills']
            learning_attitude = request.POST['learning_attitude']
            assignment_submission = request.POST['assignment_submission']
            communication_skills = request.POST['communication_skills']
            collaboration_with_students = request.POST['collaboration_with_students']
            others_if_mention = request.POST['others_if_mention']
            try:
                valid1 = Performance.objects.get(regno=regno, teac_id=teac_id, sub_name=subject, date=date)
            except:
                n = Performance(regno=regno, sub_name=subject, date=date, teac_id=teac_id, attendance=attendance,
                                listening_skills=listening_skills \
                                , learning_attitude=learning_attitude, assignment_submission=assignment_submission \
                                , communication_skills=communication_skills \
                                , collaboration_with_students=collaboration_with_students,
                                others_if_mention=others_if_mention)

                n.save()
            else:
                valid1.attendance = attendance
                valid1.listening_skills = listening_skills
                valid1.learning_attitude = learning_attitude
                valid1.assignment_submission = assignment_submission
                valid1.communication_skills = communication_skills
                valid1.collaboration_with_students = collaboration_with_students
                valid1.others_if_mention = others_if_mention
                valid1.save()
            subject = 'Performance Update on '+date
            message = 'Performance of the Student \n Registration no:  '+regno+'\n'\
                        +'Name : '+student.name+'\n'+'Attendance'+attendance+'\n'+\
                    'Listening Skills: '+listening_skills+'\n'+'Learning Attitude: '+learning_attitude+'\n'+\
                'Assignment Submission: '+assignment_submission+'\n'+'Communication Skills: '+communication_skills+'\n'+\
                'Collaboration with Students:  '+collaboration_with_students+'\n'+'Other: '+others_if_mention
            from_mail = 'STUDENT ANALYSIS OF SRKREC'
            to_list = [student.student_email,student.parent_email]
            send_mail(subject, message, from_mail, to_list, fail_silently=True)
            return redirect('posting_analysis_success')

        except:
            error="Registered Number Not found"
            return render(request, 'post_analysis.html', {'faculty': faculty,'error':error})

    else:
        return render(request, 'post_analysis.html', {'faculty': faculty})


@login_required
@staff_member_required
def posting_analysis_success(request):
    return render(request, 'posting_analysis_success.html')


# Student Info
@login_required
def student(request):
    si = Student_info.objects.order_by('regno')
    return render(request, 'student.html', {'si': si})


@login_required
def details(request, regno_id):
    det = Student_info.objects.get(id=regno_id)
    return render(request, 'details.html', {'det': det})


# performance
@login_required
def performance(request):
    user_id = request.user.id
    user_profile1 = Teacher.objects.get(user_id=user_id)
    teac_id = user_profile1.teac_id
    p = Performance.objects.filter(teac_id=teac_id).order_by('regno')
    return render(request, 'performance.html', {'perf': p})



@login_required
@staff_member_required
def perf_details(request,regno,teac_id):
    s = Performance.objects.order_by('date').filter(regno=regno).filter(teac_id=teac_id).reverse()

    paginator = Paginator(s,1)
    page= request.GET.get('page')
    s1= paginator.get_page(page)

    return render(request, 'perf_details.html',{'s':s1})


# score
@login_required
@staff_member_required
def exam_report(request,sub_code):
    '''user_id = request.user.id
    user_profile1 = Teacher.objects.get(user_id=user_id)
    teac_id = user_profile1.teac_id
    '''
    s = Score.objects.values_list('regno',sub_code,'exam_type')

    print(s)
    return render(request, 'exam_report.html',{'s':list(s)})


@login_required
@staff_member_required
def exam_report_page(request):
    if (request.method == "POST"):
        sub_code = request.POST['subject']


        return redirect('exam_report',sub_code=sub_code)
    else:
        user_id = request.user.id
        teach = Teacher.objects.get(user_id=user_id)
        teach_id = teach.teac_id
        sub = Subjects.objects.filter(teac_id=teach_id)
        sub_list = []
        for i in sub:
            sub_list.append(i.sub_name)
        return render(request, 'exam_report_page.html',{'sub':sub})

@login_required
@staff_member_required
def perf_report_page(request):
    user_id = request.user.id
    teach = Teacher.objects.get(user_id=user_id)
    teach_id = teach.teac_id
    if (request.method == "POST"):
        regno = request.POST['regno']


        return redirect('perf_details',regno=regno,teac_id=teach_id)
    else:
        perf = Performance.objects.filter(teac_id=teach_id)
        perf_list = []
        for i in perf:
            perf_list.append(i.regno)
        perf_list=list(set(perf_list))
        return render(request, 'perf_report_page.html',{'perf':perf_list})



@login_required
def sco_details(request, regno_id):
    det = Score.objects.get(id=regno_id)
    return render(request, 'sco_details.html', {'sco_det': det})


def teac_login_view(request):
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index2')

            else:
                return redirect('login_rej')
    else:
        form = LoginForm()
    return render(request, 'teac_login.html', {'form': form})


def login_rejected(request):
    return render(request, 'login_rejected.html')


def teac_register(request):
    if (request.method == 'POST'):
        form = UserForm(request.POST)
        form1 = ProfileForm(request.POST)
        if form.is_valid() and form1.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            department = form1.cleaned_data['department']

            user1 = User.objects.all()
            dept = Dept.objects.get(dept_name=department)

            pr = Teacher(user_id=user.id,
                         name=form.cleaned_data['first_name'],
                         mobile=form1.cleaned_data['mobile'],
                         dept_id=dept.id,
                         teac_id=form1.cleaned_data['teac_id']

                         )
            pr.save()
            subject = 'THANK YOU FOR REGISTERING AS TEACHER YOU WILL BE PROVIDED STAFF STATUS SOON AFTER VERIFICATION'
            message = 'WELCOME TO STUDENT ANALYSIS SYSTEM OF SRKR \n' + \
                      'username=\t' + username + '\n password=\t' + password
            from_mail = 'STUDENT ANALYSIS OF SRKREC'
            to_list = [form.cleaned_data['email']]
            send_mail(subject, message, from_mail, to_list, fail_silently=True)
            if user.is_staff:
                login(request, user)
                return redirect('index2')
            else:
                login(request, user)
                return redirect('index')

    else:
        form = UserForm()
        form1 = ProfileForm()
    return render(request, 'teac_register.html', {'form': form, 'form1': form1})


def register(request):
    return render(request, 'register.html')


# the details of register no.and corresponding subject clicked in postreport page comes here

@login_required
@staff_member_required
def post_report(request, sub,reg,exam,year):
    if (request.method == 'POST'):
        sub_l = sub.split('-')
        sub_l = sub_l[:-1]
        subs=''
        for i in sub_l:
            sm = request.POST[i]
            k = Subjects.objects.get(sub_name=i)
            sub_c = k.sub_code
            '''s=Score()
            for attr,val in s.__dict__.iteritems():
                    if attr=sub_c:

            '''
            if sub_c == 's1':

                try:
                    n = Score.objects.get(regno=reg,exam_type=exam,year=year,)
                except Exception:
                    n = Score(regno=reg,exam_type=exam,year=year,s1=sm)
                    n.save()
                else:

                    n.s1 = sm
                    n.save()
            elif sub_c == 's2':
                try:
                    n = Score.objects.get(regno=reg,exam_type=exam,year=year)
                except Exception:
                    n = Score(regno=reg,exam_type=exam,year=year, s2=sm)
                    n.save()
                else:

                    n.s2 = sm
                    n.save()
            elif sub_c == 's3':
                try:
                    n = Score.objects.get(regno=reg,exam_type=exam,year=year)
                except Exception:
                    n = Score(regno=reg,exam_type=exam,year=year, s3=sm)
                    n.save()
                else:

                    n.s3 = sm
                    n.save()
            elif sub_c == 's4':
                try:
                    n = Score.objects.get(regno=reg,exam_type=exam,year=year)
                except Exception:
                    n = Score(regno=reg,exam_type=exam,year=year, s4=sm)
                    n.save()
                else:

                    n.s4 = sm
                    n.save()
            elif sub_c == 's5':
                try:
                    n = Score.objects.get(regno=reg,exam_type=exam,year=year)
                except Exception:
                    n = Score(regno=reg,exam_type=exam,year=year, s5=sm)
                    n.save()
                else:

                    n.s5 = sm
                    n.save()

            elif sub_c == 's6':
                try:
                    n = Score.objects.get(regno=reg,exam_type=exam,year=year)
                except Exception:
                    n = Score(regno=reg,exam_type=exam,year=year, s6=sm)
                    n.save()
                else:

                    n.s6 = sm
                    n.save()

            elif sub_c == 's7':
                try:
                    n = Score.objects.get(regno=reg,exam_type=exam,year=year)
                except Exception:
                    n = Score(regno=reg,exam_type=exam,year=year, s7=sm)
                    n.save()
                else:

                    n.s7 = sm
                    n.save()
            elif sub_c == 's8':
                try:
                    n = Score.objects.get(regno=reg,exam_type=exam,year=year)
                except Exception:
                    n = Score(regno=reg,exam_type=exam,year=year, s8=sm)
                    n.save()
                else:

                    n.s8 = sm
                    n.save()
            elif sub_c == 's9':
                try:
                    n = Score.objects.get(regno=reg,exam_type=exam,year=year)
                except Exception:
                    n = Score(regno=reg,exam_type=exam,year=year, s9=sm)
                    n.save()
                else:

                    n.s9 = sm
                    n.save()
            elif sub_c == 's10':
                try:
                    n = Score.objects.get(regno=reg,exam_type=exam,year=year)
                except Exception:
                    n = Score(regno=reg,exam_type=exam,year=year, s10=sm)
                    n.save()
                else:

                    n.s10 = sm
                    n.save()
            subs=subs+'\n'+i+':'+' '+str(sm)
        l = []
        print(subs)
        user_exam_report1 = Score.objects.filter(regno=reg)

        avg1 = 0
        c=0
        for i in user_exam_report1.values_list():
            if (i[2] == exam):
                print(i[2])
                for j in i[4:14]:
                    if j is not None:
                        avg1 = avg1 + j
                        c=c+1

        s1 = Score.objects.get(regno=reg, exam_type=exam)
        s1.avg = avg1/c
        s1.save()
        student=Student_info.objects.get(regno=reg)

        subject = 'Exam Report Update Of ' + exam
        message = 'Exam Report of the Student \n Registration no:  ' + str(reg) + '\n'+ \
                  subs
        from_mail = 'STUDENT ANALYSIS OF SRKREC'
        to_list = [student.student_email, student.parent_email]
        send_mail(subject, message, from_mail, to_list, fail_silently=False)

        return redirect('post_report_success')
    else:
        sub_l = sub.split('-')
        sub_l = sub_l[:-1]
        return render(request, 'post_report.html', {'sub': sub_l})


@login_required
@staff_member_required
def post_report_page(request):
    if (request.method == "POST"):
        regno = request.POST['regno']
        exam_type = request.POST['exam_type']
        try:
            s = Student_info.objects.get(regno=regno)
            dept_id = s.dept_id
            year = s.year
            user_id = request.user.id
            teach = Teacher.objects.get(user_id=user_id)
            teach_id = teach.teac_id
            sub = Subjects.objects.filter(teac_id=teach_id).filter(dept_id=dept_id).filter(year=year)
            sub_list = ''
            for i in sub:
                sub_list = sub_list + i.sub_name + '-'
            return redirect('post_report', sub=sub_list, reg=regno,exam=exam_type,year=year)
        except:
            error="Registered Number Not found"
            return render(request, 'post_report_page.html', {'error':error})

    else:
        return render(request, 'post_report_page.html')


@login_required
@staff_member_required
def post_report_success(request):
    return render(request, 'post_report_sucess.html')