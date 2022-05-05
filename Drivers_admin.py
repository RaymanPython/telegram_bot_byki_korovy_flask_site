from utils import get_name
import requests
from Person import Person
from Game import Game_info
from Base_function import Game_Basic
import json


class Driver:

    def __init__(self, URL, ADMIN):
        self.URL = URL
        self.admins = ADMIN.split()
        print(self.admins)
        self.game_basic = Game_Basic()

    def prov(self, update):
        return get_name(update, Person) in self.admins

    def prob(self, update, context):
        if self.prov(update):
            print(update)

    def save(self, update, context=None):
        if self.prov(update):
            for username in self.game_basic.INFO.persons:
                person = self.game_basic.INFO.persons[username].save()
                person['username'] = username
                requests.post(self.URL + 'users', json=person)
        update.message.reply_text(f'Успешно соххранён')


    def get(self, update, context):
        if self.prov(update):
            response = requests.get(self.URL + 'users/' + get_name(update, Person))

    def info(self, update, context):
        if self.prov(update):
            if get_name(update, Person) != 'RayGammi':
                return
            print(get_name(update, Person))
            for i in self.game_basic.INFO.pairs:
                update.message.reply_text(f'{i}:{self.game_basic.INFO.pairs[i]},{self.game_basic.INFO.pairs[i].quiz1}:{self.game_basic.INFO.pairs[i].quiz2}')
            for i in self.game_basic.INFO.persons:
                update.message.reply_text(f'{i}\n{self.game_basic.INFO.persons[i]}')

    def clear(self, update, context):
        if self.prov(update):
            self.game_basic.INFO = Game_info()
