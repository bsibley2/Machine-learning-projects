import socket
import json
import math
from scipy.spatial.distance import euclidean
import random
import numpy as np
import cv2 
import sys
import os
import gym
import stable_baselines3 as sb3
from robot_arm_gym_environment import RobotArmEnv

env = RobotArmEnv()
agent = sb3.SAC(
    policy="MlpPolicy",
    env=env,tensorboard_log="./logs/")

agent.learn(total_timesteps=2000)

# tensorboard --logdir=logs