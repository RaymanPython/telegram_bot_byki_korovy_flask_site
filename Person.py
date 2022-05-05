from utils import get_name


class Person:

    def __init__(self, update, context):
        self.update = update
        self.index = None
        self.friend = None
        self.zapros = None
        self.friends = []
        self.records = {'поражения': 0, 'ничьи': 0, 'победы': 0}

    def free(self):
        return self.index == None

    def name(self):
        return self.update.message.chat.username

    def __str__(self):
        return str(self.__dict__)

    def do(self):
        if self.zapros != None:
            self.append_friend(self.friend)
            self.zapros()

    def clear_zapros(self):
        self.friend = None
        self.zapros = None

    def append_friend(self, update):
        self.friends.append(get_name(update, Person))

    def name_first_name(self):
        return f'{self.update.message.chat.first_name} {self.update.message.chat.last_name}'

    def save(self):
        return {'records': str(self.records), 'real_name': self.name_first_name()}