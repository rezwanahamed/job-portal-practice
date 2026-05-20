from django import forms
from job_portal_app.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'display_name', 'user_type', 'password1', 'password2']
    
class UserLoginForm(AuthenticationForm):
  pass

class RecruiterProfileForm(forms.ModelForm):
  class Meta:
    model = RecruiterProfileModel
    fields = '__all__'
    exclude = ['user']
    
class JobSeekerProfileForm(forms.ModelForm):
  class Meta:
    model = JobSeekerProfileModel
    fields = '__all__'
    exclude = ['user']
    
class JobPostForm(forms.ModelForm):
  class Meta:
    model = JobPostModel
    fields = '__all__'
    exclude = ['created_by', 'created_at']
    
    widgets = {
      'deadline' : forms.DateInput(attrs={'type': 'date'})
    }
    
class JobApplicationForm(forms.ModelForm):
  class Meta:
    model = JobApplicationModel
    fields = '__all__'
    exclude = ['applicant', 'applied_at']