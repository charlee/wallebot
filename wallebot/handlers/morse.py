# coding: utf-8

import re
from .base import Handler

import logging

log = logging.getLogger(__name__)

MORSE_CODE = {
    
    '.-'  : 'A',
    '-...': 'B',
    '-.-.': 'C',
    '-..' : 'D',
    '.'   : 'E',
    '..-.': 'F',
    '--.' : 'G',
    '....': 'H',
    '..'  : 'I',
    '.---': 'J',
    '-.-' : 'K',
    '.-..': 'L',
    '--'  : 'M',
    '-.'  : 'N',
    '---' : 'O',
    '.--.': 'P',
    '--.-': 'Q',
    '.-.' : 'R',
    '...' : 'S',
    '-'   : 'T',
    '..-' : 'U',
    '...-': 'V',
    '.--' : 'W',
    '-..-': 'X',
    '-.--': 'Y',
    '--..': 'Z',
    '-----': '0',
    '.----': '1',
    '..---': '2',
    '...--': '3',
    '....-': '4',
    '.....': '5',
    '-....': '6',
    '--...': '7',
    '---..': '8',
    '----.': '9',
    '--..--': ',',
    '.-.-.-': '.',
    '..--..': '?',
    '-.-.-.': ';',
    '---...': ':',
    '.----.': ',',
    '-....-': '-',
    '-..-.' : '/',
}

class MorseCodeHandler(Handler):

    def message(self, msg):

        text = msg['text']
        text = text.replace(u'—', u'--').replace(u'_', u'-')

        if not re.match(r'^[-_./ ]+$', text):
            return

        chat_id = msg['chat']['id']

        results = []
        words = filter(None, text.split('/'))
        for word in words:
            letters = filter(None, word.split(' '))
            results.append(''.join(self.translate(letter) for letter in letters))

        result = ' '.join(results)

        if len(result) >= 3:

            log.info('Translate morse: %s // %s' % (text, result))

            self.bot.sendMessage(chat_id=chat_id, text=result)


    def translate(self, morse):
        return MORSE_CODE.get(morse, '*')
        

        
