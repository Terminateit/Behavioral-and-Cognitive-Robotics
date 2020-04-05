# The balancing bot is a robot with two wheels on the same axis that should manage to keep its body
# balanced, i.e. upright. The robot has three sensors that encode the orientation and angular velocity of
# its body and the angular velocity of its wheels. Moreover, it has an actuator that controls the angular
# velocity of the wheels. The balancing bot is made of a rectangular body with two cylindrical wheels
# on each side.

# The head of the file should include the instructions for importing of the required components and
# the definition of the class:

import os
import math
import numpy as np
import gym
from gym import spaces
from gym.utils import seeding
import pybullet as p
import pybullet_data

class BalancebotEnv(gym.Env):
    metadata = {
    'render.modes': ['human', 'rgb_array'],
    'video.frames_per_second' : 50
    }
    # The __init__ method performs some initializations and defines the observation and action space of
    # the robot. The space class permits to define the characteristics of these space. In particular, the
    # spaces.Box() method can be used to specify a continuous space, the dimension of the space, and the
    # minimum and maximum value of each dimension. In this example, the output space includes a single
    # value that indicates the commanded variation of wheel velocity. The observation space containsvalues that indicate the inclination of the robot, the angular velocity of the robot, and the angular
    # velocity of the wheels, respectively.


    def __init__(self, render=False):
        self._observation = []
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.Box(np.array([-math.pi, -math.pi, -5]), 
                                            np.array([math.pi, math.pi, 5])) # pitch, gyro, com.sp.


        self.physicsClient = p.connect(p.GUI)  # Graphical version
        # self.physicsClient = p.connect(p.DIRECT)  # Non-Graphical version (for evolving)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # used by loadURDF

        self._seed()
        
        # paramId = p.addUserDebugParameter("My Param", 0, 100, 50)

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        self._assign_throttle(action)
        p.stepSimulation()
        self._observation = self._compute_observation()
        reward = self._compute_reward()
        done = self._compute_done()

        self._envStepCounter += 1

        return np.array(self._observation), reward, done, {}

    def _reset(self):
        # reset is called once at initialization of simulation
        self.vt = 0
        self.vd = 0
        self.maxV = 24.6 # 235RPM = 24,609142453 rad/sec
        self._envStepCounter = 0

        p.resetSimulation()
        p.setGravity(0,0,-10) # m/s^2
        p.setTimeStep(0.01) # sec
        planeId = p.loadURDF("plane.urdf")
        cubeStartPos = [0,0,0.001]
        cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])

        path = os.path.abspath(os.path.dirname(__file__))
        self.botId = p.loadURDF(os.path.join(path, "balancebot_simple.xml"),
                           cubeStartPos,
                           cubeStartOrientation)

        # you *have* to compute and return the observation from reset()
        self._observation = self._compute_observation()
        return np.array(self._observation)

    def _assign_throttle(self, action):
        dv = 0.1
        deltav = [-10.*dv,-5.*dv, -2.*dv, -0.1*dv, 0, 0.1*dv, 2.*dv,5.*dv, 10.*dv][action]
        vt = clamp(self.vt + deltav, -self.maxV, self.maxV)
        self.vt = vt

        p.setJointMotorControl2(bodyUniqueId=self.botId, 
                                jointIndex=0, 
                                controlMode=p.VELOCITY_CONTROL, 
                                targetVelocity=vt)
        p.setJointMotorControl2(bodyUniqueId=self.botId, 
                                jointIndex=1, 
                                controlMode=p.VELOCITY_CONTROL, 
                                targetVelocity=-vt)

    def _compute_observation(self):
        cubePos, cubeOrn = p.getBasePositionAndOrientation(self.botId)
        cubeEuler = p.getEulerFromQuaternion(cubeOrn)
        linear, angular = p.getBaseVelocity(self.botId)
        return [cubeEuler[0],angular[0],self.vt]

    def _compute_reward(self):
        return 0.1 - abs(self.vt - self.vd) * 0.005

    def _compute_done(self):
        cubePos, _ = p.getBasePositionAndOrientation(self.botId)
        return cubePos[2] < 0.15 or self._envStepCounter >= 1500

    def _render(self, mode='human', close=False):
        pass

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)