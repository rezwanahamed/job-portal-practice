from django.urls import path
from job_portal_app.views import *

urlpatterns = [
    path('', userRegistration, name='registration_page'),
    path('login/', userLogin, name='login_page'),
    path('logout/', userLogout, name='logout_page'),
    path('create-profile/', createProfile, name='create_profile_page'),
    path('update-profile/', updateProfile, name='update_profile_page'),
    path('create-job-post/', createJobPost, name='create_job_post_page'),
    path('job-details/<int:job_post_id>/', jobDetails, name='job_details_page'),
    path('applicants/<int:job_post_id>/', applicant_list, name='applicant_list_page'),
    path('update-job/<int:job_post_id>/', updateJobPost, name='update_job_page'),
    path('delete-job/<int:job_post_id>/', deleteJobPost, name='delete_job_page'),
    path('apply-job/<int:job_post_id>/', applyJobPost, name='apply_job_post_page'),
    path('applied-jobs/', appliedJobs, name='applied_jobs_page'),
    path('recommended-jobs/', recommendedJobs, name='recommended_jobs_page'),
    path('dashboard/', dashboard, name='dashboard_page'),
]
