import socket
import json
import math
from scipy.spatial.distance import euclidean
import random
import numpy as np
import cv2 
import sys
import gym
from robot_pose import robot_pose
from mask_and_centroid_functions import make_mask
from mask_and_centroid_functions import get_centroid




class RobotArmEnv(gym.Env):
     

    def __init__(self):
        super().__init__()
    
        self.observation_space = gym.spaces.Box(low=0.0, high=1.0, shape=(4,), dtype=np.float32)
        self.action_space = gym.spaces.Box(np.array([-1.0,-1.0,-1.0]),np.array([-np.sqrt(2)/2, -np.sqrt(2)/2, 1.0]), dtype=np.float32)
        
    def reset(self):
        self.gripper_pos = np.random.rand(2)
        
        # Center coordinates
        self.centre_x = random.randint(0, 340)
        self.centre_y = random.randint(0, 280)
        self.centre_coordinates = (self.centre_x, self.centre_y)
        
        self.target_pos = np.array([self.centre_x/640,self.centre_y/480])
        observation = np.concatenate((self.gripper_pos, self.target_pos), axis=None).astype(np.float32)
        return observation
    def step(self,action):
        print(action)
        robot_pose(action[0], action[1], action[2])
        
        cap=cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        ret,frame=cap.read()
        
        mask = make_mask(frame)
        
        centroid = get_centroid(mask)
        
        cx, cy = centroid
        
        frame[int(cy-2):int(cy+2), int(cx-2):int(cx+2), :] = (0, 0, 0)
        
        height, width, depth = frame.shape
        
        gripper_pos_x, gripper_pos_y = cx / width, cy / height
        self.gripper_pos = np.array([gripper_pos_x, gripper_pos_y])
        
        print(self.centre_coordinates)
 
        # Radius of circle
        radius = 5
  
        # Red colour in BGR
        colour = (0, 0, 255)
        # Line thickness of -1 px
        thickness = -1
 
        frame = cv2.circle(frame, self.centre_coordinates, radius, colour, thickness)
    
        error = euclidean(self.target_pos, self.gripper_pos)    
        
        print(error)
        
        cv2.imshow("frame",frame)
    
        key=cv2.waitKey(1)
        
        # Reward and done
        if error >= .5:
            reward=-np.exp(100*error)
        elif .4 <= error <.5:
            reward = -100*error
        elif .3 <= error <.4:
            reward = -20*error
        elif .2 <= error <.3:
            reward = -10*error
        elif .1 <= error <.2:
            reward = 100*error
        elif .1 <= error <.05:
            reward = (1/error)**2
        else:
            reward = np.exp(1/error)
        print(reward)
        done = False
        if reward > 100 or reward <-20:
            done = True
        
        observation = np.concatenate((self.gripper_pos, self.target_pos), axis=None).astype(np.float32)
        
        return observation, reward, done, {}