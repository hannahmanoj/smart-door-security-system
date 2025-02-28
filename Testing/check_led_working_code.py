from gpiozero import LED
from time import sleep

red_led = LED(17)

try:
    while True:
        red_led.on()
        print("LED ON")
        sleep(1)
        red_led.off()
        print("LED OFF")
        sleep(1)
except KeyboardInterrupt:
    print("\nExiting program...")
    red_led.off()