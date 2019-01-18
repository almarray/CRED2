from django.apps import AppConfig

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    0

class CredappConfig(AppConfig):
    name = 'CREDapp'

    def ready(self):
        """ Code executed on application start. """
        self.is_on_rpi = False
        try:
            import RPi.GPIO as GPIO
            self.is_on_rpi = True
        except (ImportError, RuntimeError):
            self.is_on_rpi = False
        if self.is_on_rpi:
            print("Initialization sequence on RPi...")
            self.config()
        else:
            print("Initialization sequence out of RPi...")
            self.init_status()



    def init_status(self):
        """ initialize initial status of all pomps to true """
        # load all pomps from DB
        from .models import Pompe, Etat_ope
        pompes = Pompe.objects.all() # is an array     
        print('def init_status: pompes', pompes)
        etat_ope = Etat_ope.objects.all()
        print('def init_status: etat_ope', etat_ope)
        # for each, initialize object State
        for p in pompes:	    
            s = Etat_ope(pompe = p, etat_ope = True)
        #save object state in DB
        s.save()
        


    def set_status_callback(self, channel):
        """
        :param channel:
        :return:
        """
        from .models import Pompe, Etat_ope
        print("IO change detected on " + str(channel) + " - " + str(GPIO.input(channel)))
        p = Pompe.get_by_gpio_ONOFF(channel)
        current_state = p.current_state().etat_ope
        measured_state = bool(GPIO.input(channel))

        if current_state != measured_state:
            new_state = Etat_ope(pompe=p, etat_ope=measured_state)
            new_state.save()

    

    def config(self):
        """
        Configure RPi to actually run correctly
        :return:
        """
        print("Start config : " + str(self.is_on_rpi) )
        if self.is_on_rpi:
            from .models import Pompe, State
            GPIO.setmode(GPIO.BCM)
            pompes = Pompe.objects.all()
            for p in pompes:
                #print("Configuring : " + str(p.name) + " (" + str(p.gpio)  + ")")
                print("Configuring : " + str(p.name) + " (" + str(p.gpio_ONOFF) + str(p.gpio_AM) + ")")
                #GPIO.setup(p.gpio, GPIO.IN)
                GPIO.setup(p.gpio_ONOFF, GPIO.IN)
                GPIO.setup(p.gpio_AM, GPIO.IN)
                # Initialize state
                new_state = Etat_ope(pompe=p, etat_ope=bool(GPIO.input(p.gpio)))
                new_state.save()
                #GPIO.add_event_detect(p.gpio, GPIO.BOTH, callback=self.set_status_callback, bouncetime=200)
                GPIO.add_event_detect(p.gpio_ONOFF, GPIO.BOTH, callback=self.set_status_callback, bouncetime=200)
                GPIO.add_event_detect(p.gpio_AM, GPIO.BOTH, callback=self.set_status_callback, bouncetime=200)
                