from gpiozero import MotionSensor

pir = MotionSensor(4)

try:
    while True:
        pir.wait_for_motion()
        print("Motion Detected")
        pir.wait_for_no_motion()
        print("Motion Stopped")
except KeyboardInterrupt:
    print("\nExiting program...")
    pir.close()