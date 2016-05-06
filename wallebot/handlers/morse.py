# coding: utf-8

import re
from .base import MessageHandler

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

class MorseCodeHandler(MessageHandler):

    def test(self, msg):
        text = msg['text'].encode('utf-8').replace('—', '--')
        return re.match(r'^[-_./ ]+$', text)

    def handle(self, msg):

        text = msg['text'].encode('utf-8')
        text = text.replace('—', '--').replace('_', '-')

        chat_id = msg['chat']['id']

        results = []
        words = filter(None, text.split('/'))
        for word in words:
            letters = filter(None, word.split(' '))
            results.append(''.join(self.translate(letter) for letter in letters))

        result = ' '.join(results)

        if len(result) >= 3:

            print 'Translate morse: %s // %s' % (text, result)

            self.bot.sendMessage(chat_id=chat_id, text=result)


    def translate(self, morse):
        return MORSE_CODE.get(morse, '*')
        

        
