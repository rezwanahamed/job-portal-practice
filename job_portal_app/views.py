from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from job_portal_app.models import *
from job_portal_app.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def userRegistration(req):
  if req.method == 'POST':
    form = UserRegistrationForm(req.POST)
    if form.is_valid():
      form.save()
      return redirect('login_page')
    
  registration_form = UserRegistrationForm()
  context = {
    'form': registration_form,
    'form_button': 'Register',
    'form_title': 'User Registration'
  }
    
  return render(req, 'master/base_form.html', context)

def userLogin(req):
  if req.method == "POST":
    form = UserLoginForm(req, req.POST)
    if form.is_valid():
      user = form.get_user()
      login(req, user)
      return redirect('dashboard_page')
    
  login_form = UserLoginForm()
  context = {
    'form': login_form,
    'form_button': 'Login', 
    'form_title': 'User Login'
  }
  return render(req, 'master/base_form.html', context)

def userLogout(req):
  logout(req)
  return redirect('login_page')

# update profile view
@login_required
def createProfile(req):
  current_user = req.user
  
  if current_user.user_type == 'recruiter':
    profile_form = RecruiterProfileForm(req.POST, req.FILES)
  
  else:
    profile_form = JobSeekerProfileForm(req.POST, req.FILES)

  if req.method == 'POST':
    if profile_form.is_valid():
      instance = profile_form.save(commit=False)
      instance.user = current_user
      instance.save()
      return redirect('dashboard_page')

  context = {
    'form': profile_form,
    'form_button': 'Create Profile',
    'form_title': 'Create Your Profile'
  }
  return render(req, 'master/base_form.html', context)

@login_required
def updateProfile(req):
  current_user = req.user
  
  if current_user.user_type == 'recruiter':
    profile_instance  = current_user.recruiter_profile
    if req.method == 'POST':
      profile_update_form = RecruiterProfileForm(req.POST, req.FILES, instance=profile_instance)
    else:
      profile_update_form = RecruiterProfileForm(instance=profile_instance)
  
  else:
    profile_instance = current_user.job_seeker_profile
    if req.method == 'POST':
      profile_update_form = JobSeekerProfileForm(req.POST, req.FILES, instance=profile_instance)
    else:
      profile_update_form = JobSeekerProfileForm(instance=profile_instance)

  if req.method == 'POST':
    if profile_update_form.is_valid():
      instance = profile_update_form.save(commit=False)
      instance.user = current_user
      instance.save()
      return redirect('update_profile_page')

  context = {
    'form': profile_update_form,
    'form_button': 'Update Profile',
    'form_title': 'Update Your Profile'
  }
  return render(req, 'master/base_form.html', context)  


# job post creation view
@login_required
def createJobPost(req):
  if req.user.user_type != 'recruiter':
    logout(req)
    return redirect('login_page')
    
  if not hasattr(req.user, 'recruiter_profile'):
    return redirect('update_profile_page')

  if req.method == 'POST':
    job_post_form = JobPostForm(req.POST)
    if job_post_form.is_valid():
      instance = job_post_form.save(commit=False)
      instance.created_by = req.user.recruiter_profile
      instance.save()
      return redirect('dashboard_page')
    
  job_post_form = JobPostForm()
  context = {
    'form': job_post_form,
    'form_button': 'Create Job Post',
    'form_title': 'Create a New Job Post'
  }
  return render(req, 'master/base_form.html', context)

#apply job post view for job seeker
@login_required
def applyJobPost(req, job_post_id):
  if req.user.user_type != 'job_seeker':
    logout(req)
    return redirect('login_page')
  
  # check user have already applied for the job
  if JobApplicationModel.objects.filter(job_post = job_post_id, applicant = req.user.job_seeker_profile).exists():
    messages.error(req,"You have already applied in the job")
    return redirect('dashboard_page')
    
  # get job details
  job_details_instance = JobPostModel.objects.get(id=job_post_id)
  JobApplicationModel.objects.create(
    job_post = job_details_instance,
    applicant = req.user.job_seeker_profile
  )
  return redirect('applied_jobs_page')
  

@login_required
def updateJobPost(req, job_post_id):
  if req.user.user_type != 'recruiter':
    logout(req)
    return redirect('login_page')
  
  job_post_instance = JobPostModel.objects.get(id=job_post_id)
  
  if req.method == 'POST':
    job_post_update_form = JobPostForm(req.POST, instance=job_post_instance)
    if job_post_update_form.is_valid():
      job_post_update_form.save()
      return redirect('dashboard_page')
    
  job_post_update_form = JobPostForm(instance=job_post_instance)
  context = {
    'form': job_post_update_form,
    'form_button': 'Update Job Post',
    'form_title': f'Update {job_post_instance.title} Position'
  }
  return render(req, 'master/base_form.html', context)

@login_required
def deleteJobPost(req, job_post_id):
  if req.user.user_type != 'recruiter':
    logout(req)
    return redirect('login_page')
  
  job_post_instance = JobPostModel.objects.get(id=job_post_id)
  job_post_instance.delete()
  return redirect('dashboard_page')

# applied job list view for job seeker
@login_required
def appliedJobs(req):
  if req.user.user_type != 'job_seeker':
    logout(req)
    return redirect('login_page')
  applied_jobs = JobApplicationModel.objects.filter(applicant=req.user.job_seeker_profile)
  context = {
    'applied_jobs': applied_jobs
  }
  return render(req, 'applied_jobs.html', context)

# recommended jobs view for job seeker
@login_required
def recommendedJobs(req):
  if req.user.user_type != 'job_seeker':
    logout(req)
    return redirect('login_page')
  
  job_data = JobPostModel.objects.none()  
  skill_set = req.user.job_seeker_profile.skill_set
  for skill in skill_set.split(','):
    cleaned_skill = skill.strip()
    
    job_data |= JobPostModel.objects.filter(skill_set__icontains = cleaned_skill)
    
  context = {
    'jobs': job_data
  }
  return render(req, 'recommended_jobs.html', context)

# dashboard view (show all jobs to job seeker, son seeker can search job, show posted jobs to recruiter)
@login_required
def dashboard(req):
  query_param = req.GET.get('search_param', '').strip()
  
  if req.user.user_type == 'job_seeker':
    if not hasattr(req.user, 'job_seeker_profile'):
      return redirect('create_profile_page')
    
    all_jobs = JobPostModel.objects.all()
    
    # Apply search filter if query_param is not empty
    if query_param:
      all_jobs = all_jobs.filter(
        Q(title__icontains=query_param) | 
        Q(description__icontains=query_param) | 
        Q(skill_set__icontains=query_param) | 
        Q(category__name__icontains=query_param)
      )
    
    context = {
      'jobs': all_jobs,
      'search_param': query_param
    }
    return render(req, 'dashboard.html', context)
  
  else:
    if not hasattr(req.user, 'recruiter_profile'):
      return redirect('create_profile_page')
    
    try:
      posted_jobs = JobPostModel.objects.filter(created_by=req.user.recruiter_profile)
    except:
      posted_jobs = None
    
    context = {
      'jobs': posted_jobs
    }
    return render(req, 'dashboard.html', context)

# job details view
@login_required
def jobDetails(req, job_post_id):
  try:
    job_details = JobPostModel.objects.get(id=job_post_id)
    context = {
      'job_details': job_details
    }
    return render(req, 'job_details.html', context)
  except JobPostModel.DoesNotExist:
    return redirect('dashboard_page')


@login_required
def applicant_list(req, job_post_id):
  # Only recruiters can view applicants
  if req.user.user_type != 'recruiter':
    logout(req)
    return redirect('login_page')
  
  if not hasattr(req.user, 'recruiter_profile'):
    return redirect('create_profile_page')
  
  try:
    # Get the job post and verify recruiter owns it
    job_post = JobPostModel.objects.get(id=job_post_id)
    if job_post.created_by != req.user.recruiter_profile:
      return redirect('dashboard_page')
    
    # Get all applicants for this job
    applicants = JobApplicationModel.objects.filter(job_post=job_post)
    
    context = {
      'job_post': job_post,
      'applicants': applicants,
      'total_applicants': applicants.count()
    }
    return render(req, 'applicant_list.html', context)
  except JobPostModel.DoesNotExist:
    return redirect('dashboard_page')
  
  