from flask import Flask, request
import RPi.GPIO as GPIO
import time

# Motor GPIO setup
MOTOR_PIN = 18  # GPIO 18 (Pin 12 on the Raspberry Pi)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)
pwm = GPIO.PWM(MOTOR_PIN, 50)  # PWM frequency set to 50Hz
pwm.start(0)

# Flask app setup
app = Flask(__name__)

# Previous heading to compare changes
previous_heading = None

def spin_motor(direction):
    """
    Function to control motor spinning.
    """
    if direction == "left":
        pwm.ChangeDutyCycle(30)  # Adjust duty cycle for left turn (lower duty cycle)
        time.sleep(0.5)
        pwm.ChangeDutyCycle(0)  # Stop motor
    elif direction == "right":
        pwm.ChangeDutyCycle(70)  # Adjust duty cycle for right turn (higher duty cycle)
        time.sleep(0.5)
        pwm.ChangeDutyCycle(0)  # Stop motor

@app.route('/turn', methods=['POST'])
def handle_turn():
    """
    Handle the incoming POST request with heading data.
    """
    global previous_heading

    data = request.get_json()
    heading = data.get("heading", 0)  # Get heading from the incoming data

    # If there's a previous heading to compare to
    if previous_heading is not None:
        heading_difference = heading - previous_heading

        # Determine direction of turn
        if heading_difference > 5:  # Right turn threshold
            spin_motor("right")
        elif heading_difference < -5:  # Left turn threshold
            spin_motor("left")

    # Update the previous heading for the next check
    previous_heading = heading

    return "OK", 200

if __name__ == '__main__':
    # Start the Flask web server to listen for POST requests
    app.run(host='0.0.0.0', port=5000)
