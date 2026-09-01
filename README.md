# smart door security system

a raspberry pi security prototype that combines **facial recognition, motion detection, GPIO hardware control, and SQLite logging**

when a PIR sensor detects someone approaching, the pi camera captures their face and compares it against stored face encodings. Recognised users can trigger a relay or solenoid lock, while access events are recorded locally

## tech stack

- **software:** Python, OpenCV, `face_recognition`, NumPy, SQLite
- **hardware:** Raspberry Pi, Pi Camera, PIR sensor, LEDs, relay, solenoid lock
