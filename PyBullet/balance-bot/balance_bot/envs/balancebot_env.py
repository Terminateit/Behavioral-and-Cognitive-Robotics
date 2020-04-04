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
        # action encodes the torque applied by the motor of the wheels
        self.action_space = spaces.Box(-1., 1., shape=(1,), dtype='float32')
        # observation encodes pitch, gyro, com.sp.
        self.observation = []
        self.observation_space = spaces.Box(np.array([-math.pi, -math.pi, -5]),
        np.array([math.pi, math.pi, 5]), dtype='float32')
        self.connectmode = 0
        # starts without graphic by default
        self.physicsClient = p.connect(p.DIRECT)
        # used by loadURDF
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.seed()

    # The seed() method sets the seed of the random number generator that, in turn, influence the initial
        # conditions experienced during evaluation episodes.
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    # The reset() method initializes the position, velocity, and orientation of the robot, load the files
    # containing the description of the plane and of the robot, and compute and return the observation. The
    # orientation of the robot is varied randomly within a given range.
    def reset(self):
        self.vt = 0
        # current velocity pf the wheels
        self.maxV = 24.6 # max lelocity, 235RPM = 24,609142453 rad/sec
        self.envStepCounter = 0
        p.resetSimulation()
        p.setGravity(0, 0,-10) # m/s^2
        p.setTimeStep(0.01)
        # the duration of a step in sec
        planeId = p.loadURDF("plane.urdf")
        robotStartPos = [0,0,0.001]
        robotStartOrientation = p.getQuaternionFromEuler([self.np_random.uniform(low=-
        0.3, high=0.3),0,0])
        path = os.path.abspath(os.path.dirname(__file__))
        self.botId = p.loadURDF(os.path.join(path, "balancebot_simple.xml"),
        robotStartPos,
        robotStartOrientation)
        self.observation = self.compute_observation()
        return np.array(self.observation)
        
    #     The step() method sets the state of the actuators, advances the simulation for a step, computes the
    # new observation, computes the reward, checks whether the condition for terminating the evaluation
    # episode are satisfied or not, and increases the step counter. The method receives as input the action
    # to perform and returns the observation, the reward, a Boolean value that indicates whether the episode
    # should terminate, and an empty dictionary.
    def step(self, action):
        self.set_actuator(action)
        p.stepSimulation()
        self.observation = self.compute_observation()
        reward = self.compute_reward()
        done = self.compute_done()
        self.envStepCounter += 1
        status = "Step " + str(self.envStepCounter) + " Reward " +
        '{0:.2f}'.format(reward)
        p.addUserDebugText(status, [0,-1,3], replaceItemUniqueId=1)
        return np.array(self.observation), reward, done, {}

    # The render() method connects the graphic display for the visualization of the robot and of the
    # environment

    def render(self, mode='human', close=False):
        if (self.connectmode == 0):
            p.disconnect(self.physicsClient)
        # connect the graphic renderer
            self.physicsClient = p.connect(p.GUI)
            self.connectmode = 1
        pass
        
    # Finally, the following four methods: update the desired velocity of the actuators; compute the
    # observation on the basis of the current position, orientation and velocity of the robot; compute the
    # reward; check whether the episode should terminate.

    def set_actuator(self, action):
        deltav = action[0]
        vt = np.clip(self.vt + deltav, -self.maxV, self.maxV)
        self.vt = vt
        p.setJointMotorControl2(bodyUniqueId=self.botId,
        jointIndex=0,
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity=vt)
        p.setJointMotorControl2(bodyUniqueId=self.botId,
        jointIndex=1,
        controlMode=p.VELOCITY_CONTROL,
        targetVelocity=-vt)

    def compute_observation(self):
        robotPos, robotOrn = p.getBasePositionAndOrientation(self.botId)
        robotEuler = p.getEulerFromQuaternion(robotOrn)
        linear, angular = p.getBaseVelocity(self.botId)
        return (np.array([robotEuler[0],angular[0],self.vt], dtype='float32'))

    def compute_reward(self):
        # receive a bonus of 1 for balancing and pay a small cost proportional to speed
        return 1.0 - abs(self.vt) * 0.05

    def compute_done(self):
        # episode ends when the barycentre of the robot is too low or after 500 steps
        cubePos, _ = p.getBasePositionAndOrientation(self.botId)
        return cubePos[2] < 0.15 or self.envStepCounter >= 500


