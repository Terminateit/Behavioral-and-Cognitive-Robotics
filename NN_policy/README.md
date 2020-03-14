# Run the project
```bash
python3 main.py
```


# Evorobotpy

######   it's a software library implemented by the author compliant with AI-Gym that permits to evolve robots.

I was familiarized with the usage of this program by evolving a policy for the acrobot problem. To
do that I entered into the /xacrobot folder and run the command:
```bash
python3 ../bin/es.py -f acrobot.ini -s <seed>
```
I ran it three times with different seeds. Then, I inspected the behavior of and evolved agents with the next commands:
```bash
python3 ../bin/es.py -f acrobot.ini -t bestgS<seed>.npy
```
The example of result you can see here:

![The behavior](https://raw.githubusercontent.com/Terminateit/Behavioral-and-Cognitive-Robotics/master/NN_policy/Files/BestS15.png)

After that, I  displayed the variation of performance across generations and the average and standard deviation of
performance among multiple runs, using the following command, respectively:
```bash
python3 ../bin/plotstat.py

python3 ../bin/plotave.py
```
The example of result you can see here:

![Plot of performance](https://raw.githubusercontent.com/Terminateit/Behavioral-and-Cognitive-Robotics/master/NN_policy/Files/statS.png)

Average Generalization: -66.56 +-1.13 (3 S*.fit files)

###### Note: The action is either applying +1, 0 or -1 torque on the joint between the two pendulum links. The state consists of the sin() and cos() of the two rotational joint angles and the joint angular velocities : [cos(theta1) sin(theta1) cos(theta2) sin(theta2) thetaDot1 thetaDot2].

# FAQ:

1.How is the code organized?
-
##### I did both tasks 2a and 2b in one .py script. You can just change parameters "technique" and "environment" in the code to run various cases.

2.The case: Neural Network with random updates of parameters. What happens?
-
  ##### When this case is run, you can see every time that the system doesn't become stable because of NN learning absence. So, such technique doesn't fit our requirements.

3.The case: Evolutionary Strategy.
-
1.  Does the robot manage to solve the problem? 
  
    ##### Yes, the robot manages to solve the problem. But the efficiency depends. It doesn't give the same results every time I run the code. I think it's because of the learning nature and parameters' randomization. Increasing the number of steps or epochs could make the model much and much better.

2. Does it solve the problem every time you run the training process?
  
    ##### I ran the code several times and every time it solved the problem with various accuracy. But it works...

3. What happens by changing the
parameters (e.g. size of the population, number of hidden units, the variance of the perturbation
vector, the number of evaluation episodes)?


    ######  "success" - (sum of reward)/(number of steps)
    ##### If we increase the size of the population, then the post-evaluation of the model shows the better "success" (55 % having size = 10 ). And if we decrease the size of the population, then the model is much worse (5 % having size = 1)

    ##### As the experiments showed, the increasing of number of hidden units may either increase the "success" or decrease it... But usually it increases the "success" of the post-evaluation model. 5 is quite enough, because increasing this could be unpredictable.

    ##### According to the observation of the post-evaluation model's behavior, I can say that decreasing of the variance of the perturbation vector may increase the "success".

    ##### Number of episodes as the rule increases the "success".


4.  Case: simple control problem such
as the Pendulum-v0. What happens?

      ##### Works not so cool... The nature of the reward is a bit strange. 

      #### Update:
      ##### I went to the documentation of the pendulum and noticed that the reward of the pendulum models is actually the angle of rotation 
