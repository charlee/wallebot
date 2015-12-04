
import redis
from flask import Flask
from wallebot.config_loader import load_config

app = Flask(__name__)

cfg = load_config()
app.config.from_object(cfg)

rds = redis.StrictRedis(host=cfg.REDIS_HOST, db=cfg.REDIS_DB)


from api import api_bp

app.register_blueprint(api_bp, url_prefix='/api')
