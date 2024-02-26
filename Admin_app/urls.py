from django.urls import path
from .import views 


urlpatterns = [
    
    path('',views.Admin_Login,name='Admin_Login'),
    path('Dashboard/',views.Admin_Dashboard,name='Admin_Dashboard'),
    path('Signout',views.Signout,name='Signout'),
    path('Employers/',views.Employers,name='Employers'),
    path('Employer_Profile/<int:employer_id>',views.Employer_Profile,name='Employer_Profile'),
    path('Candidates/',views.Candidates,name='Candidates'),
    path('Candidate_Profile/<int:candidate_id>',views.Candidate_Profile,name='Candidate_Profile'),
    path('All_Jobs/',views.All_Jobs,name='All_Jobs'),
    path('Job_details/<int:job_id>/',views.Job_details,name='Job_details'),
    path('applied_candidates/<int:job_id>/',views.applied_candidates,name='applied_candidates'),
    path('Application_View/<int:application_id>/',views.Application_View,name='Application_View'),
    path('employer_jobs/<int:employer_id>/',views.employer_jobs,name='employer_jobs'),
    path('candidate_applications/<int:candidate_id>/',views.candidate_applications,name='candidate_applications')
    
    
    
]