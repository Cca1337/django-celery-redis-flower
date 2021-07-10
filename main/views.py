from django.shortcuts import render
from .tasks import count_words, send_async_email, get_weather_api
from django.http import JsonResponse
from django.contrib import messages
from celery import current_app
import time
from django_celery_results.models import TaskResult
from collections import defaultdict
import operator

task_ids = []
task_ids_wc = []
success = 'SUCCESS'        
failure = 'FAILURE'
active = 'ACTIVE'

  
# ----------------Create your views here-------------

def home(response):

    messages.success(response, "Zdravicko")
    return render(response, "main/home.html", {})
    
    
#--------------WEATHER FORECAST----------------    
def weather(response):

    for i in task_ids:
        for i in  TaskResult.objects.filter(task_id=i):
            if i.status == success:
                task_ids.remove(i.task_id)
           

    if response.method == "POST":

        mesto = response.POST.get('mesto')
        

        
        if len(mesto) < 1:
            messages.error(response,"I bet there is no city which such a short name!")
        else:
            try:
                task = get_weather_api.delay(mesto)

                message = f"Task id: {task} started status: {task.status}"

                messages.success(response,f"Pre mesto {mesto} task id: {task}")
                
                if task in task_ids:
                    pass
                else:    
                    task_ids.append(task)
                    
                string = 'main.tasks.get_weather_api'

                
                for e in TaskResult.objects.all():
                    if e.task_name == string:
                        if e.status != failure and e.status != success:
#                            print(e.task_name)
#                            print(e.task_id)
#                            print(e.status)
                            
                            if e.task_id in task_ids:
                                continue
                            else:
                                task_ids.append(e.task_id)      
                 
                for i in task_ids:
                    for i in  TaskResult.objects.filter(task_id=i):
                        if i.status == success:
                            task_ids.remove(i.task_id)
                                      

                return render(response, "main/weather.html", {"task_ids": task_ids})

            except KeyError as err:
                flash(f"[ERROR] Problem with city name: [{mesto}]. Try again!", category='error')
                
                return render_template("main/weather.html")


    else:
    
        for i in task_ids:
            for i in TaskResult.objects.filter(task_id=i):
                if i.status == success:
                    task_ids.remove(i.task_id)
    
    
    return render(response, "main/weather.html", {"task_ids": task_ids})

       
#-------------------EMAIL SENDER ----------------------
def email_sender(response):

    if response.method == 'GET':
    
        return render(response, "main/mails.html", {"email": response.session.get('email', '')})
        
    email = response.POST.get('email')

    response.session['email'] = email
    
    # send the email
    email_data = {
        'subject': 'Hello from Django',
        'to': email,
        'body': 'This is a test email sent from a background Celery task.'
    }
    if response.POST.get('submit') == 'Send':
        # send right away
        send_async_email.delay(email_data)
        messages.success(response,'Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[email_data], countdown=60)
        messages.success(response, 'An email will be sent to {0} in one minute'.format(email))


    return render(response, "main/mails.html", {"email": email})    
        
   
#--------------------word counter -------------------------   
    
def word_counter(response):


    for i in task_ids_wc:
        for i in TaskResult.objects.filter(task_id=i):
            if i.status == success:
                task_ids_wc.remove(i.task_id)        

    if response.method == "POST":
        message = None

        url = response.POST.get('url')
        task = count_words.delay(url) 
        messages.success(response, f"Aktualny jobik si zadal {task.id} a status je : {task.status} ")  
        
        if task in task_ids_wc:
            pass
        else:    
            task_ids_wc.append(task)
                    
        string = 'main.tasks.count_words'

        print(task_ids)        
        for e in TaskResult.objects.all():
            if e.task_name == string:
                if e.status != failure and e.status != success:
                    print(e.task_name)
                    print(e.task_id)
                    print(e.status)
                            
                    if e.task_id in task_ids_wc:
                        continue
                    else:
                        task_ids_wc.append(e.task_id)      
        print(task_ids)                  
        for i in task_ids_wc:
            for i in TaskResult.objects.filter(task_id=i):
                if i.status == success:
                    task_ids_wc.remove(i.task_id)             

        print(task_ids)   
        return render(response, "main/word_counter.html", {"task_ids_wc": task_ids_wc})  
        
    else:
    
        return render(response, "main/word_counter.html", {"task_ids_wc": task_ids_wc})      
    
#-----------------------DASHBOARD------------

def dashboard(response):


#    for e in TaskResult.objects.all():
#        if e.status == success:
#            print("---------")
#            print(e.task_name)
#            print(e.task_args)
#            print(e.task_id)
#            print(e.status)
#            print(e.result)


    last_five = TaskResult.objects.filter(status=success).order_by('-id')[:5]


 #   all = TaskResult.objects.all()
    failed = TaskResult.objects.filter(status=failure)
    
    return render(response, "main/dashboard.html", {"success": success,
    						    "failure":failure,
    						    "last_five": last_five,
    						    "failed": failed
    						    })
    						    
    