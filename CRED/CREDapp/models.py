from django.db import models

class Pompe(models.Model):
    """Represente une pompe, une pompe a un statut courant et un journal d'historique du statut."""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=2, unique=True)
    gpio_ONOFF = models.IntegerField(default=0)
    gpio_AM = models.IntegerField(default=0)    #DSI A/M
    gpio_AC = models.IntegerField(default=0)

    
    @classmethod
    def get_by_gpio_ONOFF(self, gpio):
        return self.objects.get(gpio_ONOFF=gpio)
    
    @classmethod
    def get_by_gpio_AM(self, gpio):
        return self.objects.get(gpio_AM=gpio)

    @classmethod
    def get_by_code(self, code):
        return self.objects.get(code=code)
  
    def status_log(self):
        """ Returns the query set of the given statuses"""
        return self.status_set.all().order_by("-date")

    def state_log(self):
        """ Returns the query set of the given statuses"""
        return self.etat_ope_set.all().order_by("-date")

    def current_state(self):
        """The current status is represented by the last status occured in time."""
        return self.etat_ope_set.latest('date')

    def current_status(self):
        """The current status is represented by the last status occured in time."""
        return self.status_set.latest('date_etat')

    def __str__(self):
        return str(self.name)




class Etat_ope(models.Model):
    """ Represents the measured state of the GPIO."""
    pompe = models.ForeignKey(Pompe, on_delete=models.CASCADE)
    etat_ope = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    


class Status(models.Model):
    """Represente le statut d'une pompe selon un log."""
    pompe = models.ForeignKey(Pompe, on_delete=models.CASCADE)

    # Administrative Status codes.
    ARRET = 'OFF'      # objet a l'arrêt
    MARCHE = 'ON'                 # objet en marche et OK
    DEFAUT = 'KO_NACK'       # objet en marche et en défaut sans impact majeur non acquitté
    DEFAUT_ACK = 'KO_ACK'    # objet en marche et en défaut sans impact majeur acquitté
    ALARME = 'AL_NACK'         # objet en marche et en défaut avec impact majeur non acquitté
    ALARME_ACK = 'AL_ACK'     # objet en marche et en défaut avec impact majeur acquitté

    # Existing states
    ETATS = (
        (ARRET, 'Arrêt'),
        (MARCHE, 'Marche'),
        (DEFAUT, 'Défaut non acquitté'),
        (DEFAUT_ACK, 'Défaut acquitté'),
        (ALARME, 'Alarme non acquittée'),
        (ALARME_ACK, 'Alarme acquittée')
    )

    # champ etat.
    status = models.CharField(
        max_length=7,
        choices=ETATS,
        default=MARCHE
    )
    # champ date de mise a jour de l'état
    date_etat = models.DateTimeField('date', auto_now_add=True)
    
    # champ date d'acquittement de changement d'état ( en cas de défaut et d'alarme)
    date_ack = models.DateTimeField('date', auto_now_add=False)

    def __str_(self):
        return str(self.status) + " at " + self.date_etat.strftime("%Y-%m-%d %H:%M:%S")
