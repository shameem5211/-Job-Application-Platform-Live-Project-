from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from .utilities import create_notification
from django.db.models import Q


# Create your views here.

def Index_Page(request):
    if request.user.is_authenticated:
        jobs = Job.objects.filter(status=Job.ACTIVE).order_by('-created_at')
    else:
        jobs = Job.objects.filter(status=Job.ACTIVE).order_by('-created_at')[:6]
    
    return render(request,'Index_Page.html',{'jobs':jobs})


def Search_Job(request):
    query = request.GET.get('q')

    if query:
        jobs = Job.objects.filter(Q(title__icontains=query) & Q(status=Job.ACTIVE)).order_by('-created_at')
    else:
        jobs = Job.objects.filter(status=Job.ACTIVE).order_by('-created_at')

    context = {
        'jobs': jobs,
        'query': query,
    }
    return render(request,'Index_Page.html',context)



def Signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            account_type = request.POST.get('account_type', 'jobseeker')

            if account_type == 'employer':
                userprofile = Userprofile.objects.create(user=user, is_employer=True)
                userprofile.save()
            else:
                userprofile = Userprofile.objects.create(user=user)
                userprofile.save()

            login(request, user)

            return redirect('Profile')
    else:
        form = UserCreationForm()

    return render(request, 'Signup.html', {'form': form})




def Profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        if user_profile.is_employer:
            form = EmployerProfileForm(request.POST, request.FILES)
        else:
            form = JobSeekerProfileForm(request.POST, request.FILES)

        if form.is_valid():
            # Process form data and update user profile
            update_user_profile(user_profile, form)

            return redirect('Profile_Page')  # Redirect to the profile page after successful form submission
    else:
        if user_profile.is_employer:
            form = EmployerProfileForm()
        else:
            form = JobSeekerProfileForm()

    return render(request, 'profile.html', {'form': form})




def update_user_profile(user_profile, form):
    # Update user profile fields based on the form
    # Save the form data to the user profile
    # You might want to customize this based on your user profile model

    if user_profile.is_employer:
        user_profile.company_name = form.cleaned_data.get('company_name', '')
        user_profile.email = form.cleaned_data.get('email', '')
        user_profile.company_category = form.cleaned_data.get('company_category', '')
        user_profile.company_address = form.cleaned_data.get('company_address', '')
        user_profile.contact_number = form.cleaned_data.get('contact_number', '')
        user_profile.profile_pic = form.cleaned_data.get('profile_pic', '')
    else:
        user_profile.full_name = form.cleaned_data.get('full_name', '')
        user_profile.job_title = form.cleaned_data.get('job_title', '')
        user_profile.email = form.cleaned_data.get('email', '')
        user_profile.contact_number = form.cleaned_data.get('contact_number', '')
        user_profile.location = form.cleaned_data.get('location', '')
        user_profile.cv = form.cleaned_data.get('cv', '')
        user_profile.qualification = form.cleaned_data.get('qualification', '')
        user_profile.profile_pic = form.cleaned_data.get('profile_pic', '')

    # Handle file uploads separately
    if 'cv' in form.files:
        user_profile.cv = form.files['cv']
    if 'profile_pic' in form.files:
        user_profile.profile_pic = form.files['profile_pic']

    user_profile.save()
    



def SignIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Check if the user is an employer
            try:
                user_profile = Userprofile.objects.get(user=user)
                if user_profile.is_employer:
                    return redirect('Dashboard')
            except Userprofile.DoesNotExist:
                pass

            # If not an employer, redirect to Index_Page
            return redirect('Index_Page')
    else:
        form = AuthenticationForm()

    return render(request, 'SignIn.html', {'form': form})


@login_required(login_url='SignIn')
def Dashboard(request):
    jobs = request.user.jobs.all()
    return render(request,'Dashboard.html',{'jobs':jobs})



def SignOut(request):
    logout(request)
    return redirect('Index_Page')


@login_required(login_url='SignIn')
def Profile_Page(request):
    user_profile = request.user.userprofile
    
    if user_profile.is_employer:
        # If the user is an employer, pass the employer's data
        data = {
            'user_type': 'employer',
            'company_name': user_profile.company_name,
            'email': user_profile.email,
            'company_category': user_profile.company_category,
            'company_address': user_profile.company_address,
            'contact_number': user_profile.contact_number,
            'profile_pic': user_profile.profile_pic.url if user_profile.profile_pic else None,
            # Add other employer-specific data as needed
        }
    else:
        # If the user is a job seeker, pass the job seeker's data
        data = {
            'user_type': 'job_seeker',
            'full_name': user_profile.full_name,
            'job_title':user_profile.job_title,
            'email': user_profile.email,
            'contact_number': user_profile.contact_number,
            'location': user_profile.location,
            'qualification': user_profile.qualification,
            'cv': user_profile.cv.url if user_profile.cv else None,
            'profile_pic': user_profile.profile_pic.url if user_profile.profile_pic else None,
            # Add other job seeker-specific data as needed
        }

    return render(request, 'profile_page.html', data)
        
        
        
@login_required(login_url='SignIn')      
def Edit_Profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        if user_profile.is_employer:
            form = EmployerProfileForm(request.POST, request.FILES,instance=user_profile)
        else:
            form = JobSeekerProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect('Profile_Page')
    else:
        if user_profile.is_employer:
            form = EmployerProfileForm(instance=user_profile)
        else:
            form = JobSeekerProfileForm(instance=user_profile)

    return render(request, 'Edit_Profile.html', {'form': form})





@login_required(login_url='SignIn')
def Add_Job(request):
    if request.method == 'POST':
        form = AddJobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()

            return redirect('Dashboard')
    else:
        form = AddJobForm()
    
    return render(request, 'Add_Job.html', {'form': form})


@login_required(login_url='SignIn')
def Job_Detail(request, job_id):
    job = Job.objects.get(pk=job_id)
    user = request.user

    # Check if the user has already applied for the job
    has_applied = job.applications.filter(created_by=user).exists()

    context = {'job': job, 'has_applied': has_applied}
    
    return render(request, 'Job_Detail.html',context)


@login_required(login_url='SignIn')
def Applied_Candidates(request,job_id):
    job = Job.objects.get(pk=job_id)
    
    return render(request, 'Applied_Candidates.html', {'job': job})


@login_required(login_url='SignIn')
def Edit_Job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, created_by=request.user)

    if request.method == 'POST':
        form = AddJobForm(request.POST, instance=job)

        if form.is_valid():
            job = form.save(commit=False)
            job.status = request.POST.get('status')
            job.save()

            return redirect('Job_Detail', job_id=job.id)
    else:
        form = AddJobForm(instance=job)

    return render(request, 'Edit_Job.html', {'job': job, 'form': form})




@login_required(login_url='SignIn')
def Apply_Job(request, job_id):
    job = Job.objects.get(pk=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.created_by = request.user
            application.save()

            create_notification(request, job.created_by, 'application', extra_id=application.id) 

            return redirect('Dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'Apply_Job.html', {'form': form, 'job': job})




@login_required(login_url='SignIn')
def View_Application(request, application_id):
    if request.user.userprofile.is_employer:
        application = get_object_or_404(Application, pk=application_id, job__created_by=request.user)
    else:
        application = get_object_or_404(Application, pk=application_id, created_by=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            conversationmessage = ConversationMessage.objects.create(application=application, content=content, created_by=request.user)

            create_notification(request, application.created_by, 'message', extra_id=application.id)

            return redirect('View_Application', application_id=application_id)
        
    
    return render(request, 'View_Application.html', {'application': application})


@login_required(login_url='SignIn')
def View_Candidate_Profile(request, candidate_id):
    candidate = get_object_or_404(User, pk=candidate_id)
    candidate_profile = Userprofile.objects.get(user=candidate)
    
    return render(request, 'View_Candidate_Profile.html', {'candidate': candidate, 'candidate_profile': candidate_profile})



@login_required(login_url='SignIn')
def Notifications(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)
    extra_id = request.GET.get('extra_id', 0)
    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

        context = {}
        
        if notification.notification_type == Notification.MESSAGE:
            return redirect('View_Application', application_id=notification.extra_id)
        elif notification.notification_type == Notification.APPLICATION:
            return redirect('View_Application', application_id=notification.extra_id)
        elif notification.notification_type == Notification.REJECTED_APPLICATION:
            return redirect('View_Application', application_id=notification.extra_id)
    
    return render(request, 'Notifications.html')



@login_required(login_url='SignIn')
def Reject_Application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    if request.method == 'POST':
        # Check if the 'Reject' button is clicked
        if 'reject_application' in request.POST:
            # Set the application status to 'rejected'
            application.status = Application.REJECTED
            application.save()
            
            create_notification(request, application.created_by, 'rejected_application', extra_id=application.id)

            return redirect('Dashboard')
        
        
        

    