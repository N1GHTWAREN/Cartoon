import telebot
import sqlite3
import json
import random
import datetime
from telebot import types


bot = telebot.TeleBot('6887806463:AAGFV6FPhnLj6Iy1-jAHfjcb3BmP10YXZh0')
bot.delete_webhook()
all_cards = {
    '1': ('Aston Martin Valkyrie 2018', '2016 - 2019', '🇬🇧', '6.5 л / 1176 л.с. / бензин', 'legendary'),
    '2': ('Mitsubishi Delica 1993', '1968 - настоящее время', '🇯🇵', '2.5 л / 85 л.с. / дизель', 'common'),
    '3': ('Fiat Nuova 500 1966', '1957 - 1975', '🇮🇹', '0.5 л / 17 л.с. / бензин', 'common'),
    '4': ('Peugeot 208 2014', '2012 - настоящее время', '🇫🇷', '1.6 л / 92 л.с. / дизель', 'common'),
    '5': ('Renault Captur 2016', '2013 - настоящее время', '🇫🇷', '1.6 л / 114 л.с. / бензин', 'common'),
    '6': ('Opel Astra 2014', '1991 - настоящее время', '🇩🇪', '1.6 л / 115 л.с. / бензин', 'common'),
    '7': ('Infinity Q30 2019', '2015 - 2019', '🇬🇧', '2.0 л / 211л.с. / бензин', 'rare'),
    '8': ('Bugatti Veyron 2007', '2005 - 2015', '🇫🇷', '8.0 л / 1001 л.с. / бензин', 'legendary'),
    '9': ('Volvo XC60 2019', '2008 - настоящее время', '🇸🇪', '2.0 / 235 л.с./ дизель', 'rare'),
    '10': ('Alfa Romeo Giulia II 2019', '2015 - настоящее время', '🇮🇹', ' 2.0 л / 280 л.с. / бензин', 'rare'),
    '11': ('Land Rover Defender 110 1990', '1983 - настоящее время', '🇬🇧', '2.5 л / 113 л.с. / дизель', 'common'),
    '12': ('Škoda Karoq 2017', '2017 - настоящее время', '🇨🇿', '1.4 / 150 л.с. / бензин', 'common'),
    '13': ('Tesla Model S 2015', '2012 - настоящее время', '🇺🇸', '515 кВт / электро', 'epic'),
    '14': ('Ferrari F40 1992', '1987 - 1992', '🇮🇹', '2.9 л / 478 л.с. / бензин', 'legendary'),
    '15': ('Lamborghini Huracán 2022', '2014 - настоящее время', '🇮🇹', '5.2 л / 640 л.с. / бензин', 'legendary'),
    '16': ('Range Rover Sport 2015', '2005 - настоящее время', '🇬🇧', '4.4 л / 339 л.с./ дизель', 'epic'),
    '17': ('Nissan X-Trail T32 2013', '2000 - настоящее время', '🇯🇵', '2.0 л / 144 л.с. / бензин', 'common'),
    '18': ('Porsche 911 carrera 4S 2013', '1963 - настоящее время', '🇩🇪', '3.8л / 400 л.с. / бензин', 'epic'),
    '19': ('Maserati GrandTurismo 2013', '2007 - настоящее время', '🇮🇹', '4.7 л / 460 л.с./ бензин', 'epic'),
    '20': ('Mazda 3 2018', '2003 - настоящее время', '🇯🇵', '1.5 л / 120 л.с./ бензин', 'common'),
    '21': ('Hyundai Solaris I рестайлинг 2014', '2011 - настоящее время', '🇰🇷', '1.6л / 123 л.с. / бензин', 'common'),
    '22': ('Lexus GS 300 2018', '1991 - 2020', '🇯🇵', '2.0л / 245 л.с. / бензин', 'rare'),
    '23': ('Audi R8 V10 2011', '2007 - 2012', '🇩🇪', '5.2 / 525 л.с. / бензин', 'epic'),
    '24': ('McLaren P1 2015', '2012 - 2017', '🇬🇧', '3.8л / 650 л.с. / бензин', 'legendary'),
    '25': ('Bentley Mulsanne II 2010', '2010 - 2020', '🇬🇧', '6.8 / 512 л.с. / бензин', 'epic'),
    '26': ('BMW 3-й серии 325i 1986', '1982 - 1994', '🇩🇪', '2.5 / 170 л.с. / бензин', 'common'),
    '27': ('Mercedes-Benz S-Класс AMG 63 Long 2018', '1999 - настоящее время', '🇩🇪', '4.0 л / 612 л.с. / бензин', 'epic'),
    '28': ('Toyota Camry 2019', '1980 - настоящее время', '🇯🇵', '3.5 л / 249 л.с. / бензин', 'common'),
    '29': ('Toyota Supra A90 2020', '1986 - настоящее время', '🇯🇵', '3.0 л / 340 л.с. / бензин', 'epic'),
    '30': ('Hummer H3 2008', '2005 - 2010', '🇺🇸', '5.3 л / 300 л.с. / бензин', 'rare'),
    '31': ('Chevrolet Camaro VI 2016', '2005 - 2018', '🇺🇸', '2.0 л / 275 л.с. / бензин', 'rare'),
    '32': ('Mercedes-Benz AMG GT 2017', '2014 - 2017', '🇩🇪', '4.0 л / 462 л.с. / бензин', 'epic'),
    '33': ('Chevrolet Corvette 1993', '1984 - 1998', '🇺🇸', '5.7 л / 300 л.с. / бензин', 'rare'),
    '34': ('Chevrolet Corvette Zr1 2018', '2013 - 2019', '🇺🇸', '6.2 л / 466 л.с. / бензин', 'epic'),
    '35': ('Ford Mustang 2005', '2004 - 2009', '🇺🇸', '4.6 л / 315 л.с. / бензин', 'common'),
    '36': ('Ford Mustang 2017', '2014 - 2017', '🇺🇸', '2.3 л / 317 л.с. / бензин', 'rare'),
    '37': ('Jeep Wrangler III 2011', '2007 - 2018', '🇺🇸', '2.8 л / 200 л.с. / дизель', 'common'),
    '38': ('BMW M2 F87 2017', '2015 - 2021', '🇩🇪', '3.0 л / 370 л.с. / бензин', 'epic'),
    '39': ('Mercedes-Benz E-Класс 2018', '1992 - настоящее время', '🇩🇪', '2.0 / 184 л.с. / бензин', 'epic')

}
for_random = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
              '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36',
              '37', '38', '39']
rarities = (1, 3.928, 3.928, 3.928, 3.928, 3.928, 3.75, 1, 3.75, 3.75, 3.928, 3.928, 0.833, 1, 1, 0.833, 3.928, 0.833, 0.833, 3.928, 3.928, 3.75, 0.833, 1, 0.833, 3.928, 0.833, 3.928, 0.833, 3.75, 3.75, 0.833, 3.75, 0.833, 3.928, 3.75, 3.928, 0.833, 0.833)


def rarity_test(card):
    if card[4] == 'legendary':
        return 'Легендарная', 3000
    elif card[4] == 'epic':
        return 'Эпическая', 1500
    elif card[4] == 'rare':
        return 'Редкая', 500
    elif card[4] == 'common':
        return 'Обычная', 250


def time_conversion(sec):
    sec %= (24 * 3600)
    hour_value = str(sec // 3600)
    sec %= 3600
    minunte_value = str(sec // 60)
    if hour_value == '0':
        hour_value = ''
    elif hour_value == '1':
        hour_value = f'{hour_value} час '
    else:
        hour_value = f'{hour_value} часа '
    if minunte_value == '0':
        minunte_value = ''
    elif minunte_value[-1] == '1':
        minunte_value = f'{minunte_value} минута'
    elif minunte_value[-1] in ('2', '3', '4'):
        minunte_value = f'{minunte_value} минуты'
    else:
        minunte_value = f'{minunte_value} минут'
    if minunte_value == '' and hour_value == '': return 'Меньше минуты'
    return hour_value + minunte_value


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('garage_data_base.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int primary key, number_of_cards int, cards VARCHAR, rating int, last_time VARCHAR)')
    conn.commit()
    if cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE id = '%i')" % message.from_user.id).fetchone()[0] == 0:
        now = datetime.datetime.now()
        cur.execute("INSERT INTO users (id, number_of_cards, cards, rating, last_time) VALUES ('%i', '%i', '%s', '%i', '%s')" % (message.from_user.id, 0, '{}', 0, json.dumps((now.year, now.month, now.day, now.hour - 4, now.minute, now.second))))
        conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    new_card = types.KeyboardButton('Получить новую карту 🚗')
    menu = types.KeyboardButton('Главное меню 🏠')
    markup.add(new_card, menu)
    bot.send_message(message.chat.id, f'👋 Привет, <b><em>{message.from_user.first_name}</em></b>, рад тебя видеть в гараже!\n\n🎮 Здесь ты можешь собрать коллекцию из своих любимых машин, устраивать дуэли с друзьями, торговать своими карточками и играть в мини игры.\n\n🃏 Всего 4 вида карт: обычные, редкие, эпические и легендарные. За получение карточки ты поднимаешь свой <b><em>рейтинг</em></b>, чем реже карта, тем больше ты получишь за нее рейтинга.\n\n💰 Ты можешь продавать дупликаты или не нужные тебе карты в твоей коллекции, за продажу карт, а также за еженедельные задания ты можешь получать <b><em>очки влияния</em></b>, за которые, в свою очередь, можешь купить улучшения твоего персонажа или гаража.\n\nНу что, ты готов получить свою первую машину? Нажимай кнопку <b><em>"Получить новую карту"</em></b>, приятной игры! 🍀\n\n👥 Авторы:\n@N1GHTWARE\n@nsrkaaa\n@kailzz', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, f'Полная информация для разработчика:\n{message}')
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    conn = sqlite3.connect('garage_data_base.sql')
    cur = conn.cursor()
    if message.text == '/start':
        return start(message)
    elif message.text == '/info':
        return info(message)
    elif message.text == 'Получить новую карту 🚗':
        cur.execute("SELECT * FROM users")
        user = cur.fetchall()
        cards = {}
        last_time = None
        for i in user:
            if i[0] == message.chat.id:
                cards = json.loads(i[2])
                last_time = datetime.datetime(*json.loads(i[4]))
                break
        # 14400
        if (datetime.datetime.now() - last_time).seconds >= 1:
            card_num = random.choices(for_random, weights=rarities)[0]
            card = all_cards[str(card_num)]
            rarity_of_card = rarity_test(card)
            bot.send_photo(message.chat.id, open(f'{card_num}.jpg', 'rb'), f'Ты получил новую карту: {card[0]}\nГоды выпуска: {card[1]}\nСтрана: {card[2]}\nДвигатель: {card[3]}\nРедкость: {rarity_of_card[0]}\nРейтинг + {str(rarity_of_card[1])}')
            cur.execute("UPDATE users SET number_of_cards = number_of_cards + 1 WHERE id = '%i'" % message.chat.id)
            conn.commit()
            cur.execute("UPDATE users SET rating = rating + '%i' WHERE id = '%i'" % (rarity_of_card[1], message.chat.id))
            conn.commit()
            if str(card_num) in list(map(lambda x: x[0], cards.items())):
                cards[str(card_num)] += 1
            else:
                cards[str(card_num)] = 1
            cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards), message.chat.id))
            conn.commit()
            now = datetime.datetime.now()
            cur.execute("UPDATE users SET last_time = '%s' WHERE id = '%i'" % (json.dumps([now.year, now.month, now.day, now.hour, now.minute, now.second]), message.chat.id))
            conn.commit()
        else:
            # 14400
            bot.send_message(message.chat.id, f'До следующей попытки {time_conversion(1 - (datetime.datetime.now() - last_time).seconds)}')
    elif message.text == 'Главное меню 🏠':
        markup = types.InlineKeyboardMarkup()
        prof = types.InlineKeyboardButton('Твой профиль', callback_data='profile')
        deck = types.InlineKeyboardButton('Твоя коллекция', callback_data='deck')
        markup.row(prof, deck)
        bot.send_photo(message.chat.id, open('./garage_main.png', 'rb'), 'Доступные действия:', reply_markup=markup)
    cur.close()
    conn.close()
    bot.register_next_step_handler(message, on_click)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    conn = sqlite3.connect('garage_data_base.sql')
    cur = conn.cursor()
    if callback.data == 'profile':
        cur.execute("SELECT * FROM users")
        user = cur.fetchall()
        rating = 0
        for i in user:
            if i[0] == callback.message.chat.id:
                rating = i[3]
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, f'Имя:\n{callback.message.chat.first_name}\nРейтинг: {rating}\nПобед в дуэлях: _')
    elif callback.data == 'deck':
        markup = types.InlineKeyboardMarkup()
        show_all = types.InlineKeyboardButton('Показать все карты', callback_data='show_all')
        show_legendary = types.InlineKeyboardButton('Показать все легендарные карты', callback_data='show_legendary')
        show_epic = types.InlineKeyboardButton('Показать все эпические карты', callback_data='show_epic')
        show_rare = types.InlineKeyboardButton('Показать все редкие карты', callback_data='show_rare')
        show_common = types.InlineKeyboardButton('Показать все обычные карты', callback_data='show_common')
        markup.row(show_all)
        markup.row(show_common)
        markup.row(show_rare)
        markup.row(show_epic)
        markup.row(show_legendary)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        cur.execute("SELECT * FROM users")
        user = cur.fetchall()
        num = 0
        for i in user:
            if i[0] == callback.message.chat.id:
                num = i[1]
                break
        if num == 0:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
        elif str(num)[-1] != '1':
            bot.send_message(callback.message.chat.id, f'Твоя коллеция состоит из {num} карт', reply_markup=markup)
        else:
            bot.send_message(callback.message.chat.id, f'Твоя коллеция состоит из {num} карты', reply_markup=markup)
    elif callback.data == 'show_all':
        cur.execute("SELECT * FROM users")
        user = cur.fetchall()
        cards = {}
        do_not_have_cards = False
        for i in user:
            if i[0] == callback.message.chat.id:
                if json.loads(i[2]):
                    cards = json.loads(i[2])
                else:
                    do_not_have_cards = True
                break
        if not do_not_have_cards:
            items = list(map(lambda x: x[0], cards.items()))
            names = ''
            for i in range(1, len(all_cards) + 1):
                if str(i) in items:
                    names += f'\n{all_cards[str(i)][0]} x {cards[str(i)]}'
            bot.send_message(callback.message.chat.id, f'Все твои карты:{names}')
        else:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
    elif callback.data == 'show_common':
        cur.execute("SELECT * FROM users")
        user = cur.fetchall()
        cards = {}
        do_not_have_cards = False
        for i in user:
            if i[0] == callback.message.chat.id:
                if json.loads(i[2]):
                    cards = json.loads(i[2])
                else:
                    do_not_have_cards = True
                break
        if not do_not_have_cards:
            items = list(map(lambda x: x[0], cards.items()))
            names = ''
            for i in range(1, len(all_cards) + 1):
                if str(i) in items and all_cards[str(i)][4] == 'common':
                    names += f'\n{all_cards[str(i)][0]} x {cards[str(i)]}'
            if names != '':
                bot.send_message(callback.message.chat.id, f'Твои обычные карты:{names}')
            else:
                bot.send_message(callback.message.chat.id, 'У тебя пока нет обычных карт')
        else:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
    elif callback.data == 'show_rare':
        cur.execute("SELECT * FROM users")
        user = cur.fetchall()
        cards = {}
        do_not_have_cards = False
        for i in user:
            if i[0] == callback.message.chat.id:
                if json.loads(i[2]):
                    cards = json.loads(i[2])
                else:
                    do_not_have_cards = True
                break
        if not do_not_have_cards:
            items = list(map(lambda x: x[0], cards.items()))
            names = ''
            for i in range(1, len(all_cards) + 1):
                if str(i) in items and all_cards[str(i)][4] == 'rare':
                    names += f'\n{all_cards[str(i)][0]} x {cards[str(i)]}'
            if names != '':
                bot.send_message(callback.message.chat.id, f'Твои редкие карты:{names}')
            else:
                bot.send_message(callback.message.chat.id, 'У тебя пока нет редких карт')
        else:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
    elif callback.data == 'show_epic':
        cur.execute("SELECT * FROM users")
        user = cur.fetchall()
        cards = {}
        do_not_have_cards = False
        for i in user:
            if i[0] == callback.message.chat.id:
                if json.loads(i[2]):
                    cards = json.loads(i[2])
                else:
                    do_not_have_cards = True
                break
        if not do_not_have_cards:
            items = list(map(lambda x: x[0], cards.items()))
            names = ''
            for i in range(1, len(all_cards) + 1):
                if str(i) in items and all_cards[str(i)][4] == 'epic':
                    names += f'\n{all_cards[str(i)][0]} x {cards[str(i)]}'
            if names != '':
                bot.send_message(callback.message.chat.id, f'Твои эпические карты:{names}')
            else:
                bot.send_message(callback.message.chat.id, 'У тебя пока нет эпических карт')
        else:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
    elif callback.data == 'show_legendary':
        cur.execute("SELECT * FROM users")
        user = cur.fetchall()
        cards = {}
        do_not_have_cards = False
        for i in user:
            if i[0] == callback.message.chat.id:
                if json.loads(i[2]):
                    cards = json.loads(i[2])
                else:
                    do_not_have_cards = True
                break
        if not do_not_have_cards:
            items = list(map(lambda x: x[0], cards.items()))
            names = ''
            for i in range(1, len(all_cards) + 1):
                if str(i) in items and all_cards[str(i)][4] == 'legendary':
                    names += f'\n{all_cards[str(i)][0]} x {cards[str(i)]}'
            if names != '':
                bot.send_message(callback.message.chat.id, f'Твои легендарные карты:{names}')
            else:
                bot.send_message(callback.message.chat.id, 'У тебя пока нет легендарных карт')
        else:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
    cur.close()
    conn.close()


bot.polling(none_stop=True)
