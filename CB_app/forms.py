from django import forms
from .models import *


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['full_name','job_title', 'email', 'contact_number', 'location','qualification','profile_pic', 'cv']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'cv': forms.ClearableFileInput(attrs={'accept': 'application/pdf, application/msword'}),
        }
    
    
class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['company_name', 'company_category', 'email','company_address','contact_number','profile_pic']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
        
        
class AddJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title',   'company_name', 'company_address', 'company_zipcode', 'company_place', 'company_country', 'company_size','description']



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['content', 'experience']
        widgets = {
            'content': forms.Textarea(attrs={'rows': '4'}),  # Adjust the rows value as needed
            'experience': forms.Textarea(attrs={'rows': '4'}),  # Adjust the rows value as needed
        }
        labels = {
            'content':'Message'
        }