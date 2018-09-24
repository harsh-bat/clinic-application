from django.contrib import admin

# Register your models here.
from .models import Patient
from .models import Result
from .models import Evaluation

admin.site.register(Patient)
admin.site.register(Result)
admin.site.register(Evaluation)
