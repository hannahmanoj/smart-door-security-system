from gpiozero import LED, MotionSensor
from signal import pause
import sys

# Initialize the LED and MotionSensor
red_led = LED(17)
pir = MotionSensor(4)

# Ensure the LED is off initially
red_led.off()

def motion_detected():
    print("Motion Detected")
    red_led.on()

def motion_stopped():
    print("Motion Stopped")
    red_led.off()

try:
    # Assign the event handlers
    pir.when_motion = motion_detected
    pir.when_no_motion = motion_stopped

    # Keep the script running
    pause()

except KeyboardInterrupt:
    # Handle the KeyboardInterrupt (Ctrl+C) gracefully
    print("\nExiting program...")
    red_led.off()
    pir.close()
    sys.exit(0)