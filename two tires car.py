import machine
from machine import Pin,PWM,ADC
import time

class Moteur:
    def __init__(self,pin1,pin2,en):
        
        self.en  = PWM(Pin(en), freq=500)
        self.pin1 = Pin(pin1,Pin.OUT)
        self.pin2 = Pin(pin2,Pin.OUT)
        
    def avancer(self,vitesse):
        self.en.duty(vitesse)
        self.pin1.on()
        self.pin2.off()
        
    def reculer(self,vitesse):
        self.en.duty(vitesse)
        self.pin1.off()
        self.pin2.on()
                  
    def stop(self):
        self.en.duty(0)
        self.pin1.off()
        self.pin2.off()
        
class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.
    The timeouts received listening to echo pin are converted to OSError('Out of range')
    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin. 
        By default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)
 
        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)
 
    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex
 
    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()
 
        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
        mm = pulse_time * 100 // 582
        return mm
 
    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()
 
        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms
import math 

# originally by Radomir Dopieralski http://sheep.art.pl
# from https://bitbucket.org/thesheep/micropython-servo

class Servo:
    """
    A simple class for controlling hobby servos.
    Args:
        pin (machine.Pin): The pin where servo is connected. Must support PWM.
        freq (int): The frequency of the signal, in hertz.
        min_us (int): The minimum signal length supported by the servo.
        max_us (int): The maximum signal length supported by the servo.
        angle (int): The angle between the minimum and maximum positions.
    """
    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=190):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.pwm = PWM(Pin(pin), freq=freq, duty=0)

    def write_us(self, us):
        """Set the signal to be ``us`` microseconds long. Zero disables it."""
        if us == 0:
            self.pwm.duty(0)
            return
        us = min(self.max_us, max(self.min_us, us))
        duty = us * 1024 * self.freq // 1000000
        self.pwm.duty(duty)

    def write_angle(self, degrees=None, radians=None):
        """Move to the specified angle in ``degrees`` or ``radians``."""
        if degrees is None:
            degrees = math.degrees(radians)
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)
        
        
class Voiture:
    def __init__(self,motGauche,motDroit,capteur,servo):
        
        self.motGauche = Moteur(motGauche[0],motGauche[1],motGauche[2])
        self.motDroit = Moteur(motDroit[0],motDroit[1],motDroit[2])
       
        self.servo = Servo(servo)
        
        self.capteur = HCSR04(capteur[0],capteur[1])
        
                
                
    def stop(self): # s'arr猫ter
        self.motGauche.stop()
        self.motDroit.stop()
        
              
    def avancer(self, vitesse): #aller devant
        self.motGauche.avancer(vitesse)
        self.motDroit.avancer(vitesse)
        
            
    def reculer(self, vitesse): #aller arri猫re
        self.motGauche.reculer(vitesse)
        self.motDroit.reculer(vitesse)
       
    def tournerAGauche(self,vitesse):
        self.motGauche.avancer(int(vitesse/3))
        self.motDroit.avancer(vitesse)
    
    def tournerADroite(self,vitesse):
        self.motGauche.avancer(vitesse)
        self.motDroit.avancer(int(vitesse/3))
        
    def tourner_capteur(self,angle):
        self.servo.write_angle(angle)
        
    def distance(self):
        return self.capteur.distance_mm()

