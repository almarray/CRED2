from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http import HttpRequest
from django.db import models
from .models import Pompe
from .models import Status
from .models import Etat_ope
from datetime import datetime
from django.utils import timezone



def index(request):
    pompes = Pompe.objects.all()
    context = {'pompes': pompes }
    if (request.method == 'POST'): # message sent when pressing buttons in status page
        print('POST', request.POST)
        for k in request.POST.keys():      
            if k.isnumeric():
                # k is the string for the received key
                # get the related pump instance
                pump_id = Pompe.objects.get(pk=int(k))
                #build the new forced state for this pump
                if (request.POST[k]=='OPE'):
                    forced_state = Etat_ope(pompe = pump_id, etat_ope = 'True')                
                    forced_state.save()                                         # save pump state in DB
                if (request.POST[k]=='NOP'):
                    forced_state = Etat_ope(pompe = pump_id, etat_ope = 'False')
                    forced_state.save()
                if (request.POST[k]=='ON'):
                    forced_status=Status(pompe = pump_id)
                    forced_status.status = 'ON'
                    forced_status.date_ack = datetime(1999,1,1,1,1,2,tzinfo=timezone.utc)
                    forced_status.save()
                if (request.POST[k]=='OFF'):
                    forced_status = Status(pompe = pump_id)
                    forced_status.status = 'OFF'
                    forced_status.date_ack = datetime(1999,1,1,1,1,3,tzinfo=timezone.utc)
                    forced_status.save()                    
                if (request.POST[k]=='ARRET COMMANDE'):
                    forced_status = Status(pompe = pump_id, status = 'OFF', date_ack = datetime(1999,1,1,1,1,1,tzinfo=timezone.utc))
                    forced_status.save()
                if (request.POST[k]=='KO_NACK'):
                    forced_status = Status(pompe = pump_id, status = 'KO_NACK', date_ack = datetime(1999,1,1,1,1,1,tzinfo=timezone.utc))
                    forced_status.save()
                if (request.POST[k]=='KO_ACK'):
                    forced_status = Status(pompe = pump_id, status = 'KO_ACK', date_ack = datetime(1999,1,1,1,1,1,tzinfo=timezone.utc))
                    forced_status.save()    
                if (request.POST[k]=='AL_NACK'):
                    forced_status = Status(pompe = pump_id, status = 'AL_NACK', date_ack = datetime(1999,1,1,1,1,1,tzinfo=timezone.utc))
                    forced_status.save()
                if (request.POST[k]=='AL_ACK'):
                    forced_status = Status(pompe = pump_id, status = 'AL_ACK', date_ack = datetime(1999,1,1,1,1,1,tzinfo=timezone.utc))
                    forced_status.save()
    pompes = Pompe.objects.all()
    context = {'pompes': pompes }
    
    return render(request, 'CREDapp/index.html', context)


def log(request, pompe_id):
    try:
        pompe = Pompe.objects.get(pk=pompe_id)
        context = {'pompe': pompe, 'logs': pompe.state_log()}
    except Pompe.DoesNotExist:
        raise Http404("Pompe object does not exist.")
    ## If pompe not found send 404
    return render(request, 'CREDapp/log.html', context)
# Create your views here.
