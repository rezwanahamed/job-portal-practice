from django.contrib import admin
from job_portal_app.models import User, RecruiterProfileModel, JobSeekerProfileModel, JobCategoryModel, JobPostModel, JobApplicationModel

# Register your models here.
admin.site.register([User, RecruiterProfileModel, JobSeekerProfileModel, JobCategoryModel, JobPostModel, JobApplicationModel])
