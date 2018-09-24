from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.
class Patient(models.Model):
    p_id = models.CharField(primary_key=True, max_length = 4)
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,10}$', message="")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True) # validators should be a list
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name


class Evaluation(models.Model):
    e_id = models.CharField(primary_key=True, max_length = 4)
    test_name = models.CharField(max_length=200, null=True)
    STATUS_CHOICES = (
        ('C', 'Completed'),
        ('I', 'Incomplete'),
    )
    status = models.CharField(max_length=1, choices = STATUS_CHOICES)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.e_id + "-" + self.test_name + "-" + self.patient.name + " "+ self.patient.doctor.username

class Result(models.Model):
    label = models.CharField(max_length=200, null=True)
    val = models.FloatField()
    optimalH = models.FloatField()
    optimalL = models.FloatField()
    eval = models.ForeignKey(Evaluation, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.label + "-" + self.eval.test_name + "-" + self.eval.e_id
