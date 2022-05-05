from Person import Person
from utils import get_name, check_name
from Pair import Pair
from telegram import ReplyKeyboardMarkup


class Game_info:

    def init_param(self, **params):
        pass

    def __init__(self):
        self.free = True
        self.free_name = None
        self.key = 0
        self.persons = dict()
        self.pairs = dict()
        self.N = 4
        self.win_ball = 10
        self.draw_ball = 5
        self.keys_records = ['поражения', 'ничьи', 'победы']

    def put(self, update, context):
        self.free = False
        self.free_name = self.person_get(update)
        self.person_get(update).index = False

    def find_game(self, update, context):
        person = self.free_name
        person_new = self.person_get(update)
        self.free = True
        self.free_name = None
        self.find_game_add(person, person_new)

    def find_game_add(self, person1, person2):
        self.find_game_message(person1)
        self.find_game_message(person2)
        self.append_pair(person1, person2)

    def find_game_message(self, person):
        person.update.message.reply_text('Игра найдена.\nЗагадайте, пожалуйста Ваше число.')

    def person_put_game(self, person1, person2):
        self.persons[get_name(person1, Person)].index = person2

    def append_pair(self, person1, person2):
        pair = Pair(person1, person2)
        self.pairs[pair.key] = pair
        self.person_put_game(person1, pair.key)
        self.person_put_game(person2, pair.key)

    def append_person(self, update, context):
        if get_name(update, Person) not in self.persons:
            self.persons[get_name(update, Person)] = Person(update, context)
        return Person(update, context)

    def person_free(self, update):
        return self.person_get(update).free()

    def person_get(self, update, contex=None):
        return self.persons.get(get_name(update, Person), self.append_person(update, contex))

    def person_get_game(self, update):
        return self.person_get(update)

    def person_put_free(self, update):
        self.persons[get_name(update, Person)].index = None

    def person_key(self, update):
        return self.persons[get_name(update, Person)].index

    def get_pair(self, update):
        return self.pairs[self.person_key(update)]

    def pair_quiz(self, update):
        return self.get_pair(update).quiz(update)

    def pair_queue_number(self, update):
        return self.get_pair(update).number_queue(update)

    def pair_xod(self, update, ans, text):
        self.pairs[self.person_key(update)].xod(update, ans, text)

    def free_pair(self, pair):
        self.person_put_free(pair.person1)
        self.person_put_free(pair.person2)

    def pair_finish(self, update, draw=False):
        rec = self.get_pair(update).finish(draw)
        pair = self.get_pair(update)
        key = self.person_key(update)
        self.free_pair(pair)
        del self.pairs[key]
        self.save_record(rec)

    def save_record(self, rec):
        for i in rec:
            self.person_get(i).records[self.keys_records[rec[i]]] += 1

    def pair_free_xod(self, update):
        return self.get_pair(update).free_xod()

    def pair_put_quiz(self, update, text):
        self.pairs[self.person_key(update)].put_quiz(update, text)

    def get_zapros(self, update, name):
        markup_go_friend = ReplyKeyboardMarkup([['/yes', '/no']], one_time_keyboard=True)
        self.persons[check_name(name)].update.message.reply_text(f'Вас пригласил игрок {get_name(update, Person)}, '
                                                                 f'если хотите с ним играть то нажмите на одну из кнопок /yes или /n.',
                                                                 reply_markup=markup_go_friend)
        self.persons[check_name(name)].friend = get_name(update, Person)

    def zapros(self, update, name):
        name = check_name(name)
        self.person_get(update).friend = name
        function = lambda: self.get_zapros(update, name)
        self.persons[name].zapros = function
        self.persons[name].friend = self.person_get(update)
        if self.persons[name].free():
            self.persons[name].do()

    def clear_zapros(self, update):
        self.persons[get_name(self.get_friend(update))].clear_zapros()
        self.persons[get_name(update, Person)].clear_zapros()

    def if_friend(self, update):
        return self.person_get(update).friend != None

    def get_friend(self, update):
        if self.if_friend(update):
            return self.person_get(self.person_get(update).friend)

    def end_draw(self, update):
        self.pair_finish(update, True)
