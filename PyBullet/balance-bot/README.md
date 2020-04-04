You can install the environment with the following instructions:

```bash
cd balance-bot
pip install -e .
```

Finally, you can use balance_bot as a standard gym environment after importing it with the following
instructions:

```bash
import balance_bot
```

For example, you can train the robot with the ```evorobotpy/bin/es.py``` script after adding the import
statement in the script.

If you have some mode problems with ```policy.py``` file, go to it and change line
```bash
self.env.render()
``` 
to 
```bash
self.env.render(mode = 'human')
``` 

Note!
If you evolve model, change line in ```balancebot_env.py``` file
```bash
self.physicsClient = p.connect(p.DIRECT)  # Non-Graphical version (for evolving)
``` 
If you want to seee evolved model, change line in ```balancebot_env.py``` file
```bash
self.physicsClient = p.connect(p.GUI)  # Graphical version
```