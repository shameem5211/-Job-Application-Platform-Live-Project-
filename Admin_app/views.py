from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from CB_app.models import *

# Create your views here.

def Admin_Login(request):
    try:
        if request.user.is_authenticated:
            return redirect('Admin_Dashboard')
        
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username = username)
            if not user_obj.exists():
                messages.info(request,'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            user_obj = authenticate(username=username , password = password)
            
            if user_obj and user_obj.is_superuser:
                login(request,user_obj)
                return redirect('Admin_Dashboard')
            
            messages.info(request, 'Invalid Password')
            return redirect('Admin_Login')
        
        return render(request,'Admin/Login.html')
    
    except Exception as e:
        print(e)
                
                

@login_required(login_url='Admin_Login')
def Admin_Dashboard(request):
    employers_count = Userprofile.objects.filter(is_employer=True).count()

    # Get the count of candidates
    candidates_count = Userprofile.objects.filter(is_employer=False).count()

    # Get the count of jobs
    jobs_count = Job.objects.count()

    context = {
        'employers_count': employers_count,
        'candidates_count': candidates_count,
        'jobs_count': jobs_count
    }
    return render(request,'Admin/Dashboard.html',context)


def Signout(request):
    logout(request)
    return redirect('Admin_Login')


@login_required(login_url='Admin_Login')
def Employers(request):
    employers = Userprofile.objects.filter(is_employer=True)
    context = {
        'employers':employers
    }
    return render(request,'Admin/Employers.html',context)


@login_required(login_url='Admin_Login')
def Employer_Profile(request,employer_id):
    employer = get_object_or_404(Userprofile, id=employer_id, is_employer=True)
    context = {
        'employer':employer
    }
    return render(request,'Admin/Employer_Profile.html',context)



@login_required(login_url='Admin_Login')
def Candidates(request):
    candidates = Userprofile.objects.filter(is_employer=False)
    context = {
        'candidates':candidates
    }
    
    return render(request,'Admin/Candidates.html',context)


@login_required(login_url='Admin_Login')
def Candidate_Profile(request,candidate_id):
    candidate = get_object_or_404(Userprofile, id=candidate_id, is_employer=False)
    context = {
        'candidate':candidate
    }
    return render(request,'Admin/Candidate_Profile.html',context)


@login_required(login_url='Admin_Login')
def All_Jobs(request):
    jobs = Job.objects.all()
    return render(request, 'Admin/All_Jobs.html', {'jobs': jobs})


@login_required(login_url='Admin_Login')
def Job_details(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'Admin/Job_details.html', {'job': job})


@login_required(login_url='Admin_Login')
def applied_candidates(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'Admin/applied_candidates.html', {'job': job})


@login_required(login_url='Admin_Login')
def Application_View(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    return render(request, 'Admin/Application_View.html', {'application': application})


@login_required(login_url='Admin_Login')
def employer_jobs(request, employer_id):
    employer = User.objects.get(id=employer_id)
    jobs = Job.objects.filter(created_by=employer)
    return render(request, 'Admin/employer_jobs.html', {'jobs': jobs, 'employer': employer})


@login_required(login_url='Admin_Login')
def candidate_applications(request, candidate_id):
    # Get the candidate user object
    candidate = User.objects.get(id=candidate_id)

    # Get all applications submitted by the candidate
    applications = Application.objects.filter(created_by=candidate)

    context = {'applications': applications, 'candidate': candidate}
    return render(request, 'Admin/candidate_applications.html', context)