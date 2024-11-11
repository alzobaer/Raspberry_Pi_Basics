import pigpio
import time

class ServoController:
    def __init__(self, horizontal_pin, vertical_pin):
        self.pi = pigpio.pi()
        self.horizontal_pin = horizontal_pin
        self.vertical_pin = vertical_pin
        self.horizontal_angle = 1500
        self.vertical_angle = 1500
        self.pi.set_servo_pulsewidth(self.horizontal_pin, self.horizontal_angle)
        self.pi.set_servo_pulsewidth(self.vertical_pin, self.vertical_angle)

    def set_angle(self, h_angle, v_angle):
        # Limit angle range for safety
        self.horizontal_angle = max(1000, min(2000, self.horizontal_angle + h_angle))
        self.vertical_angle = max(1000, min(2000, self.vertical_angle + v_angle))
        
        # Move servos to new angles
        self.pi.set_servo_pulsewidth(self.horizontal_pin, self.horizontal_angle)
        self.pi.set_servo_pulsewidth(self.vertical_pin, self.vertical_angle)

    def stop(self):
        self.pi.set_servo_pulsewidth(self.horizontal_pin, 0)
        self.pi.set_servo_pulsewidth(self.vertical_pin, 0)
        self.pi.stop()
