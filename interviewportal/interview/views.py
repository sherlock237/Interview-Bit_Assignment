from django.shortcuts import render
from .models import *
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Q
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self,**kwargs):
        context = TemplateView.get_context_data(self,**kwargs)
        interviewerdetail = []
        candidatedetail = []
        
        for i in Interviewer.objects.raw('Select * From interview_interviewer'):
            interviewerdetail.append(i.Name+"("+i.Email+")")

        for i in Candidate.objects.raw('Select * From interview_candidate'):
            candidatedetail.append(i.Name+"("+i.Email+")")

        upcomingevent = InterviewSchedule.objects.filter(Start_Date_time__gt=datetime.now()).order_by('Start_Date_time')
        print(upcomingevent)
        context['interviewerdetail'] = interviewerdetail
        context['candidatedetail']   = candidatedetail
        context['upcomingevent']     = upcomingevent
        return context

    def post(self,*args, **kwargs):
        msg=""
        if self.request.method == 'POST' and self.request.POST['action'] == 'Delete':
            msg = ""
            Id  = self.request.POST.get("Id")

            InterviewSchedule.objects.filter(Id=Id).delete()
            msg = "Ok"
            context = {'msg':msg}
            return JsonResponse(context, status=200)
        if self.request.method =='POST' and self.request.POST['action']=='interview_schedule':
            interviewer_name  = self.request.POST.get('interviewer_name')
            interviewer_email = self.request.POST.get('interviewer_email')
            candidate_name    = self.request.POST.get('candidate_name')
            candidate_email   = self.request.POST.get('candidate_email')
            start_date_time   = self.request.POST.get('start_date_time')
            end_date_time     = self.request.POST.get('end_date_time')
            
            end_date_time = datetime.strptime(end_date_time, "%m/%d/%Y %I:%M %p")
            start_date_time = datetime.strptime(start_date_time, "%m/%d/%Y %I:%M %p")
            interviewer_instance = Interviewer.objects.get(Email=interviewer_email)
            candidate_instance = Candidate.objects.get(Email=candidate_email)
            interview_schedule_instance = InterviewSchedule.objects.filter(Interviewer_Email=interviewer_email)

            for i in interview_schedule_instance:
                if(start_date_time.date()==i.Start_Date_time.date() and 
                    (start_date_time.time()>=i.Start_Date_time.time() and start_date_time.time()<=i.End_Date_time.time()) 
                        or start_date_time.date()==i.Start_Date_time.date() 
                    and(end_date_time.time()>=i.Start_Date_time.time() and end_date_time.time()<=i.End_Date_time.time())):
                    msg="Interviewer Time is Booked"+""
                    context = {'msg':msg}
                    return JsonResponse(context, status=400)
            
            candidate_schedule_instance = InterviewSchedule.objects.filter(Candidate_Email=candidate_email)
            for i in candidate_schedule_instance:
                if(start_date_time.date()==i.Start_Date_time.date() 
                    and (start_date_time.time()>=i.Start_Date_time.time() and start_date_time.time()<=i.End_Date_time.time()) 
                        or start_date_time.date()==i.Start_Date_time.date() 
                    and(end_date_time.time()>=i.Start_Date_time.time() and end_date_time.time()<=i.End_Date_time.time())):
                    msg="Candidate has an interview at that time slot"+""
                    context = {'msg':msg}
                    return JsonResponse(context, status=400)
            IS = InterviewSchedule(
                Interviewer_Email = interviewer_instance,
                Candidate_Email   = candidate_instance,
                Start_Date_time   = start_date_time,
                End_Date_time     = end_date_time,
                
            )
            IS.save()
            # print(start_date_time.split(" ")[0])
            msg = "Interview is Successfully Schedule: Intereview Email:"+" "+interviewer_email+" "+"and Candidate Email:"+" "+candidate_email+" "+"at"+" "+str(start_date_time)
        
        context = {'msg':msg}
        return JsonResponse(context, status = 200)


def Update(request,Id):
    update_detail = InterviewSchedule.objects.filter(Id = Id)
    for i in update_detail:
        interview_detail = Interviewer.objects.filter(Email = i.Interviewer_Email)
        candidate_detail = Candidate.objects.filter(Email = i.Candidate_Email)
    for i in interview_detail:
        intv_detail = i.Name+"("+i.Email+")"
    for i in candidate_detail:
        cand_detail = i.Name+"("+i.Email+")"
    
    interviewerdetail = []
    candidatedetail = []

    for i in Interviewer.objects.raw('Select * From interview_interviewer'):
        interviewerdetail.append(i.Name+"("+i.Email+")")

    for i in Candidate.objects.raw('Select * From interview_candidate'):
        candidatedetail.append(i.Name+"("+i.Email+")")

    context = {
        'update_detail'  : update_detail,
        'curr_int_name_email': intv_detail,
        'curr_can_name_email' : cand_detail,
        'interviewerdetail' : interviewerdetail,
        'candidate_detail' : candidatedetail,

    }
    if request.method =='POST' and request.POST['action']=='interview_schedule':
        
        msg=""
        interviewer_name  = request.POST.get('interviewer_name')
        interviewer_email = request.POST.get('interviewer_email')
        print(interviewer_name)
        candidate_name    = request.POST.get('candidate_name')
        candidate_email   = request.POST.get('candidate_email')
        start_date_time   = request.POST.get('start_date_time')
        end_date_time     = request.POST.get('end_date_time')
        print(interviewer_email+" "+candidate_email+" "+start_date_time+" "+end_date_time+" ")
        end_date_time = datetime.strptime(end_date_time, "%m/%d/%Y %I:%M %p")
        start_date_time = datetime.strptime(start_date_time, "%m/%d/%Y %I:%M %p")
        interviewer_instance = Interviewer.objects.get(Email=interviewer_email)
        candidate_instance = Candidate.objects.get(Email=candidate_email)
        interview_schedule_instance = InterviewSchedule.objects.filter(Interviewer_Email=interviewer_email)

        for i in interview_schedule_instance:
                if(start_date_time.date()==i.Start_Date_time.date() and 
                    (start_date_time.time()>=i.Start_Date_time.time() and start_date_time.time()<=i.End_Date_time.time()) 
                        or start_date_time.date()==i.Start_Date_time.date() 
                    and(end_date_time.time()>=i.Start_Date_time.time() and end_date_time.time()<=i.End_Date_time.time())):
                    msg="Interviewer Time is Booked"+""
                    context = {'msg':msg}
                    return JsonResponse(context, status=400)

        candidate_schedule_instance = InterviewSchedule.objects.filter(Candidate_Email=candidate_email)
        for i in candidate_schedule_instance:
            if(start_date_time.date()==i.Start_Date_time.date() 
                and (start_date_time.time()>=i.Start_Date_time.time() and start_date_time.time()<=i.End_Date_time.time()) 
                    or start_date_time.date()==i.Start_Date_time.date() 
                and(end_date_time.time()>=i.Start_Date_time.time() and end_date_time.time()<=i.End_Date_time.time())):
                msg="Candidate has an interview at that time slot"+""
                context = {'msg':msg}
                return JsonResponse(context, status=400)
        
        InterviewSchedule.objects.filter(Id=Id).update(Interviewer_Email = interviewer_instance,Candidate_Email=candidate_instance,Start_Date_time = start_date_time,End_Date_time = end_date_time)
        # print(start_date_time.split(" ")[0])
        msg = "Interview is Successfully Updated"+""
        context = {'msg':msg}
        return JsonResponse(context, status = 200)
    return render(request,'update.html',context)
    
    
