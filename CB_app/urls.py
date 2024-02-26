from django.urls import path
from .import views 



urlpatterns = [
    
    path('',views.Index_Page,name='Index_Page'),
    path('Search_Job/',views.Search_Job,name='Search_Job'),
    path('Signup/',views.Signup,name='Signup'),
    path('Profile/',views.Profile,name='Profile'),
    path('SignIn/',views.SignIn,name='SignIn'),
    path('Dashboard/',views.Dashboard,name='Dashboard'),
    path('SignOut/', views.SignOut, name='SignOut'),
    path('Profile_Page/',views.Profile_Page,name='Profile_Page'),
    path('Edit_Profile/',views.Edit_Profile,name='Edit_Profile'),
    path('Add_Job/',views.Add_Job,name='Add_Job'),
    path('Job_Detail/<int:job_id>/',views.Job_Detail,name='Job_Detail'),
    path('Edit_Job/<int:job_id>/',views.Edit_Job,name='Edit_Job'),
    path('Apply_Job/<int:job_id>/',views.Apply_Job,name='Apply_Job'),
    path('Applied_Candidates/<int:job_id>/',views.Applied_Candidates,name='Applied_Candidates'),
    path('View_Candidate_Profile/<int:candidate_id>/',views.View_Candidate_Profile,name='View_Candidate_Profile'),
    path('View_Application/<int:application_id>/',views.View_Application,name='View_Application'),
    path('Notifications/',views.Notifications,name='Notifications'),
    path('Reject_Application/<int:application_id>/',views.Reject_Application,name='Reject_Application')

    
]