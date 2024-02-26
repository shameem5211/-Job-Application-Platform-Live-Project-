from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_employer = models.BooleanField(default=False)
    
    EDUCATION_CHOICES = [
        ('+2', '+2'),('Diploma', 'Diploma'),
        ('BA ', 'BA'),('BSc','BSc'),('BCom','BCom'),('BCA','BCA'),
        ('BBA','BBA'),('B.Tech','B.Tech'),('B.Ed','B.Ed'),('BFA','BFA'),
        
        ('MA', 'MA'),('MSc','MSc'),('Mcom','Mcom'),('MCA','MCA'),
        ('MBA','MBA'),('M.Tech','M.Tech'),('M.Ed','M.Ed'),('MFA','MFA'),
        ('Ph.D', 'Ph.D')
    ]
    
    # Additional fields for job seekers
    full_name = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=50,blank=True)
    email = models.EmailField(blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=20, choices=EDUCATION_CHOICES,blank=True)
    cv = models.FileField(upload_to='cv/', blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/',blank=True)
    
    
    # Additional fields for employers
    company_name = models.CharField(max_length=100, blank=True)
    company_category = models.CharField(max_length=100, blank=True)
    company_address = models.CharField(max_length=200, blank=True)


User.userprofile = property(lambda u:Userprofile.objects.get_or_create(user=u)[0])





class Job(models.Model):
    SIZE_1_9 = 'size_1-9'
    SIZE_10_49 = 'size_10-49'
    SIZE_50_99 = 'size_50-99'
    SIZE_100 = 'size_100'

    CHOICES_SIZE = (
        (SIZE_1_9, '1-9'),
        (SIZE_10_49, '10-49'),
        (SIZE_50_99, '50-99'),
        (SIZE_100, '100+'),
    )

    ACTIVE = 'active'
    EMPLOYED = 'employed'
    ARCHIVED = 'archived'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (EMPLOYED, 'Employed'),
        (ARCHIVED, 'Archived')
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    company_zipcode = models.CharField(max_length=255, blank=True, null=True)
    company_place = models.CharField(max_length=255, blank=True, null=True)
    company_country = models.CharField(max_length=255, blank=True, null=True)
    company_size = models.CharField(max_length=20, choices=CHOICES_SIZE, default=SIZE_1_9)

    created_by = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=ACTIVE)

    def __str__(self):
        return self.title




class Application(models.Model):
    
    PENDING = 'pending'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
    ]
    
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    content = models.TextField()
    experience = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    created_by = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_rejected(self):
        return self.status == self.REJECTED



class ConversationMessage(models.Model):
    application = models.ForeignKey(Application, related_name='conversationmessages', on_delete=models.CASCADE)
    content = models.TextField()

    created_by = models.ForeignKey(User, related_name='conversationmessages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']



    
    
class Notification(models.Model):
    MESSAGE = 'message'
    APPLICATION = 'application'
    REJECTED_APPLICATION = 'rejected_application'

    CHOICES = (
        (MESSAGE, 'Message'),
        (APPLICATION, 'Application'),
        (REJECTED_APPLICATION, 'Rejected Application')
    )

    to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)
    extra_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creatednotifications', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
    