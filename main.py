import telebot
import re
import random
import requests

import CONFIG
import lessons_parser

bot = telebot.TeleBot(f'{CONFIG.TG_BOT_TOKEN}')

answers = ['🧘 Матерщинник-рецедивист!!!\n 🧘 Помни грешник - кара Админа может настигнуть тебя!\nОбщайся культурно!',
           'Ваши матерные слова вызывают недоумение в глазах уважаемых граждан этого чата. Просим впредь ими не пользоваться.',
           'Давай без твоих урчаний',
           'Именем сообщества данного чата нарекаю тебя петушарой',
           'Куда деньги на лечение от бескультурья скидывать?',
           'Знаешь что? А ни что! Нормально общайся',
           'Ай-яй-яй. Плохо. Но еще есть время искупить вину перед всевышним.',
           'Это неуважение ко всем нам. Прекрати',
           'Вы только что совершили смертный грех. Я бы на вашем месте незамедлительно отправлялся в церковь. Замаливать.',
           'Вот и зачем, скажи мне на милость, Кирилл и Мефодий тебе письменность подарили?',
           'Если ты извинишься за эту пакость сейчас, мы сделаем вид, что ничего не видели. У тебя 10 секунд',
           'А теперь выйди и зайди как положено',
           'Соизвольте здесь только в культурной форме',
           'Не нужно выносить мусор сюда, пожалуйста. Для этого есть специально отведенные места.',
           'И этими губами ты маму целуешь?',
           'Я прошу прощения, но что вы себе позволяете? Вы бы еще штаны сняли и голой задницей перед нами посветили. Нет, нет, здесь так не принято! Немедленно извинитесь!',
           'Неправильно ты, дядя Федор, в сообщениях выражаешься',
           'Коллективный стыд-позор тебе!',
           'Великий Кристофер Шоулз почти три века назад придумал раскладку для твоей клавиатуры не для того, чтоб ты непотребства отправлял. Не делай так больше',
           'Не делай этого, прошу, не разбивай мне сердце! Пиши культурно!']

with open('russian_ban_words.txt', encoding='UTF-8') as ban_words:
    russian_ban_words = set(i.strip() for i in ban_words)

# поможет заменить похожие английские буквы на русские
eng_remover = {'t': 'т', 'a': 'а', 'x': 'х', 'o': 'о', 'e': 'е', 'p': 'р', 'm': 'м', 'c': 'с', 'y': 'у', 'k': 'к'}
days_offset = {'сегодня': 0, 'завтра': 1}


def remove_duplicate_chars(string):
    new_string = ""
    for char in string:
        if new_string.find(char) == -1:
            new_string += char
    return new_string


class MakePeriods:
    def __init__(self, tg_message):
        self.message = tg_message

    def update_homework_message(self):
        pass


@bot.message_handler(commands=['дз'])
def beautiful_list_creator(message):
    # Очистить от пустых строк
    new_message = [i for i in message.text.split('\n') if i != '']
    # Забыть "\команду", разделить сообщение по точкам
    new_message = new_message[1].split('.')
    # Создать заголовок
    lesson = f'🌘{new_message[0]}🌒'

    # Пройтись по "пунктам" из дз (пункт = точка)
    for i in new_message[1::]:
        lesson += f'\n🔻{i}'

    bot.send_message(message.chat.id, text=f'{lesson}')


@bot.message_handler(commands=['сегодня', 'завтра', 'послезавтра'])
def command_checker(message):
    DAYS_OFFSET = {'сегодня': 0, 'завтра': 1, 'послезавтра': 2, 'через-два-дня': 3}

    if message.from_user.username in ['EXTRAOS', ]:
        response_schedule = lessons_parser.get_schedules_from_dnevnik_html(offset=DAYS_OFFSET[message.text[1::]])
        bot.send_message(chat_id=message.chat.id,
                         text=f'{lessons_parser.add_date_to_text(response_schedule, to_end=True, to_start=True, offset=DAYS_OFFSET[message.text[1::]])}')


# @bot.message_handler()
# def message_checker(message):
#     stripped_message_text = message.text.lower()
#     stripped_message_text = re.sub('"', '', stripped_message_text)
#     stripped_message_text = re.sub(rf"[.':,!@#№;%?*$^&()_]", '', stripped_message_text)
#     stripped_message_text = re.sub(r"\d+", "", stripped_message_text)
#     stripped_message_text = remove_duplicate_chars(stripped_message_text)
#
#     for letter in stripped_message_text:
#         if letter in eng_remover.keys():
#             stripped_message_text = stripped_message_text.replace(letter, eng_remover[letter])
#
#     for message_word in stripped_message_text.split():
#         for i in russian_ban_words:
#             if i in message_word:
#                 bot.delete_message(message.chat.id, message.id)
#                 bot.send_message(message.chat.id,
#                                  text=f'@{message.from_user.username}, {random.choice(answers)}')
#                 break


bot.polling(none_stop=True)
