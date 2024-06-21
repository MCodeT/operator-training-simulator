import serial.tools.list_ports
import time

def identify_arduino():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(port.device)
        arduino = serial.Serial(port.device, 9600)
        time.sleep(2)  # Wait for the Arduino to initialize
        arduino.write(b'IDENTIFY\n')
        identifier = arduino.readline().decode('utf-8').strip()
        arduino.write(b'CLOSE\n')
        arduino.close()
        return identifier
    return None

identifier = identify_arduino()

if identifier == "Taping":
    import taping as interface
    print("Taping detected")
elif identifier == "Crimping":
    import crimping as interface
elif identifier == "Slots":
    #import slots as interface
    pass
else:
    print("No valid Arduino detected")
    exit()

interface.run()