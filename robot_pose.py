import socket
import json
import numpy as np


def robot_pose(float_0, float_1, float_2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9395))
    list=[(0,float_0), (1,float_1), (2,float_2)]
    for (servo_index,float_) in list:

        command = {'start': ['servo_write', servo_index, np.degrees(np.arccos(-float_)), 0, 0]}
        command_str = json.dumps(eval(str(command))) + '\n'
        command_bytes = bytes(command_str, 'utf8')
        s.sendall(command_bytes)
    s.close()