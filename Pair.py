from utils import get_name
from Person import Person


class Pair:

    def __init__(self, person1: Person, person2: Person):
        self.person1 = person1
        self.person2 = person2
        self.persons = [self.person1, self.person2]
        self.key = f'{get_name(self.person1, Person)}@{get_name(self.person2, Person)}'
        self.quiz1 = None
        self.quiz2 = None
        self.queue_number = 0
        self.count_xod = 0

    # фуннкциф возрващающая противника
    def enemy(self, update):
        if self.person1.update.message.chat.username == update.message.chat.username:
            return self.person2
        if self.person2.update.message.chat.username == update.message.chat.username:
            return self.person1

    def quiz(self, update):
        if self.person1.update.message.chat.username == update.message.chat.username:
            return self.quiz2
        if self.person2.update.message.chat.username == update.message.chat.username:
            return self.quiz1

    def number(self, update):
        if self.person1.update.message.chat.username == update.message.chat.username:
            return 0
        if self.person2.update.message.chat.username == update.message.chat.username:
            return 1

    def number_queue(self, update):
        return self.number(update) == self.queue_number

    def message(self, s, update):
        self.enemy(update).update.message.reply_text(str(s))

    def __str__(self):
        return f'{self.person1.name()}:{self.person2.name()},{self.free_xod()}.{self.quiz1},{self.quiz2}'

    def xod(self, update, ans=None, text=None):
        if self.free_xod():
            self.count_xod += 1
            self.queue_number += 1
            self.queue_number %= 2
            self.message(f'Ваш противник сходил так: {text}: {str(ans)}.', update)

    def finish(self, draw=False):
        if draw:
            self.person1.update.message.reply_text('Поздравляем с Ничьёй!')
            self.person2.update.message.reply_text('Поздравляем с Ничьёй!')
            return {get_name(self.person1, Person): 1, get_name(self.person2, Person): 1}
        if self.count_xod % 2 == 1:
            self.person2.update.message.reply_text('Поздравляем с победой')
            self.person1.update.message.reply_text(
                f'Увы, Вы проиграли, но не расстраивайтесь, в следующий раз Вам повезёт).\n'
                f'Число Вашего противника: {self.quiz2}')
            return {get_name(self.person1, Person): 0, get_name(self.person2, Person): 2}
        else:
            self.person1.update.message.reply_text('Поздравляем с победой')
            self.person2.update.message.reply_text(
                f'Увы, Вы проиграли, но не расстраивайтесь, в следующий раз Вам повезёт).\n'
                f'Число Вашего противника: {self.quiz1}')
            return {get_name(self.person1, Person): 2, get_name(self.person2, Person): 0}

    def free_xod(self):
        return not (None in (self.quiz1, self.quiz2))

    def put_quiz(self, update, quiz):
        if get_name(self.person1, Person) == get_name(update, Person) and self.quiz1 == None:
            self.quiz1 = quiz
        if get_name(self.person2, Person) == get_name(update, Person) and self.quiz2 == None:
            self.quiz2 = quiz
        if self.free_xod():
            self.person1.update.message.reply_text('Игра началась. Ваш ход.')
            self.person2.update.message.reply_text('Игра началась. Ждём когда первый игрок сходит.')
