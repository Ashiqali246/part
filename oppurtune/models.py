from django.db import models

# Create your models here.
class login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class workers_table(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    image=models.FileField()
    phone=models.BigIntegerField()
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.IntegerField()
    email=models.CharField(max_length=40)

class job_provider(models.Model):
    LOGIN=models.ForeignKey(login_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    photo=models.FileField()
    id_proof=models.FileField()

class users_table(models.Model):
    LOGIN=models.ForeignKey(login_table, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    dob=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    image=models.FileField()
    idproof=models.FileField()
    phone=models.BigIntegerField()
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.BigIntegerField()

class job_opening(models.Model):
    JOB_PROVIDER=models.ForeignKey(job_provider, on_delete=models.CASCADE)
    job_type=models.CharField(max_length=100)
    no_of_vaccancy=models.IntegerField()
    qualification=models.CharField(max_length=100)
    experience=models.IntegerField()
    salary=models.BigIntegerField()
    due_date=models.DateField()


class chat(models.Model):
    fromid=models.ForeignKey(login_table, on_delete=models.CASCADE,related_name='from_id')
    toid=models.ForeignKey(login_table, on_delete=models.CASCADE,related_name='to_id')
    message=models.CharField(max_length=100)
    date=models.DateField()

class feedback(models.Model):
    USER=models.ForeignKey(users_table, on_delete=models.CASCADE)
    WORKER=models.ForeignKey(workers_table, on_delete=models.CASCADE)
    feedback=models.CharField(max_length=100)
    date=models.DateField()
    rating=models.CharField(max_length=100)

class complaint(models.Model):
    USER=models.ForeignKey(users_table, on_delete=models.CASCADE)
    complaint=models.CharField(max_length=100)
    date=models.DateField()
    replay=models.CharField(max_length=100)

class rate_info(models.Model):
    WORKER = models.ForeignKey(workers_table, on_delete=models.CASCADE)
    worktype=models.CharField(max_length=100)
    details=models.CharField(max_length=100)
    rate=models.CharField(max_length=100)

class work_request(models.Model):
    USER=models.ForeignKey(users_table, on_delete=models.CASCADE)
    WORKER=models.ForeignKey(workers_table, on_delete=models.CASCADE)
    description=models.CharField(max_length=500)
    date=models.DateField()
    status=models.CharField(max_length=100)

class rating(models.Model):
    USER=models.ForeignKey(users_table, on_delete=models.CASCADE)
    WORKER=models.ForeignKey(workers_table, on_delete=models.CASCADE)
    ratingg=models.CharField(max_length=100)
    review=models.CharField(max_length=100)
    date=models.DateField()



class job_application(models.Model):
    LOGIN=models.ForeignKey(login_table, on_delete=models.CASCADE)
    JOB=models.ForeignKey(job_opening, on_delete=models.CASCADE)
    date=models.DateField(max_length=100)
    qualification=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    status=models.CharField(max_length=100)


