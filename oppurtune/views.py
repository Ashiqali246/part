import datetime
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from oppurtune.models import *


# def login(request):
#     return render(request,'admin/login.html')

def login(request):
    return render(request,'index.html')

def login_post(request):
    print(request.POST,'jjjjjjjjjj')
    uname=request.POST['textfield']
    passw=request.POST['textfield2']

    if uname and passw:
        try:
            user = login_table.objects.get(username=uname, password=passw)
            request.session['lid']=user.id
            if user.type == 'admin':
                return HttpResponse('''<script> alert('Admin Logged');window.location='/admin_home';</script>''')
            elif user.type == 'job provider':
                return HttpResponse('''<script> alert('Provider Logged');window.location='/job_provider_home_page';</script>''')
            elif user.type == 'worker':
                return HttpResponse('''<script> alert('Worker Logged');window.location='/worker_home_page';</script>''')
            else:
                return HttpResponse('''<script> alert('Invalid');window.location='/';</script>''')

        except:
            return HttpResponse('''<script> alert('Invalid');window.location='/';</script>''')

    else:
        return HttpResponse('''<script> alert('Invalid');window.location='/';</script>''')

def view_feedback(request):
    ob=rating.objects.all()
    return render(request,'admin/feedback.html',{'data':ob})

def view_jobprovider(request):
    a=job_provider.objects.all()
    return render(request,'admin/jobprovider.html',{'data':a})


def accept_jobprovider(request,id):
    a=login_table.objects.get(id=id)
    a.type='job provider'
    a.save()
    return HttpResponse('''<script> alert('Accepted');window.location='/view_jobprovider';</script>''')

def reject_jobprovider(request,id):
    a=login_table.objects.get(id=id)
    a.type='rejected'
    a.save()
    return HttpResponse('''<script> alert('Rejected');window.location='/view_jobprovider';</script>''')


# def view_verifiedjobprovider(request):
#     a=job_provider.objects.all()
#     return render(request,'admin/verified job provider.html',{'data':a})
def view_verifiedjobprovider(request):
    a=job_provider.objects.filter(LOGIN__type ='job provider')
    return render(request,'admin/verified job provider.html',{'data':a})

def send_reply(request, id):
    request.session['cid'] = id
    return render(request, 'admin/replyto complaint.html')


def send_reply_post(request):
    replay = request.POST['textfield']
    cid = request.session['cid']

    c = complaint.objects.get(id=cid)
    c.replay = replay
    c.save()

    return HttpResponse('''<script> alert('replied'); window.location='/veiw_complaint'; </script>''')

def veiw_complaint(request):
    a=complaint.objects.all()
    return render(request,'admin/sendcomplaint.html',{'data':a})


def veiw_complaint_jp(request):
    a=complaint.objects.all()
    return render(request,'job provider/sendcomplaintjb.html',{'data':a})




def admin_home(request):
    return render(request,'admin/index.html')

def view_users_table(request):
    a=users_table.objects.all()
    return render(request,'admin/user.html',{'data':a})


def worker_registration(request):
    return render(request,'worker/regindex.html')
def worker_register_post(request):
    name=request.POST['name']
    dob=request.POST['textfieldd']
    place=request.POST['textfield3']
    post=request.POST['textfield']
    pin=request.POST['textfield7']
    phone=request.POST['textfield2']
    gender=request.POST['textfield3']
    username=request.POST['textfield4']
    password=request.POST['textfield5']
    email=request.POST['email']
    image = request.FILES['file']
    fs=FileSystemStorage()
    fp=fs.save(image.name,image)

    log_details = login_table()
    log_details.username = username
    log_details.password = password
    log_details.type="worker"
    log_details.save()

    reg_details=workers_table()
    reg_details.name=name
    reg_details.dob=dob
    reg_details.email=email
    reg_details.place=place
    reg_details.post=post
    reg_details.pin=pin
    reg_details.phone=phone
    reg_details.gender=gender
    reg_details.username=username
    reg_details.password=password
    reg_details.image=fp
    reg_details.type='worker'
    reg_details.LOGIN=log_details
    reg_details.save()


    return HttpResponse('''<script> alert('worker successfully registered');window.location='/';</script>''')

#
# def worker_home_page(request):
#     return render(request,'worker/worker home page.html')


def worker_home_page(request):
    return render(request,'worker/index.html')
def view_work_request(request):
    a = work_request.objects.all()
    return render(request,'worker/viewworkstatus.html',{'data':a})


def work_status(request):
    ob=work_request.objects.get()
    return render(request,'worker/upadate status.html',{'data':ob})

def work_status_update(request):
    name=request.POST['textfield']
    date=request.POST['textfield3']
    status=request.POST['textfield2']

    c=work_request()
    c.USER=users_table.objects.get(id=name)
    c.date=date
    c.status=status
    c.save()
    return render(request,'worker/upadate status.html')

def accept_work(request,id):
    dat=work_request.objects.filter(id=id).update(status='accepted')
    return HttpResponse('''<script> alert('Status Updated');window.location='/view_work_request';</script>''')

def reject_work(request,id):
    dat=work_request.objects.filter(id=id).update(status='rejected')
    return HttpResponse('''<script> alert('Status Updated');window.location='/view_work_request';</script>''')

def manage_rate(request):
    print(request.session['lid'],'ffftffffffffffffffffffff')
    dat=rate_info.objects.filter(WORKER__LOGIN_id=request.session['lid'])
    return render(request, 'worker/manage rate.html', {'data':dat})

def new_rate(request):
    return render(request,'worker/add new rate.html')

def new_rate_post(request):
    worktype=request.POST['textfield']
    details=request.POST['textfield2']
    rate=request.POST['textfield3']
    ob=rate_info()
    ob.worktype=worktype
    ob.WORKER=workers_table.objects.get(LOGIN_id=request.session['lid'])
    ob.details=details
    ob.rate=rate
    ob.save()
    return HttpResponse('''<script>alert('new rate added successfully');window.location='manage_rate'</script>''')

def edit_rate(request,id):
    ob=rate_info.objects.get(id=id)
    request.session['rid']=id
    return render(request,'worker/edit rate.html',{'val':ob})

def edit_rate_post(request):
    worktype=request.POST['textfield']
    details=request.POST['textfield2']
    rate=request.POST['textfield3']

    ob=rate_info.objects.get(id=request.session['rid'])
    ob.worktype=worktype
    ob.details=details
    ob.rate=rate
    ob.save()
    return HttpResponse('''<script>alert('updated successfully');window.location='/manage_rate';</script>''')


def delete_rate(request,id):
    pd=rate_info.objects.get(id=id)
    pd.delete()
    return HttpResponse('''<script>alert('Deleted successfully');window.location='/manage_rate';</script>''')

def view_profile(request):
    work=workers_table.objects.get(LOGIN_id=request.session['lid'])
    print(work,'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
    return render(request,'worker/view profile.html',{'work':work})

def edit_profile(request):
    work = workers_table.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'worker/edit profile.html', {'work': work})

def editProfilePost(request):
    name=request.POST["textfield"]
    phone=request.POST["textfield2"]
    place=request.POST["place"]
    post=request.POST["post"]
    pin=request.POST["pin"]
    dob=request.POST["textfield4"]
    email=request.POST["email"]


    ob=workers_table.objects.get(LOGIN_id=request.session['lid'])
    ob.name=name
    ob.phone=phone
    ob.place=place
    ob.pin=pin
    ob.post=post
    ob.email=email
    ob.dob=dob
    if 'file' in request.FILES:
        image = request.FILES["file"]
        fs = FileSystemStorage()
        fp = fs.save(image.name, image)
        ob.image = fp
        ob.save()


    else:
        pass

    ob.save()
    return HttpResponse('''<script>alert('Successfully Updated');window.location='/view_profile';</script>''')



def job_provider_register(request):
    return render(request,'job provider/regindex.html')

def job_provider_register_post(request):
    name=request.POST['textfield']
    place=request.POST['textfield3']
    post=request.POST['textfield4']
    pin=request.POST['textfield5']
    phone=request.POST['textfield6']
    email=request.POST['textfield7']
    username=request.POST['textfield8']
    password=request.POST['textfield9']
    image = request.FILES['file']
    id_proof = request.FILES['idproof']
    fs=FileSystemStorage()
    fp=fs.save(image.name,image)
    fn=fs.save(id_proof.name,id_proof)
    ob=login_table()
    ob.username=username
    ob.password=password
    ob.password=password
    ob.type="pending"
    ob.save()
    ob1=job_provider()
    ob1.LOGIN=ob
    ob1.name=name
    ob1.place=place
    ob1.post=post
    ob1.pin=pin
    ob1.phone=phone
    ob1.email=email
    ob1.photo=fp
    ob1.id_proof=fn
    ob1.save()
    return HttpResponse('''<script>alert('Registered successfully !');window.location='/';</script>''')


def add_job_opening(request):
    return render(request,'job provider/add job opening.html')

def view_rating(request):
    ob=rating.objects.filter(WORKER__LOGIN_id= request.session['lid'])
    return render(request,'worker/view_rating.html',{'val':ob})

def job_provider_feedback(request):
    return render(request,'job provider/feedback.html')

# def job_provider_register(request):
#     return render(request,'job provider/job provider register.html')

def Jobopening(request):
    ob=job_opening.objects.filter(JOB_PROVIDER__LOGIN_id=request.session['lid'])
    return render(request,'job provider/Jobopening.html',{'val':ob})



def Delete_jobopenings(request,id):
    request.session['jid']=id
    ob=job_opening.objects.get(id=request.session['jid'])
    ob.delete()
    return HttpResponse('''<script>alert('Successfully Deleted');window.location='/Jobopening';</script>''')


def edit_job_openings(request,id):
    request.session['jid'] = id
    ob = job_opening.objects.get(id=request.session['jid'])
    return render(request,'job provider/editjobopenings.html',{'val':ob,"date":str(ob.due_date)})


def add_job_opening(request):
    return render(request,'job provider/add job opening.html')

def add_job_opening_post(request):
    job_type = request.POST['textfield']
    no_of_vaccancy = request.POST['textfield5']
    qualification = request.POST['textfield4']
    experience = request.POST['textfield2']
    salary = request.POST['textfield6']
    due_date = request.POST['ooo']
    ob = job_opening()
    ob.job_type = job_type
    ob.JOB_PROVIDER = job_provider.objects.get(LOGIN_id=request.session['lid'])
    ob.qualification = qualification
    ob.no_of_vaccancy = no_of_vaccancy
    ob.experience = experience
    ob.salary = salary
    ob.due_date = due_date
    ob.save()
    return HttpResponse('''<script>alert('job_opening added successfully');window.location='Jobopening'</script>''')



def edit_job_opening_post(request):
    job_type = request.POST['textfield']
    no_of_vaccancy = request.POST['textfield5']
    qualification = request.POST['textfield4']
    experience = request.POST['textfield3']
    salary = request.POST['textfield6']
    due_date = request.POST['ooo']

    ob=job_opening.objects.get(id=  request.session['jid'])
    ob.job_type = job_type
    ob.JOB_PROVIDER = job_provider.objects.get(LOGIN_id=request.session['lid'])
    ob.qualification = qualification
    ob.no_of_vaccancy = no_of_vaccancy
    ob.experience = experience
    ob.salary = salary
    ob.due_date = due_date
    ob.save()
    return HttpResponse('''<script>alert('updated successfully');window.location='/Jobopening';</script>''')


def veiw_user(request):
    ob=users_table.objects.all()
    return render(request,'job provider/veiw user.html',{"val":ob})

def verifyjobprovider(request):
    ob = job_application.objects.filter(JOB__JOB_PROVIDER__LOGIN__id=request.session['lid'])
    return render(request, 'job provider/verifyjobprovider.html', {"val": ob})



def accept_jobrequest(request,id):
    dat=job_application.objects.filter(id=id).update(status='accepted')
    return HttpResponse('''<script> alert('Status Updated');window.location='/verifyjobprovider';</script>''')

def reject_jobrequest(request,id):
    dat=job_application.objects.filter(id=id).update(status='rejected')
    return HttpResponse('''<script> alert('Status Updated');window.location='/verifyjobprovider';</script>''')


def job_provider_home_page(request):
    # return render(request,'job provider/job provider home page.html')
    return render(request,'job provider/jobpindex.html')



def view_jobapplication(request):
    ob=job_application.objects.filter(JOB__JOB_PROVIDER__LOGIN__id=request.session['lid'])
    return render(request,'job provider/verifyjobprovider.html',{"val":ob})




def chatwithuser(request):
    ob = users_table.objects.all()
    return render(request,"job provider/chat with user.html",{'val':ob})




def chatview(request):
    ob = users_table.objects.all()
    d=[]
    for i in ob:
        r={"name":i.name,'photo':i.image.url,'email':i.phone,'loginid':i.LOGIN.id}
        d.append(r)
    return JsonResponse(d, safe=False)




def coun_insert_chat(request,msg,id):
    print("===",msg,id)
    ob=chat()
    ob.fromid=login_table.objects.get(id=request.session['lid'])
    ob.toid=login_table.objects.get(id=id)
    ob.message=msg
    ob.date=datetime.datetime.today().strftime("%Y-%m-%d")
    ob.time=datetime.datetime.today()
    ob.save()

    return JsonResponse({"task":"ok"})
    # refresh messages chatlist



def coun_msg(request,id):

    ob1=chat.objects.filter(fromid__id=id,toid__id=request.session['lid'])
    ob2=chat.objects.filter(fromid__id=request.session['lid'],toid__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.fromid.id,"msg":i.message,"date":i.date,"chat_id":i.id})

    obu=users_table.objects.get(LOGIN__id=id)


    return JsonResponse({"data":res,"name":obu.name,"photo":obu.image.url,"user_lid":obu.LOGIN.id})

# def update_profile(request):
#     name=request.POST['name']
#     place=request.POST['place']
#     post=request.POST['post']
#     pin=request.POST['pin']
#     dob=request.POST['dob']
#     image=request.POST['image']


# ---------------------android---------------------------------

def and_login_post(request):
    print(request.POST,'jjjjjjjjjj')
    uname=request.POST['username']
    passw=request.POST['password']

    if uname and passw:
        try:
            user = login_table.objects.get(username=uname, password=passw)

            return JsonResponse({"status":"ok","lid":user.id,'type':user.type})

        except:
            return JsonResponse({"status": "no"})


    else:
        return JsonResponse({"status": "no"})



def user_register(request):
    name=request.POST['name']
    dob=request.POST['dob']
    gender=request.POST['gender']
    image=request.FILES['files']
    idproof=request.FILES['idproof']
    phone=request.POST['phone']
    place=request.POST['place']
    post=request.POST['post']
    pin=request.POST['pin']
    username=request.POST['username']
    password=request.POST['password']

    fs=FileSystemStorage()
    path=fs.save(image.name,image)
    fp=fs.save(idproof.name,idproof)

    a=login_table()
    a.username=username
    a.password=password
    a.type='user'
    a.save()


    b=users_table()
    b.LOGIN=a
    b.name=name
    b.image=path
    b.idproof=fp
    b.dob=dob
    b.pin=pin
    b.place=place
    b.post=post
    b.gender=gender
    b.phone=phone
    b.save()
    return JsonResponse({'status':'ok'})



def view_job(request):
    l=[]
    a=job_opening.objects.all()
    for i in a:
        l.append({'id':i.id,'JOB_PROVIDER':i.JOB_PROVIDER.name,
                  'job_type':i.job_type,'no_of_vaccancy':i.no_of_vaccancy,
                  'qualification':i.qualification,
                  'experience':i.experience,
                  'salary':i.salary,
                  'due_date':i.due_date})
    print(l)
    return JsonResponse({"status":'ok','data':l})



def view_application_status(request):
    print(request.POST,'lllllllllllllll')
    lid = request.POST['lid']
    a = job_application.objects.filter(LOGIN_id=lid)
    print(a,"gggggggggggggg")
    l = []
    for i in a:
        l.append({
            'id': i.id,
            'JOB': i.JOB.job_type,
            'date': i.date,
            'qualification': i.qualification,
            'experience': i.experience,
            'status': i.status,
            'pid':i.JOB.JOB_PROVIDER.LOGIN.id
        })
    return JsonResponse({"status": 'ok', "data": l})




def veiw_request_status(request):
    l=[]
    a=request.objects.all()
    for i in a:
        l.append({'id':i.id,
                  'USER':i.USER.name,
                  'WORKER':i.WORKER.name,
                  'description':i.description,
                  'date':i.date,
                  'status':i.status})
    return JsonResponse({"status":'ok','data':l})


def view_worker(request):
    workers_list = []
    workers = workers_table.objects.all()

    for worker in workers:
        obty=rate_info.objects.filter(WORKER__id=worker.id)
        lis=[]
        for j in obty:
            lis.append(j.worktype)
        workers_list.append({
            'id': worker.id,
            'name': worker.name,
            'dob': str(worker.dob),
            'gender': worker.gender,
            'image': request.build_absolute_uri(worker.image.url) if worker.image else None,
            'phone': worker.phone,
            'place': worker.place,
            'post': worker.post,
            'pin': worker.pin,
            'wt': ', '.join(lis)
        })
        print(workers_list)

    return JsonResponse({"status": 'ok', 'data': workers_list})


# def veiw_rating(request):
#     lid=request.POST['lid']
#     a=rating.objects.filter(WORKER__LOGIN__id=)
#     for i in a:
#         l.append({'id':i.id,
#                   'USER':i.USER.name,
#                   'WORKER':i.WORKER.name,
#                   'rating':i.rating,
#                   'date':i.date
#                   })
#     return JsonResponse({"status":'ok','data':l})
#


def veiw_reply(request):
     l=[]
     a=complaint.objects.all()
     for i in a:
         l.append({'id':i.id,
                   'USER':i.USER.name,
                   'complaint':i.complaint,
                   'date':i.date,
                   'replay':i.replay
         })
     return JsonResponse({"status": 'ok', 'data': l})

def ViewMyComplaints(request):
    lid = request.POST['id']
    user = users_table.objects.get(LOGIN=lid)
    complaints = complaint.objects.filter(USER=user).order_by('-id')
    comp = []
    for i in complaints:
        comp.append({
            'id':i.id,
            'complaint':i.complaint,
            'date':i.date,
            'reply':i.replay
        })
    return JsonResponse({'status':'ok','complaint':comp})

def Viewrating(request):
    wid = request.POST['wid']
    ratings = rating.objects.filter(WORKER_id=wid)
    comp = []
    for i in ratings:
        comp.append({
            'id': i.id,
            'rating':str(i.ratingg),
            'date': str(i.date),
            'USER': str(i.USER.name),
        })
    print(comp)
    return JsonResponse({'status': 'ok', 'data': comp})

def SendAppComplaint(request):
    from datetime import datetime
    user = users_table.objects.get(LOGIN=request.POST['id'])
    comp = request.POST['complaint']

    complaint.objects.create(
        USER=user,
        complaint=comp,
        date=datetime.today(),
        replay='pending'
    )
    return JsonResponse({'status':'ok'})

def DeleteMyComplaint(request):
    complaint_id = request.POST['complaint_id']
    c = complaint.objects.get(id=complaint_id)
    c.delete()
    return JsonResponse({'status':'ok'})



def addrating(request):
    rat = request.POST['rating']
    lid = request.POST['lid']
    wid = request.POST['wid']
    review = request.POST['review']
    review = request.POST['review']
    ob=rating()
    ob.ratingg=rat
    ob.review=review
    ob.date=datetime.datetime.now().today().date()
    ob.WORKER=workers_table.objects.get(id=wid)
    ob.USER=users_table.objects.get(LOGIN_id=lid)
    ob.save()
    return JsonResponse({'status': 'ok'})



def Sendrequest(request):
    print('pppppppppppppppp')
    print(request.POST['wid'])
    user = users_table.objects.get(LOGIN_id=request.POST['id'])
    worker=workers_table.objects.get(id=request.POST['wid'])
    description = request.POST['description']

    work_request.objects.create(
        USER=user,
        WORKER=worker,
        description=description,
        date=datetime.datetime.today(),
        status='pending'
    )
    return JsonResponse({'status':'ok'})

def Viewrequest_status(request):
    lid = request.POST['lid']
    print(lid,"llllllllllllllllll")
    req = work_request.objects.filter(USER__LOGIN__id=lid)
    comp = []
    for i in req:
        comp.append({
            'id': str(i.id),
            'WORKER': i.WORKER.name,
            'WORKERid': i.WORKER.id,
            'description': i.description,
            'date': str(i.date),
            'status': i.status,
        })
    print(comp)
    return JsonResponse({'status': 'ok', 'data': comp})



def view_worker_det(request):
    wid = request.POST['wid']
    print(wid,"llllllllllllllllll")
    req = rate_info.objects.filter(WORKER__id=wid)
    comp = []
    for i in req:
        comp.append({

            'worktype': i.worktype,
            'details': str(i.details),
            'rate': i.rate,
        })
    print(comp)
    return JsonResponse({'status': 'ok', 'data': comp})





def view_worker_det(request):
    wid = request.POST['wid']
    print(wid,"llllllllllllllllll")
    req = rate_info.objects.filter(WORKER__id=wid)
    comp = []
    for i in req:
        comp.append({

            'worktype': i.worktype,
            'details': str(i.details),
            'rate': i.rate,
        })
    print(comp)
    return JsonResponse({'status': 'ok', 'data': comp})





def view_profile_user(request):
    wid = request.POST['lid']
    print(wid,"llllllllllllllllll")
    req = users_table.objects.get(LOGIN__id=wid)
    print(req)
    return JsonResponse({'status': 'ok', 'name': req.name
                         ,"dob":str(req.dob),"gender":req.gender,"image":req.image.url,"phone":str(req.phone),"place":req.place,"post":str(req.post)})





# def apply_for_job(request):
#         lid = request.POST['lid']
#         user_id = request.POST['lid']
#         job_id = request.POST['job_id']
#         qualification = request.POST['qualification']
#         experience = request.POST['experience']
#         user = login_table.objects.get(id=user_id)
#         job = job_opening.objects.get(id=job_id)
#
#         application = job_application(
#             LOGIN=user,
#             JOB=job,
#             date=datetime.datetime.now().date(),
#             qualification=qualification,
#             experience=experience,
#             status="pending"  # Initial status of the application
#         )
#         application.save()
#
#         return JsonResponse({"status": "ok", "message": "Application submitted successfully!"})

def apply_for_job(request):
    try:
        # Extract data from the request
        lid = request.POST['lid']
        user_id = request.POST['lid']
        job_id = request.POST['job_id']
        qualification = request.POST['qualification']
        experience = request.POST['experience']

        # Fetch user and job objects
        user = login_table.objects.get(id=user_id)
        job = job_opening.objects.get(id=job_id)

        # Check if an application already exists for the same user and job
        if job_application.objects.filter(LOGIN=user, JOB=job).exists():
            return JsonResponse({"status": "error", "message": "You have already applied for this job."})

        # Create a new application if no duplicate is found
        application = job_application(
            LOGIN=user,
            JOB=job,
            date=datetime.datetime.now().date(),
            qualification=qualification,
            experience=experience,
            status="pending"  # Initial status of the application
        )
        application.save()

        return JsonResponse({"status": "ok", "message": "Application submitted successfully!"})

    except login_table.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invalid user ID."})
    except job_opening.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invalid job ID."})
    except Exception as e:
        # Handle any unexpected errors
        return JsonResponse({"status": "error", "message": f"An error occurred: {str(e)}"})





# def forgot_password(request):
#     print(request.POST)
#     try:
#         username = request.POST['username']
#         s = login_table.objects.get(username=username)
#
#         # If user is not found or doesn't exist, return an invalid response
#         if s is None:
#             return JsonResponse({"status": "Invalid username"})
#         else:
#             # Fetch the Organization associated with the Login object
#             try:
#                 organization = users_table.objects.get(LOGIN=s)
#                 email_address = organization.email  # Assuming email is in Organization model
#             except users_table.DoesNotExist:
#                 return JsonResponse({"status": "Email not available in Organization"})
#
#             if not email_address:
#                 return JsonResponse({"status": "Email not available"})
#
#             # Create the email content
#             subject = 'Password Reset'
#             message = f"Your password: {s.password}"
#             from_email = 'contactashiqashiq@gmail.com'
#
#             try:
#                 # Send the email with the password to the user's email address
#                 send_mail(subject, message, from_email, [email_address])
#                 return JsonResponse({"status": "ok"})
#             except Exception as e:
#                 print(f"Error sending email: {str(e)}")
#                 return JsonResponse({"status": "Email sending failed"})
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return JsonResponse({"status": "Error occurred"})




def forgot_password(request):
    print(request.POST)

    try:
        username = request.POST.get('username')

        # Fetch the user from the login table
        try:
            user = login_table.objects.get(username=username)
        except login_table.DoesNotExist:
            return JsonResponse({"status": "Invalid username"})

        email_address = user.username  # Assuming

        if not email_address:
            return JsonResponse({"status": "Email not available"})

        # Create the email content
        subject = 'Password Reset'
        message = f"Your password: {user.password}"
        from_email = 'contactashiqashiq@gmail.com'

        try:
            # Send the email with the password to the user's email address
            send_mail(subject, message, from_email, [email_address])
            return JsonResponse({"status": "ok"})
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return JsonResponse({"status": "Email sending failed"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"status": "Error occurred"})



def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    from django.db.models import Q
    res = chat.objects.filter(Q(fromid_id=fromid, toid_id=toid) | Q(fromid_id=toid, toid_id=fromid)).order_by("id")
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.fromid_id, "date": i.date, "to": i.toid_id})

    return JsonResponse({"status":"ok",'data':l})


def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=chat()
    c.fromid_id=FROM_id
    c.toid_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})





def web_forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = login_table.objects.get(username=username)
        except login_table.DoesNotExist:
            return HttpResponse(
                '''<script>alert('Invalid username');window.location='/'</script>''')

        # Check if user belongs to workers_table or job_provider
        email_address = None
        if workers_table.objects.filter(LOGIN=user).exists():
            worker = workers_table.objects.get(LOGIN=user)
            email_address = worker.email  # Assuming username is the email
        elif job_provider.objects.filter(LOGIN=user).exists():
            provider = job_provider.objects.get(LOGIN=user)
            email_address = provider.email  # Fetch email from job_provider
        else:
            return HttpResponse(
                '''<script>alert('Error');window.location='/'</script>''')

        if not email_address:
            return HttpResponse(
                '''<script>alert('Email not available');window.location='/'</script>''')

        # Sending the stored password as plaintext (⚠️ Security Risk)
        subject = 'Password Reset'
        message = f"Your password is: {user.password}"
        from_email = 'Parttime Connect'

        try:
            send_mail(subject, message, from_email, [email_address])
            return HttpResponse(
                '''<script>alert('Email sendsuccessfully');window.location='/'</script>''')
        except Exception as e:
            return HttpResponse(
                '''<script>alert('Error sending email');window.location='/'</script>''')

    return render(request, 'forgot_password.html')


