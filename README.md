# Smart Car Controller

This Python script is designed to control a smart car using MicroPython and the ESP32 microcontroller. The code provides classes for motor control (Moteur), ultrasonic distance sensing (HCSR04), and servo motor control (Servo). Additionally, there is a class (Voiture) that integrates these components for comprehensive smart car functionality.
Requirements

    MicroPython environment on an ESP32 microcontroller.
    Appropriate connections for motors, ultrasonic sensor, and servo motor.

Motor Control (Moteur) Class

The Moteur class provides methods for controlling motors. It utilizes Pulse Width Modulation (PWM) for speed control. The methods include:

    avancer(vitesse): Move forward at the specified speed.
    reculer(vitesse): Move backward at the specified speed.
    stop(): Stop the motor.

Ultrasonic Sensor (HCSR04) Class

The HCSR04 class facilitates the use of the HC-SR04 ultrasonic sensor for distance measurement. It includes methods:

    distance_mm(): Get the distance in millimeters without floating-point operations.
    distance_cm(): Get the distance in centimeters with floating-point operations.

Servo Control (Servo) Class

The Servo class is responsible for controlling a hobby servo motor. It allows setting the signal length in microseconds and moving to a specified angle in degrees or radians.
Smart Car (Voiture) Class

The Voiture class integrates the motor control, ultrasonic sensing, and servo control for a comprehensive smart car setup. It includes methods such as:

    stop(): Stop the car.
    avancer(vitesse): Move the car forward at the specified speed.
    reculer(vitesse): Move the car backward at the specified speed.
    tournerAGauche(vitesse): Turn the car to the left.
    tournerADroite(vitesse): Turn the car to the right.
    tourner_capteur(angle): Rotate the ultrasonic sensor to a specific angle.
    distance(): Get the distance measured by the ultrasonic sensor.

Motor Control (Moteur) Standalone Class

There is also a standalone Moteur class for simpler motor control without the additional smart car functionality.
Usage

    Set up your ESP32 microcontroller with MicroPython.
    Ensure proper connections for motors, ultrasonic sensor, and servo motor.
    Copy the provided classes into your MicroPython environment.
    Instantiate the classes and utilize the methods for controlling your smart car.

