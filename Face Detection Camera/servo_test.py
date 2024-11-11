import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for servos
horizontal_servo_pin = 17  # replace with your GPIO pin for horizontal servo
vertical_servo_pin = 18    # replace with your GPIO pin for vertical servo

# Set up pins as output
GPIO.setup(horizontal_servo_pin, GPIO.OUT)
GPIO.setup(vertical_servo_pin, GPIO.OUT)

# Set PWM frequency to 50Hz (common for servos)
horizontal_pwm = GPIO.PWM(horizontal_servo_pin, 50)
vertical_pwm = GPIO.PWM(vertical_servo_pin, 50)

# Start PWM with 0 duty cycle (stops servo from moving)
horizontal_pwm.start(0)
vertical_pwm.start(0)

def set_angle(pwm, angle):
    """Convert the angle to duty cycle and set it on the PWM."""
    duty_cycle = 2 + (angle / 18)  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Allow time for servo to move to position
    pwm.ChangeDutyCycle(0)  # Stop sending signals to avoid jitter

try:
    while True:
        # Get user input for horizontal and vertical angles
        h_angle = int(input("Enter horizontal angle (0-180): "))
        v_angle = int(input("Enter vertical angle (0-180): "))
        
        # Move horizontal and vertical servos to the specified angles
        set_angle(horizontal_pwm, h_angle)
        set_angle(vertical_pwm, v_angle)

except KeyboardInterrupt:
    print("Program stopped by User")

finally:
    # Cleanup GPIO settings
    horizontal_pwm.stop()
    vertical_pwm.stop()
    GPIO.cleanup()
