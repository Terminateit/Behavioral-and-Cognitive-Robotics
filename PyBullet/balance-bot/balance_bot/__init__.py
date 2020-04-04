# The file __init__.py should include a register instruction with the name of the environment (that can
# be passed to the function gym.make()) and the entry point of the environmental class in the format
# {base module name}.envs:{Env subclass name}:
from gym.envs.registration import register
register(
id='balancebot-v0',
entry_point='balance_bot.envs:BalancebotEnv',)
