from utils import get_name
from Game_board import Game_board
from Game import Game_info
from Person import Person
from telegram import ReplyKeyboardMarkup

markup_start = ReplyKeyboardMarkup([['/go']], one_time_keyboard=True)
markup_go_friend = ReplyKeyboardMarkup([['/yes', '/no']], one_time_keyboard=True)


class Game_Basic:
    def __init__(self):
        self.INFO = Game_info()

    def start(self, update, context):
        print(get_name(update, Person))
        self.INFO.append_person(update, context)
        update.message.reply_text(f'''
    Привет!
    Это бот-игра "Быки и коровы".

    Правила игры Вы можете найти по ссылке: https://urok.1sept.ru/articles/662278.
    Мы будем играть с четырехзначными числами.
    Чтобы начать, введите команду /go. 
    Когда Ваш противник будет найден, введите загадываемое число.

    После этого Вы и Ваш противник будете по очереди пытаться отгадать число; отгадавший его первым выигрывает.
    Если хотите сыграть с другом наберите /f никнейм вашего друга в телеграмме.
    Если хотите выйти,

     Удачной игры!
        ''',
                                  reply_markup=markup_start
                                  )

    def go(self, update, context):
        self.INFO.append_person(update, context)
        if self.INFO.person_free(update):
            update.message.reply_text('Ищем соперника',
                                      reply_markup=markup_start
                                      )
            if self.INFO.if_friend(update):
                update.message.reply_text('Ваши запросы отменены')
                self.INFO.clear_zapros(update)
            if self.INFO.free:
                self.INFO.put(update, context)
            else:
                self.INFO.find_game(update, context)
        else:
            if self.INFO.person_get(update).index == False:
                update.message.reply_text(f'Вы уже ищите себе противника')
            else:
                update.message.reply_text(f'Вы уже играете с {get_name(self.INFO.get_pair(update).enemy(update), Person)}')

    def go_friend(self, update, name):
        self.INFO.zapros(update, name)

    def text_handler(self, update, context):
        if not self.INFO.person_free(update):
            if self.INFO.pair_free_xod(update):
                if self.INFO.pair_queue_number(update):
                    if Game_board.prov(update.message.text, self.INFO.N):
                        update.message.reply_text('Ход сделан')
                        ans = Game_board.count(update.message.text, self.INFO.pair_quiz(update))
                        if ans.b_count == self.INFO.N:
                            update.message.reply_text('Вы выиграли')
                            self.INFO.pair_finish(update)
                        else:
                            update.message.reply_text(str(ans))
                            self.INFO.pair_xod(update, str(ans), update.message.text)
                    else:
                        update.message.reply_text('Некоректный запрос')

                else:
                    update.message.reply_text('Не Ваша очерердь')
            else:
                if Game_board.prov(update.message.text, self.INFO.N):
                    self.INFO.pair_put_quiz(update, update.message.text)
                    update.message.reply_text(f'Вы загадали число {update.message.text}')
                else:
                    update.message.reply_text('Некоректное загадываемое число')
        else:
            s = update.message.text.split()
            if s[0] == '/f':
                self.go_friend(update, s[1])
            else:
                self.INFO.get_pair(update).message(update.message.text)

    def yes(self, update, context):
        if self.INFO.if_friend(update):
            self.INFO.find_game_add(self.INFO.get_friend(update), self.INFO.person_get(update))
            self.INFO.get_friend(update).update.message.reply_text('Вас запрос был принят!')
            self.INFO.clear_zapros(update)
        else:
            update.message.reply_text('Вам никто не  не кидал приглашение на игру!')

    def no(self, update, context):
        if self.INFO.if_friend(update):
            self.INFO.clear_zapros(update)
            self.INFO.get_friend(update).update.message.reply_text('Вас запрос был отклонён!')
        else:
            update.message.reply_text('Вам никто не  не кидал приглашение на игру!')

    def end(self, update, context):
        self.INFO.end_draw(update)

    def record(self, update, context):
        rec = self.INFO.person_get(update).records
        update.message.reply_text(str(rec)[1:-1])

    def friends(self, update, context):
        fr = self.INFO.person_get(update).friends
        for i in range(len(fr)):
            fr[i] = '/f ' + fr[i]
        update.message.reply_text('Ваши друзья', reply_markup=ReplyKeyboardMarkup([fr], one_time_keyboard=True))
