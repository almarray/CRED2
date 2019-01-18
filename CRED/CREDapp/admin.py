from django.contrib import admin

# Register your models here.
from .models import Pompe
from .models import Etat_ope
from .models import Status

admin.site.register(Pompe)
admin.site.register(Etat_ope)
admin.site.register(Status)