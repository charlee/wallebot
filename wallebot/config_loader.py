import re
import os
import config

ENV_CONFIG_PREFIX = 'WALLEBOT_'

class Config(object):
    pass


def load_config():
    cfg = Config()
    for k in config.__dict__:
        if re.match(r'[A-Z_]+', k):
            setattr(cfg, k, getattr(config, k))

    for k in os.environ:
        if k.startswith(ENV_CONFIG_PREFIX):
            setattr(cfg, k[len(ENV_CONFIG_PREFIX):], os.environ[k])
            
    return cfg
    
    
