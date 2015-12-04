from walleapi import app, rds
from flask import Blueprint, request, jsonify
import random
from wallebot.bot import WallEBot
from wallebot.handlers.api import API_TOKEN_KEY, API_TOKEN_REV_KEY
from wallebot.handlers.tags import TAGS_KEY

api_bp = Blueprint('api_bp', __name__)


def validate_api_token():
    
    api_token = request.headers.get('WallEAPIToken')
    user_info = rds.hget(API_TOKEN_REV_KEY, api_token)
    if user_info is not None and ',' in user_info:
        return user_info.split(',')
    else:
        return None, None


def get_chat_id():
    chat_id = request.headers.get('WallEAPIChatId')
    try:
        return int(chat_id)
    except:
        return None
    

@api_bp.route('/random-tag/', methods=['POST'])
def random_tag():
    
    user_id, username = validate_api_token()
    chat_id = get_chat_id()

    if user_id is None or chat_id is None:
        return jsonify({'result': 'error', 'message': 'Please set WallEAPIToken and WallEAPIChatId headers'})

    keywords = request.form.get('k')
    if keywords is not None:
        keywords = filter(None, keywords.split(' '))
        keywords = map(lambda x:x.encode('utf-8'), keywords)

    key = TAGS_KEY % chat_id
    tags = list(rds.smembers(key))
    if keywords:
        tags = filter(lambda x:all(k in x for k in keywords), tags)
    
    if len(tags) > 0:
      tag = random.choice(tags)

      bot = WallEBot(app.config['TELEGRAM_TOKEN'])
      bot.bot.sendMessage(chat_id=chat_id, text='#%s via @%s' % (tag, username))


      return jsonify({'result': 'success'})

    else:
      return jsonify({'result': 'error', 'message': 'No tags yet'})
