from walleapi import app, rds
from flask import Blueprint, request, jsonify
import random
from wallebot.bot import WallEBot
from wallebot.handlers.api import API_TOKEN_KEY, API_TOKEN_REV_KEY
from wallebot.handlers.tags import TAGS_KEY

api_bp = Blueprint('api_bp', __name__)


def validate_api_token():
    
    api_token = request.headers.get('WallEAPIToken')
    user_id = rds.hget(API_TOKEN_REV_KEY, api_token)

    return user_id


def get_chat_id():
    chat_id = request.headers.get('WallEAPIChatId')
    try:
        return int(chat_id)
    except:
        return None
    

@api_bp.route('/random-tag/', methods=['POST'])
def random_tag():
    
    user_id = validate_api_token()
    chat_id = get_chat_id()

    if user_id is None or chat_id is None:
        return jsonify({'result': 'error', 'message': 'Please set WallEAPIToken and WallEAPIChatId headers'})

    key = TAGS_KEY % chat_id
    tags = list(rds.smembers(key))
    if len(tags) > 0:
      tag = random.choice(tags)

      bot = WallEBot(app.config['TELEGRAM_TOKEN'])
      bot.bot.sendMessage(chat_id=chat_id, text='#%s' % tag)


      return jsonify({'result': 'success'})

    else:
      return jsonify({'result': 'error', 'message': 'No tags yet'})
