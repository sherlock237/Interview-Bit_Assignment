from django.contrib import admin
from .models import*
# Register your models here.

class InterviewerAdmin(admin.ModelAdmin):
    list_display =['Email','Name']
class InterviewScheduleAdmin(admin.ModelAdmin):
    list_display =['Id','Interviewer_Email','Candidate_Email','Start_Date_time','End_Date_time']
class CandidateAdmin(admin.ModelAdmin):
    list_display =['Email','Name']


admin.site.register(Interviewer,InterviewerAdmin)
admin.site.register(Candidate,CandidateAdmin)
admin.site.register(InterviewSchedule,InterviewScheduleAdmin)