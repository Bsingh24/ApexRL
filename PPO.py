import torch
from torch import nn
from torch.distributions.normal import Normal
import numpy as np

def init_layers(layer, w=np.sqrt(2), b=0):
  nn.init.orthogonal_(layer.weight, w)
  nn.init.constant_(layer.bias, b)
  return layer

class PPO(nn.Module):
  def __init__(self, obs_space, action_space):
    super().__init__()
    self.critic = nn.Sequential(
        init_layers(nn.Linear(obs_space, 64)),
        nn.Tanh(),
        init_layers(nn.Linear(64, 64)),
        nn.Tanh(),
        init_layers(nn.Linear(64, 1), w=1),
    )

    self.actor = nn.Sequential(
      init_layers(nn.Linear(obs_space, 64)),
      nn.Tanh(),
      init_layers(nn.Linear(64, 64)),
      nn.Tanh(),
      init_layers(nn.Linear(64, action_space), w=0.01) # Allows means of actions to be near 0
    )
    self.actor_logstd = nn.Parameter(torch.zeros(action_space))

  def get_value(self, x):
    value = self.critic(x)
    return value

  def get_action_and_value(self, x, action=None):
    action_mean = self.actor(x)
    action_logstd = self.actor_logstd.expand_as(action_mean) # match batch size
    action_std = torch.exp(action_logstd)
    probs = Normal(action_mean, action_std)
    if action is None:
      action = probs.sample()
    return action, probs.log_prob(action).sum(1), probs.entropy().sum(1), self.critic(x)
