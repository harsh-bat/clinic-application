from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Patient,  Evaluation, Result
from django import forms
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
import numpy as np
# Create your views here.

blood = [['Hemoglobin' ,14.2, 18.3],['WBC' ,6.9 ,12.6],['RBC' ,5.93, 9.18],['Absolute Lymphocytes x 1000' ,1.643 ,3.548],['Absolute Monocytes x 100' ,2.10, 7.90]]
lipid = [["Total Cholestrol", 200, 239],["LDL Cholestrol" ,130, 159],["HDL Cholestrol" , 40, 60],["Triglycerides" , 150, 199],["Non-HDL-C" ,130 ,159],["TG HDL Ratio" ,3.1 ,3.8]]
bone = [["Reticulum cells", 1000, 4500],["Plasma cells" ,4500 ,7500],["Monocytes" ,2500 ,4000],["Metamyelocytes" ,25000 ,41000],["Macroblasts" ,3500 ,13000],["Basophiles" ,200 ,1200]]

def firstOnly(a):
    r = []
    for i in a:
        r.append(i[0])
    return r

@login_required
def index(request):
    selectedDoctor = request.user
    selectedPatients = Patient.objects.filter(doctor=selectedDoctor)[:]
    context = {"patients":selectedPatients}
    return render(request, "docProfile/index.html", context)

@login_required
def patient(request, id):
    p_id = id
    try:
        selectedPatient = Patient.objects.get(p_id = p_id)
    except Patient.DoesNotExist:
        selectedPatient  = None
        p_id = -1
    if p_id != -1:
        selectedEvals = Evaluation.objects.filter( patient = selectedPatient)
        context = {"evals": selectedEvals}
        return render(request, "docProfile/patient.html", context)
    else:
        return HttpResponse("Page not found")

@login_required
def result(request,id):
    selectedEval = Evaluation.objects.filter(e_id=id).first()
    results = Result.objects.filter(eval = selectedEval).first()
    if results is None :
        context = {"a": f"/profile/submission/{id}"}
        return render(request, "docProfile/no_result.html", context)
    else:
        results = Result.objects.filter(eval = selectedEval)
    optimalHs = list()
    optimalLs = list()
    vals = list()
    labels = list()
    for j in results:
        vals.append(j.val)
        optimalHs.append(j.optimalH)
        optimalLs.append(j.optimalL)
        labels.append(j.label)
    fig, ax= plt.subplots()
    index = np.arange(len(labels))
    bar_width = 0.25
    rects1 = plt.bar(index+bar_width, vals, bar_width,color='b', label="Result")
    rects2 = plt.bar(index+2*bar_width, optimalHs, bar_width,color='r', label="Optimal High")
    rects3 = plt.bar(index, optimalLs ,bar_width, color='g', label="Optimal Low")
    plt.xticks(index + bar_width, labels)
    plt.legend()
    pr = mpld3.fig_to_html(fig,template_type="simple")
    plt.close()
    context={"graph":pr, "a": f"/profile/submission/{id}"}
    return render(request, "docProfile/result.html", context)
    # return HttpResponse(pr)

@login_required
def submission(request, id):
    if request.method == 'POST':
        selectedEval = Evaluation.objects.get(e_id=id)
        testList = []
        if selectedEval.test_name == "Bone Marrow Test":
            testList = bone
        elif selectedEval.test_name == "Blood Test":
            testList = blood
        else:
            testList = lipid
        for i in testList:
            resultInstance = Result.objects.filter(eval=selectedEval, label = i[0]).first()
            if resultInstance is None:
                resultInstance = Result()
            resultInstance.eval = selectedEval
            resultInstance.label=i[0]
            name_generator = i[0]
            resultInstance.val=request.POST.get(name_generator)
            resultInstance.optimalH=i[2]
            resultInstance.optimalL=i[1]
            resultInstance.save()
        return HttpResponseRedirect(f'/profile/result/{id}')
    else:
        testList = []
        selectedEval = Evaluation.objects.filter(e_id=id).first()
        if selectedEval is None:
            return HttpResponse("Invalid Result Number")
        else:
            selectedEval = Evaluation.objects.get(e_id=id)
        if selectedEval.test_name == "Bone Marrow Test":
            testList = firstOnly(bone)
        elif selectedEval.test_name == "Blood Test":
            testList = firstOnly(blood)
        else:
            testList = firstOnly(lipid)
        return render(request, "docProfile/submission.html", {"test":testList, "a":(f'/profile/submission/{id}') , "eid":id})
