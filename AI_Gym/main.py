import gym
import time
gym.logger.set_level(40)

env = gym.make('CartPole-v0') #  it's the environment with a cart that can move along the x axes with a pole attached on the top through a passive joint

env.reset() #  initializes the position of the agent and of the environment

for i in range(200):
    env.render() #  displays graphically the agent and the environment

    time.sleep(0.1)

    observation, reward, done, info = env.step(env.action_space.sample()) #  receives as input the desired state of the actuator, updates the actuators, performs a simulation step, computes the reward for the step, and checks the conditions for terminating the episode.
    # action_space.sample() return a random action or a vector of random actions suitable for the current environment

    # to know type and dimensionality of the observation and action space:
    print ('Iteration # ', i)
    print(env.action_space) # The action includes an integer value in the range [1, 2] that specifies whether the actuator push the cart left or right.

    print(env.observation_space) #the observation includes the position and the velocity of the cart along the x axes, the angle of the pole, and the velocity of the tip of the pole

    print(env.observation_space.high)

    print(env.observation_space.low)

    # print(env.action_space.high)

    # print(env.action_space.low)
    # The object Box indicates a vector of real values and the first element of the object indicates the number of elements forming the vector. 
    # The object Discrete indicates integer positive values, and the first element of the object indicates the range of the integer values.


    if done == True:
        env.reset()
env.close()