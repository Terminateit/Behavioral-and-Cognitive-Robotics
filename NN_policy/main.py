import gym
import time
import numpy as np
gym.logger.set_level(40)

environment = 0 # 0 - Cart
                # 1 - Pendulum

technique = 1   # 0 - NN without Updates
                # 1 - Evolutionary Strategy



episodes = 10 # number of episodes
networks = 10 # number of neural networks
steps = 200 # number of steps
individuals = networks//2 # number of individuals

pvariance = 0.1 # variance of initial parameters
ppvariance = 0.02 # variance of perturbations
nhiddens = 5 # number of hidden neurons

if environment == 0:
    env = gym.make('CartPole-v0') #  it's the environment with a cart that can move along the x axes with a pole attached on the top through a passive joint
    print('\nenvironment: CartPole-v0')
else:
    env = gym.make('Pendulum-v0') #  it's the environment with a Pendulum  
    print('\nenvironment: Pendulum-v0')  

# The policy consists of feed-forward neural network with a layer of sensory neurons encoding the state
# of the observation, a layer of internal neurons, and a layer of motor neurons that encode the action
# state. The activation of the internal and motor neurons is computed with the tanh function. We assume
# that observation is constituted by a vector of real numbers (4 in the case of the CartPole-v0) and that
# action is constituted by a vector of real numbers or by an integer in the range [1, amax]. In the latter
# case, the network includes amax output neurons and the action is set to the index of the most activated
# output neuron. In the CartPole-v0 action is constituted by an integer in the range [1,2] and
# consequently the network should include two motor neurons.

# the number of inputs and outputs depends on the problem
# we assume that observations consist of vectors of continuous value
# and that actions can be vectors of continuous values or discrete actions
ninputs = env.observation_space.shape[0]
if (isinstance(env.action_space, gym.spaces.box.Box)):
 noutputs = env.action_space.shape[0]
else:
 noutputs = env.action_space.n
# initialize the training parameters randomly by using a gaussian distribution with average 0.0 and variance 0.1
# biases (thresholds) are initialized to 0.0
W1 = np.random.randn(nhiddens,ninputs, networks) * pvariance # first layer
W2 = np.random.randn(noutputs, nhiddens, networks) * pvariance # second layer
b1 = np.zeros(shape=(nhiddens, 1, networks)) # bias first layer
b2 = np.zeros(shape=(noutputs, 1, networks)) # bias second layer

if technique == 1:
    print('technique - Evolutionary Strategy\n')
    time.sleep(2)
    for episode in range(episodes):
        print('episode # ', episode)
        reward_sum = np.zeros(networks, dtype=float)
        for network in range(networks):
            observation = env.reset() #  initializes the position of the agent and of the environment
            for i in range(steps):
                if network == networks//2+1:
                    env.render() #  displays graphically the agent and the environment

                # convert the observation array into a matrix with 1 column and ninputs rows

                observation.resize(ninputs,1)
                # compute the netinput of the first layer of neurons
                Z1 = np.dot(W1[:,:,network], observation) + b1[:,:,network]
                # compute the activation of the first layer of neurons with the tanh function
                A1 = np.tanh(Z1)
                # compute the netinput of the second layer of neurons
                Z2 = np.dot(W2[:,:,network], A1) + b2[:,:,network]
                # compute the activation of the second layer of neurons with the tanh function
                A2 = np.tanh(Z2)
                # if actions are discrete we select the action corresponding to the most activated unit
                if (isinstance(env.action_space, gym.spaces.box.Box)):
                    action = A2
                else:
                    action = np.argmax(A2)

                # time.sleep(0.1)

                observation, reward, done, info = env.step(action)
                reward_sum[network] = reward_sum[network] + reward
        
                # # if done == True:
                #     env.reset()

        best = reward_sum.argsort()[-individuals:][::-1] # find the best models
        worst = reward_sum.argsort()[:individuals][::-1] # pick the worst models
        print('Reward', reward_sum)
        print('Best', best,'\n')

        # Update the worst models changing them by the best ones
        W1[:, :, worst] = W1[:, :, best] + np.random.randn(nhiddens, ninputs, individuals) * ppvariance
        W2[:, :, worst] = W2[:, :, best] + np.random.randn(noutputs, nhiddens, individuals) * ppvariance
        b1[:, :, worst] = b1[:, :, best] + np.random.randn(nhiddens, 1, individuals) * ppvariance
        b2[:, :, worst] = b2[:, :, best] + np.random.randn(noutputs, 1, individuals) * ppvariance

    # Post-Evaluation
    really_best = best[-1]
else:
    print('technique - Neural Network without updates (random)\n')
    time.sleep(2)
    for episode in range(episodes):
        print('episode # ', episode)
        reward_sum = np.zeros(networks, dtype=float)
        for network in range(networks):
            observation = env.reset() #  initializes the position of the agent and of the environment
            for i in range(steps):
                if network == networks//2+1:
                    env.render() #  displays graphically the agent and the environment

                # convert the observation array into a matrix with 1 column and ninputs rows

                observation.resize(ninputs,1)
                # compute the netinput of the first layer of neurons
                Z1 = np.dot(W1[:,:,network], observation) + b1[:,:,network]
                # compute the activation of the first layer of neurons with the tanh function
                A1 = np.tanh(Z1)
                # compute the netinput of the second layer of neurons
                Z2 = np.dot(W2[:,:,network], A1) + b2[:,:,network]
                # compute the activation of the second layer of neurons with the tanh function
                A2 = np.tanh(Z2)
                # if actions are discrete we select the action corresponding to the most activated unit
                if (isinstance(env.action_space, gym.spaces.box.Box)):
                    action = A2
                else:
                    action = np.argmax(A2)

                observation, reward, done, info = env.step(action)
                reward_sum[network] = reward_sum[network] + reward

        best = reward_sum.argsort()[-individuals:][::-1] # find the best models
        worst = reward_sum.argsort()[:individuals][::-1] # pick the worst models
        print('Reward', reward_sum)
        print('Best', best,'\n')

    # Post-Evaluation
    really_best = best[-1]

# Post-Evaluation
print('Post-Evaluation')
time.sleep(2)
for episode in range(episodes):
        print('episode # ', episode)
        reward_sum = 0
        observation = env.reset() #  initializes the position of the agent and of the environment
        for i in range(steps):
            env.render() #  displays graphically the agent and the environment

            # convert the observation array into a matrix with 1 column and ninputs rows

            observation.resize(ninputs,1)

            Z1 = np.dot(W1[:,:,really_best], observation) + b1[:,:,really_best]   
            A1 = np.tanh(Z1)    
            Z2 = np.dot(W2[:,:,really_best], A1) + b2[:,:,really_best]
            A2 = np.tanh(Z2)
            # if actions are discrete we select the action corresponding to the most activated unit
            if (isinstance(env.action_space, gym.spaces.box.Box)):
                action = A2
            else:
                action = np.argmax(A2)

            observation, reward, done, info = env.step(action)
            reward_sum = reward_sum + reward
        print('Reward  = ', reward_sum*100//steps, ' %') 
env.close()

