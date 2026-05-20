from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  USER_TYPE_CHOICES = (
    ('recruiter', 'Recruiter'),
    ('job_seeker', 'Job Seeker'),
  )
  display_name = models.CharField(max_length=100, blank=True, null=True)
  user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='job_seeker')
  
class RecruiterProfileModel(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
  company_name = models.CharField(max_length=255, blank=True, null=True)
  company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
  
  
class JobSeekerProfileModel(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_seeker_profile')
  skill_set = models.TextField(blank=True, null=True)

class JobCategoryModel(models.Model):
  name = models.CharField(max_length=255)
  
  def __str__(self):
    return f'{self.name}'

class JobPostModel(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  category = models.ForeignKey(JobCategoryModel, on_delete=models.CASCADE, related_name='job_posts')
  created_at = models.DateTimeField(auto_now_add=True)
  number_of_positions = models.IntegerField(default=1)
  deadline = models.DateField()
  created_by = models.ForeignKey(RecruiterProfileModel, on_delete=models.CASCADE, related_name='posted_jobs')
  skill_set = models.TextField(blank=True, null=True)
  
class JobApplicationModel(models.Model):
  job_post = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='applications')
  applicant = models.ForeignKey(JobSeekerProfileModel, on_delete=models.CASCADE, related_name='applicant')
  applied_at = models.DateTimeField(auto_now_add=True)
