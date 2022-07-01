import pygame
import json
import socket
import threading
import asyncio
import math

TARGET_ANGLES = [0.0] * 3
CURRENT_ANGLES = [0.0] * 3

VIEWPORT_W = 1024
VIEWPORT_H = 768
ARM_LEN = 200

# Thread to update the angles
class ClientThread(threading.Thread):
    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def run(self):
        global TARGET_ANGLES

        while True:
            # Read line from socket
            line = ''

            while True:
                c = str(self.socket.recv(1, socket.MSG_WAITALL), 'ascii')

                if c == '\n':
                    break
                else:
                    line += c

            # Parse JSON
            print("SERVER GOT:", line)
            data = json.loads(line)

            if 'start' in data:
                data = data['start']

                if len(data) == 5:
                    funcname, p1, p2, p3, p4 = data

                    if funcname == 'servo_write':
                        servo_index = p1
                        angle = p2

                        if servo_index < len(TARGET_ANGLES) and servo_index >= 0:
                            TARGET_ANGLES[servo_index] = angle / 180 * 3.1415   # Go from degrees to radians


# Server that listens to commands to make the arm move
class ServerThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('0.0.0.0', 9395))
        self.s.listen(10)

        self.threads = []

    def run(self):
        while True:
            # Accept a client
            conn, addr = self.s.accept()

            # Create a thread
            t = ClientThread(conn)
            t.start()

            self.threads.append(t)

server = ServerThread()
server.start()

# Display the robot arm
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((VIEWPORT_W, VIEWPORT_H))
clock = pygame.time.Clock()

while True:
    surf = pygame.Surface(screen.get_size())

    # Clear the screen
    pygame.draw.rect(surf, (255, 255, 255), surf.get_rect())

    # Draw the robot segments as rotated rectangles
    x = VIEWPORT_W * 0.8
    y = VIEWPORT_H - 50.
    angle = 0.0             # 0 means upwards

    for joint_index in range(len(TARGET_ANGLES)):
        # Update the current position
        CURRENT_ANGLES[joint_index] += 0.1 * (TARGET_ANGLES[joint_index] - CURRENT_ANGLES[joint_index])

        # Compute end coordinates
        new_angle = angle + CURRENT_ANGLES[joint_index]
        new_y = y - ARM_LEN * math.cos(new_angle)
        new_x = x - ARM_LEN * math.sin(new_angle)

        # Make a polygon
        dx = 10 * math.cos(new_angle)
        dy = -10. * math.sin(new_angle)

        points = [
            (x - dx, y - dy),
            (x + dx, y + dy),
            (new_x + dx, new_y + dy),
            (new_x - dx, new_y - dy),
        ]

        pygame.draw.polygon(surf, color=[0, 0, 0], points=points)

        # Go to the next segment
        x = new_x
        y = new_y
        angle = new_angle

    # Add a blue dot at the tip of the arm
    pygame.draw.circle(surf, color=[0, 0, 255], center=(x, y), radius=0.1*ARM_LEN)

    # Display
    clock.tick(60)
    screen.blit(surf, (0, 0))
    pygame.event.pump()
    pygame.display.flip()
