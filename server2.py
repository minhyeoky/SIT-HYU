import serial


ser = serial.Serial('/dev/rfcomm1', 9600)

arrows = ['0', '1', '2', '3', '4', '5', '6', '7']

while True:
    print("RUNNING..")
    key = ser.read().decode('utf8')
    pressedButtons = ['1', '1', '1', '1', '1', '1', '1', '1']
    print(key)
    for i in range(len(arrows)):
        if key == arrows[i]:
            pressedButtons[i] = '0'
    with open('pressed', mode='w') as f:
        msg = ','.join(pressedButtons)
        f.write(msg)
