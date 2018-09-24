from django.urls import path
from docProfile import views
app_name = 'docProfile'
urlpatterns=[
	path('', views.index, name="index"),
	path('patient/<int:id>', views.patient, name="patient"),
	path('result/<int:id>', views.result, name="result"),
	path('submission/<int:id>', views.submission, name="submission")
]
