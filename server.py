# from flask import Flask, request
#
# app = Flask(__name__)
# pressedButtons = []
#
#
# @app.route('/post', methods=['POST'])
# def post():
#     msg = request.data.decode('utf8')
#     if msg == 'a':
#         pressedButtons.clear()
#     else:
#         pressedButtons.append(msg)
#     if len(pressedButtons) == 2:
#         with open('pressed', mode='w') as f:
#             f.write(pressedButtons[0] + ',' + pressedButtons[1])
#     return ''
#
#
# app.run(host='0.0.0.0', port=6010)
import serial


ser = serial.Serial('/dev/rfcomm0', 9600)

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

