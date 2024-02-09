import time
import telebot
import sqlite3
import json
import random
import datetime
from telebot import types


bot = telebot.TeleBot('6887806463:AAGFV6FPhnLj6Iy1-jAHfjcb3BmP10YXZh0')
bot.delete_webhook()
all_cards = {
    '1': ('Aston Martin Valkyrie (2018)', '2016 - 2019', '🇬🇧', '6.5 л / 1176 л.с. / бензин', 'legendary', 1176),
    '2': ('Mitsubishi Delica (1993)', '1968 - настоящее время', '🇯🇵', '2.5 л / 85 л.с. / дизель', 'common', 85),
    '3': ('Fiat Nuova 500 (1966)', '1957 - 1975', '🇮🇹', '0.5 л / 17 л.с. / бензин', 'common', 17),
    '4': ('Peugeot 208 (2014)', '2012 - настоящее время', '🇫🇷', '1.6 л / 92 л.с. / дизель', 'common', 92),
    '5': ('Renault Captur (2016)', '2013 - настоящее время', '🇫🇷', '1.6 л / 114 л.с. / бензин', 'common', 114),
    '6': ('Opel Astra (2014)', '1991 - настоящее время', '🇩🇪', '1.6 л / 115 л.с. / бензин', 'common', 115),
    '7': ('Infinity Q30 (2019)', '2015 - 2019', '🇬🇧', '2.0 л / 211 л.с. / бензин', 'rare', 211),
    '8': ('Bugatti Veyron (2007)', '2005 - 2015', '🇫🇷', '8.0 л / 1001 л.с. / бензин', 'legendary', 1001),
    '9': ('Volvo XC60 (2019)', '2008 - настоящее время', '🇸🇪', '2.0 л / 235 л.с./ дизель', 'rare', 235),
    '10': ('Alfa Romeo Giulia II (2019)', '2015 - настоящее время', '🇮🇹', ' 2.0 л / 280 л.с. / бензин', 'rare', 280),
    '11': ('Land Rover Defender 110 (1990)', '1983 - настоящее время', '🇬🇧', '2.5 л / 113 л.с. / дизель', 'common', 113),
    '12': ('Škoda Karoq (2017)', '2017 - настоящее время', '🇨🇿', '1.4 л / 150 л.с. / бензин', 'common', 150),
    '13': ('Tesla Model S (2015)', '2012 - настоящее время', '🇺🇸', '515 кВт / электро', 'epic', 515),
    '14': ('Ferrari F40 (1992)', '1987 - 1992', '🇮🇹', '2.9 л / 478 л.с. / бензин', 'legendary', 478),
    '15': ('Lamborghini Huracán (2022)', '2014 - настоящее время', '🇮🇹', '5.2 л / 640 л.с. / бензин', 'legendary', 640),
    '16': ('Range Rover Sport (2015)', '2005 - настоящее время', '🇬🇧', '4.4 л / 339 л.с./ дизель', 'epic', 339),
    '17': ('Nissan X-Trail T32 (2013)', '2000 - настоящее время', '🇯🇵', '2.0 л / 144 л.с. / бензин', 'common', 144),
    '18': ('Porsche 911 carrera 4S (2013)', '1963 - настоящее время', '🇩🇪', '3.8 л / 400 л.с. / бензин', 'epic', 400),
    '19': ('Maserati GrandTurismo (2013)', '2007 - настоящее время', '🇮🇹', '4.7 л / 460 л.с./ бензин', 'epic', 460),
    '20': ('Mazda 3 (2018)', '2003 - настоящее время', '🇯🇵', '1.5 л / 120 л.с./ бензин', 'common', 120),
    '21': ('Hyundai Solaris I рестайлинг (2014)', '2011 - настоящее время', '🇰🇷', '1.6 л / 123 л.с. / бензин', 'common', 123),
    '22': ('Lexus GS 300 (2018)', '1991 - 2020', '🇯🇵', '2.0 л / 245 л.с. / бензин', 'rare', 245),
    '23': ('Audi R8 V10 (2011)', '2007 - 2012', '🇩🇪', '5.2 л / 525 л.с. / бензин', 'epic', 525),
    '24': ('McLaren P1 (2015)', '2012 - 2017', '🇬🇧', '3.8 л / 650 л.с. / бензин', 'legendary', 650),
    '25': ('Bentley Mulsanne II (2010)', '2010 - 2020', '🇬🇧', '6.8 л / 512 л.с. / бензин', 'epic', 512),
    '26': ('BMW 3-й серии 325i (1986)', '1982 - 1994', '🇩🇪', '2.5 л / 170 л.с. / бензин', 'common', 170),
    '27': ('Mercedes-Benz S-Класс AMG 63 Long (2018)', '1999 - настоящее время', '🇩🇪', '4.0 л / 612 л.с. / бензин', 'epic', 612),
    '28': ('Toyota Camry (2019)', '1980 - настоящее время', '🇯🇵', '3.5 л / 249 л.с. / бензин', 'common', 249),
    '29': ('Toyota Supra A90 (2020)', '1986 - настоящее время', '🇯🇵', '3.0 л / 340 л.с. / бензин', 'epic', 340),
    '30': ('Hummer H3 (2008)', '2005 - 2010', '🇺🇸', '5.3 л / 300 л.с. / бензин', 'rare', 300),
    '31': ('Chevrolet Camaro VI (2016)', '2005 - 2018', '🇺🇸', '2.0 л / 275 л.с. / бензин', 'rare', 275),
    '32': ('Mercedes-Benz AMG GT (2017)', '2014 - 2017', '🇩🇪', '4.0 л / 462 л.с. / бензин', 'epic', 462),
    '33': ('Chevrolet Corvette (1993)', '1984 - 1998', '🇺🇸', '5.7 л / 300 л.с. / бензин', 'rare', 300),
    '34': ('Chevrolet Corvette Zr1 (2018)', '2013 - 2019', '🇺🇸', '6.2 л / 466 л.с. / бензин', 'epic', 466),
    '35': ('Ford Mustang (2005)', '2004 - 2009', '🇺🇸', '4.6 л / 315 л.с. / бензин', 'common', 315),
    '36': ('Ford Mustang (2017)', '2014 - 2017', '🇺🇸', '2.3 л / 317 л.с. / бензин', 'rare', 317),
    '37': ('Jeep Wrangler III (2011)', '2007 - 2018', '🇺🇸', '2.8 л / 200 л.с. / дизель', 'common', 200),
    '38': ('BMW M2 F87 (2017)', '2015 - 2021', '🇩🇪', '3.0 л / 370 л.с. / бензин', 'epic', 370),
    '39': ('Mercedes-Benz E-Класс (2018)', '1992 - настоящее время', '🇩🇪', '2.0 л / 184 л.с. / бензин', 'epic', 184)

}
for_random = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39']
rarities = (1, 3.928, 3.928, 3.928, 3.928, 3.928, 3.75, 1, 3.75, 3.75, 3.928, 3.928, 0.833, 1, 1, 0.833, 3.928, 0.833, 0.833, 3.928, 3.928, 3.75, 0.833, 1, 0.833, 3.928, 0.833, 3.928, 0.833, 3.75, 3.75, 0.833, 3.75, 0.833, 3.928, 3.75, 3.928, 0.833, 0.833)
skill_prices = [1000, 3000, 5000, 10000, 15000, 25000, 35000, 50000, 75000]
cooldown_prices = [100000, 200000]
time_for_cooldown_lvls = [14400, 10800, 7200]
cards_prices = {'common': 1000,
                'rare': 2500,
                'epic': 5000,
                'legendary': 10000}


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
    if minunte_value == '' and hour_value == '': return 'меньше минуты'
    return hour_value + minunte_value


@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('garage_data_base.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int primary key, number_of_cards int, cards VARCHAR, rating int, last_time VARCHAR, item_1 VARCHAR, item_2 VARCHAR, item_3 VARCHAR, item_4 VARCHAR, item_5 VARCHAR, num_1 int, num_2 int, num_3 int, num_4 int, num_5 int, username VARCHAR, driving_skill int, duel_wins int, influence_points int, card_cooldown_level int, dueling_with_id int, dueling_with_card VARCHAR, msg_to_delete int)')
    conn.commit()
    if cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE id = '%i')" % message.from_user.id).fetchone()[0] == 0:
        now = datetime.datetime.now()
        cur.execute("INSERT INTO users (id, number_of_cards, cards, rating, last_time, item_1, item_2, item_3, item_4, item_5, num_1, num_2, num_3, num_4, num_5, username, driving_skill, duel_wins, influence_points, card_cooldown_level, dueling_with_id, dueling_with_card, msg_to_delete) VALUES ('%i', '%i', '%s', '%i', '%s', '%s', '%s', '%s', '%s', '%s', '%i', '%i', '%i', '%i', '%i', '%s', '%i', '%i', '%i', '%i', '%i', '%s', '%i')" % (message.from_user.id, 0, '{}', 0, json.dumps((now.year, now.month, now.day, now.hour - 4, now.minute, now.second)), '[]', '[]', '[]', '[]', '[]', 0, 0, 0, 0, 0, '@' + message.from_user.username, 1, 0, 0, 1, 0, '0', 0))
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
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % message.from_user.id).fetchone()
        cards = json.loads(user[2])
        last_time = datetime.datetime(*json.loads(user[4]))
        cooldown_lvl = int(user[19])
        # time_for_cooldown_lvls[cooldown_lvl - 1]
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
            # time_for_cooldown_lvls[cooldown_lvl - 1]
            bot.send_message(message.chat.id, f'До следующей попытки {time_conversion(1 - (datetime.datetime.now() - last_time).seconds)}')
    elif message.text == 'Главное меню 🏠':
        markup = types.InlineKeyboardMarkup()
        prof = types.InlineKeyboardButton('Профиль 👤', callback_data=json.dumps(['profile', '']))
        deck = types.InlineKeyboardButton('Коллекция 🗃️', callback_data=json.dumps(['deck', '']))
        duel = types.InlineKeyboardButton('Начать дуэль ⚔️', callback_data=json.dumps(['duel', '']))
        shop = types.InlineKeyboardButton('Магазин 🛍', callback_data=json.dumps(['shop', '']))
        markup.row(prof, deck)
        markup.row(duel)
        markup.row(shop)
        bot.send_photo(message.chat.id, open('./garage_main.png', 'rb'), '🤔💭 Доступные действия:', reply_markup=markup)
    cur.close()
    conn.close()
    bot.register_next_step_handler(message, on_click)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    conn = sqlite3.connect('garage_data_base.sql')
    cur = conn.cursor()
    if json.loads(callback.data)[0] == 'profile':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        rating = user[3]
        duel_wins = user[17]
        driving_skill = user[16]
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, f'Имя:\n{callback.message.chat.first_name}\nРейтинг: {rating}\nПобед в дуэлях: {duel_wins}\nНавык вождения: {driving_skill}/10')
    elif json.loads(callback.data)[0] == 'deck':
        markup = types.InlineKeyboardMarkup()
        show_all = types.InlineKeyboardButton('🌌 Показать все карты', callback_data=json.dumps(['show_all', None]))
        show_legendary = types.InlineKeyboardButton('✨ Показать легендарные карты', callback_data=json.dumps(['show_legendary', '']))
        show_epic = types.InlineKeyboardButton('☄️ Показать эпические карты', callback_data=json.dumps(['show_epic', '']))
        show_rare = types.InlineKeyboardButton('🌎 Показать редкие карты', callback_data=json.dumps(['show_rare', '']))
        show_common = types.InlineKeyboardButton('🚀 Показать обычные карты', callback_data=json.dumps(['show_common', '']))
        sell_cards = types.InlineKeyboardButton('💵 Продать карты', callback_data=json.dumps(['sell_cards', '']))
        markup.row(show_all)
        markup.row(show_common)
        markup.row(show_rare)
        markup.row(show_epic)
        markup.row(show_legendary)
        markup.row(sell_cards)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        number = user[1]
        if number == 0:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
        elif str(number)[-1] != '1':
            bot.send_message(callback.message.chat.id, f'Твоя коллеция состоит из {number} карт', reply_markup=markup)
        else:
            bot.send_message(callback.message.chat.id, f'Твоя коллеция состоит из {number} карты', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'show_all':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        do_not_have_cards = False
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cards = set()
        if json.loads(user[2]):
            cards = json.loads(user[2])
        else:
            do_not_have_cards = True
        if not do_not_have_cards:
            markup = types.InlineKeyboardMarkup()
            items = list(map(lambda x: x[0], cards.items()))
            num = 0
            number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
            if len(items) > 1:
                next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card', '1']))
                markup.row(number_of_card, next_card)
            else:
                markup.add(number_of_card)
            bot.send_photo(callback.message.chat.id, open(f'./{items[num]}.jpg', 'rb'), all_cards[str(items[num])][0], reply_markup=markup)
            cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET item_1 = '%s' WHERE id = '%i'" % (json.dumps(items), callback.message.chat.id))
            conn.commit()
        else:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
    elif json.loads(callback.data)[0] == 'show_common':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        do_not_have_cards = False
        items = []
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cards = set()
        if json.loads(user[2]):
            cards = json.loads(user[2])
        else:
            do_not_have_cards = True
        if not do_not_have_cards:
            markup = types.InlineKeyboardMarkup()
            for i in cards.items():
                if all_cards[str(i[0])][4] == 'common': items.append(str(i[0]))
            num = 0
            number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
            if len(items) > 1:
                next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card', '2']))
                markup.row(number_of_card, next_card)
            else:
                markup.add(number_of_card)
            bot.send_photo(callback.message.chat.id, open(f'./{items[num]}.jpg', 'rb'), all_cards[str(items[num])][0], reply_markup=markup)
            cur.execute("UPDATE users SET num_2 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET item_2 = '%s' WHERE id = '%i'" % (json.dumps(items), callback.message.chat.id))
            conn.commit()
        else:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
    elif json.loads(callback.data)[0] == 'show_rare':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        cur.execute("SELECT * FROM users")
        do_not_have_cards = False
        items = []
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cards = set()
        if json.loads(user[2]):
            cards = json.loads(user[2])
        else:
            do_not_have_cards = True
        if not do_not_have_cards:
            markup = types.InlineKeyboardMarkup()
            for i in cards.items():
                if all_cards[str(i[0])][4] == 'rare': items.append(str(i[0]))
            num = 0
            number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
            if len(items) > 1:
                next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card', '3']))
                markup.row(number_of_card, next_card)
            else:
                markup.add(number_of_card)
            bot.send_photo(callback.message.chat.id, open(f'./{items[num]}.jpg', 'rb'), all_cards[str(items[num])][0], reply_markup=markup)
            cur.execute("UPDATE users SET num_3 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET item_3 = '%s' WHERE id = '%i'" % (json.dumps(items), callback.message.chat.id))
            conn.commit()
        else:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
    elif json.loads(callback.data)[0] == 'show_epic':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        do_not_have_cards = False
        items = []
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cards = set()
        if json.loads(user[2]):
            cards = json.loads(user[2])
        else:
            do_not_have_cards = True
        if not do_not_have_cards:
            markup = types.InlineKeyboardMarkup()
            for i in cards.items():
                if all_cards[str(i[0])][4] == 'epic': items.append(str(i[0]))
            num = 0
            number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
            if len(items) > 1:
                next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card', '4']))
                markup.row(number_of_card, next_card)
            else:
                markup.add(number_of_card)
            bot.send_photo(callback.message.chat.id, open(f'./{items[num]}.jpg', 'rb'), all_cards[str(items[num])][0], reply_markup=markup)
            cur.execute("UPDATE users SET num_4 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET item_4 = '%s' WHERE id = '%i'" % (json.dumps(items), callback.message.chat.id))
            conn.commit()
        else:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
    elif json.loads(callback.data)[0] == 'show_legendary':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        do_not_have_cards = False
        items = []
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cards = set()
        if json.loads(user[2]):
            cards = json.loads(user[2])
        else:
            do_not_have_cards = True
        if not do_not_have_cards:
            markup = types.InlineKeyboardMarkup()
            for i in cards.items():
                if all_cards[str(i[0])][4] == 'legendary': items.append(str(i[0]))
            num = 0
            number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
            if len(items) > 1:
                next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card', '5']))
                markup.row(number_of_card, next_card)
            else:
                markup.add(number_of_card)
            bot.send_photo(callback.message.chat.id, open(f'./{items[num]}.jpg', 'rb'), all_cards[str(items[num])][0], reply_markup=markup)
            cur.execute("UPDATE users SET num_5 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET item_5 = '%s' WHERE id = '%i'" % (json.dumps(items), callback.message.chat.id))
            conn.commit()
        else:
            bot.send_message(callback.message.chat.id, 'У тебя пока нет карт')
    elif json.loads(callback.data)[0] == 'next_card':
        item_num = int(json.loads(callback.data)[1])
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        items = json.loads(user[4 + item_num])
        num = int(user[9 + item_num]) + 1
        cur.execute("UPDATE users SET num_%i = '%i' WHERE id = '%i'" % (item_num, num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        if num + 1 != len(items):
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card', item_num]))
            previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['previous_card', item_num]))
            markup.row(previous_card, number_of_card, next_card)
        else:
            previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['previous_card', item_num]))
            markup.row(previous_card, number_of_card)
        file = types.InputMedia(type='photo', media=open(f'./{items[num]}.jpg', 'rb'), caption=all_cards[str(items[num])][0])
        bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'previous_card':
        item_num = int(json.loads(callback.data)[1])
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        items = json.loads(user[4 + item_num])
        num = int(user[9 + item_num]) - 1
        cur.execute("UPDATE users SET num_%i = '%i' WHERE id = '%i'" % (item_num, num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        if num != 0:
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card', item_num]))
            previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['previous_card', item_num]))
            markup.row(previous_card, number_of_card, next_card)
        else:
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card', item_num]))
            markup.row(number_of_card, next_card)
        file = types.InputMedia(type='photo', media=open(f'./{items[num]}.jpg', 'rb'),caption=all_cards[str(items[num])][0])
        bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'duel':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        if int(user[1]) == 0: bot.send_message(callback.message.chat.id, 'У тебя ещё нет карт, чтобы учавстовать в дуэлях тебе нужна хотя бы одна карта')
        else:
            markup = types.InlineKeyboardMarkup()
            cancel = types.InlineKeyboardButton('🚫 Отменить действие', callback_data=json.dumps(['cancel', '']))
            markup.add(cancel)
            bot.send_message(callback.message.chat.id, '🛣️ Ты зашел в режим дуэли\nЗдесь ты можешь учасвстовать в гонках 1 на 1 с другими пользователями\nПобедитель определяется случайно, шансы зависят от навыка вождения и от двигателя выбранного автомобиля\nПобедивший игрок забирает карту проигравшего\nУдачных заездов 🍀\n🏎 Введи @username пользователя, с которым хочешь начать дуэль', reply_markup=markup)
            bot.clear_step_handler_by_chat_id(callback.message.chat.id)
            bot.register_next_step_handler(callback.message, duels)
    elif json.loads(callback.data)[0] == 'cancel':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.clear_step_handler_by_chat_id(callback.message.chat.id)
        bot.register_next_step_handler(callback.message, on_click)
    elif json.loads(callback.data)[0] == 'accept':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(int(json.loads(callback.data)[1]), f'✅ {json.loads(callback.data)[3]} принял твое предложение')
        id1 = int(json.loads(callback.data)[1])
        id2 = int(json.loads(callback.data)[2])
        cur.execute("UPDATE users SET dueling_with_id = '%i' WHERE id = '%i'" % (id2, id1))
        conn.commit()
        cur.execute("UPDATE users SET dueling_with_id = '%i' WHERE id = '%i'" % (id1, id2))
        conn.commit()
        user1 = cur.execute("SELECT * FROM users WHERE id = '%i'" % id1).fetchone()
        user2 = cur.execute("SELECT * FROM users WHERE id = '%i'" % id2).fetchone()
        cards = json.loads(user1[2])
        markup = types.InlineKeyboardMarkup()
        items = list(map(lambda x: x[0], cards.items()))
        num = 0
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        choose = types.InlineKeyboardButton('👉 Выбрать карту для дуэли', callback_data=json.dumps(['choose', num]))
        leave = types.InlineKeyboardButton('🚪 Выйти из дуэли', callback_data=json.dumps(['leave_duel', '']))
        if len(items) > 1:
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card_duel', '']))
            markup.row(number_of_card, next_card)
        else:
            markup.row(number_of_card)
        markup.row(choose)
        markup.row(leave)
        msg1 = bot.send_photo(id1, open(f'./{items[num]}.jpg', 'rb'), f'{all_cards[str(items[num])][0]}\nДвигатель: {all_cards[str(items[num])][3]}', reply_markup=markup)
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, id1))
        conn.commit()
        cur.execute("UPDATE users SET item_1 = '%s' WHERE id = '%i'" % (json.dumps(items), id1))
        conn.commit()
        cur.execute("UPDATE users SET msg_to_delete = '%i' WHERE id = '%i'" % (msg1.message_id, id1))
        conn.commit()
        cards = json.loads(user2[2])
        markup = types.InlineKeyboardMarkup()
        items = list(map(lambda x: x[0], cards.items()))
        num = 0
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        choose = types.InlineKeyboardButton('👉 Выбрать карту для дуэли', callback_data=json.dumps(['choose', num]))
        leave = types.InlineKeyboardButton('🚪 Выйти из дуэли', callback_data=json.dumps(['leave_duel', '']))
        if len(items) > 1:
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card_duel', '']))
            markup.row(number_of_card, next_card)
        else:
            markup.row(number_of_card)
        markup.row(choose)
        markup.row(leave)
        msg2 = bot.send_photo(id2, open(f'./{items[num]}.jpg', 'rb'), f'{all_cards[str(items[num])][0]}\nДвигатель: {all_cards[str(items[num])][3]}', reply_markup=markup)
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, id2))
        conn.commit()
        cur.execute("UPDATE users SET item_1 = '%s' WHERE id = '%i'" % (json.dumps(items), id2))
        conn.commit()
        cur.execute("UPDATE users SET msg_to_delete = '%i' WHERE id = '%i'" % (msg2.message_id, id2))
        conn.commit()
    elif json.loads(callback.data)[0] == 'decline':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        msg = bot.send_message(int(json.loads(callback.data)[1]), f'❌ {json.loads(callback.data)[2]} отклонил твое предложение')
        bot.clear_step_handler_by_chat_id(int(json.loads(callback.data)[1]))
        bot.register_next_step_handler(msg, on_click)
        bot.clear_step_handler_by_chat_id(callback.message.chat.id)
        bot.register_next_step_handler(callback.message, on_click)
    elif json.loads(callback.data)[0] == 'next_card_duel':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        items = json.loads(user[5])
        num = int(user[10]) + 1
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        choose = types.InlineKeyboardButton('👉 Выбрать карту для дуэли', callback_data=json.dumps(['choose', num]))
        leave = types.InlineKeyboardButton('🚪 Выйти из дуэли', callback_data=json.dumps(['leave_duel', '']))
        if num + 1 != len(items):
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card_duel', '']))
            previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['previous_card_duel', '']))
            markup.row(previous_card, number_of_card, next_card)
        else:
            previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['previous_card_duel', '']))
            markup.row(previous_card, number_of_card)
        markup.row(choose)
        markup.row(leave)
        file = types.InputMedia(type='photo', media=open(f'./{items[num]}.jpg', 'rb'), caption=f'{all_cards[str(items[num])][0]}\nДвигатель: {all_cards[str(items[num])][3]}')
        bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'previous_card_duel':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        items = json.loads(user[5])
        num = int(user[10]) - 1
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        choose = types.InlineKeyboardButton('👉 Выбрать карту для дуэли', callback_data=json.dumps(['choose', num]))
        leave = types.InlineKeyboardButton('🚪 Выйти из дуэли', callback_data=json.dumps(['leave_duel', '']))
        if num != 0:
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card_duel', '']))
            previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['previous_card_duel', '']))
            markup.row(previous_card, number_of_card, next_card)
        else:
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card_duel', '']))
            markup.row(number_of_card, next_card)
        markup.row(choose)
        markup.row(leave)
        file = types.InputMedia(type='photo', media=open(f'./{items[num]}.jpg', 'rb'),caption=f'{all_cards[str(items[num])][0]}\nДвигатель: {all_cards[str(items[num])][3]}')
        bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'choose':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user1 = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        id2 = int(user1[20])
        user2 = cur.execute("SELECT * FROM users WHERE id = '%i'" % id2).fetchone()
        card1 = json.loads(user1[5])[int(json.loads(callback.data)[1])]
        cur.execute("UPDATE users SET dueling_with_card = '%s' WHERE id = '%i'" % (card1, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        leave = types.InlineKeyboardButton('🚪 Выйти из дуэли', callback_data=json.dumps(['leave_duel', '']))
        markup.add(leave)
        bot.send_photo(callback.message.chat.id, open(f'./{card1}.jpg', 'rb'), f'<b>Ты выбрал</b>\n{all_cards[card1][0]}\nДвигатель: {all_cards[card1][3]}', parse_mode='html', reply_markup=markup)
        if user2[21] != '0':
            card2 = user2[21]
            bot.send_photo(callback.message.chat.id, open(f'./{card2}.jpg', 'rb'), f'<b>Твой противник выбрал</b>\n{all_cards[card2][0]}\nДвигатель: {all_cards[card2][3]}', parse_mode='html')
            bot.send_photo(id2, open(f'./{card1}.jpg', 'rb'), f'<b>Твой противник выбрал</b>\n{all_cards[card1][0]}\nДвигатель: {all_cards[card1][3]}', parse_mode='html')
            bot.send_message(callback.message.chat.id, 'Гонка началась')
            bot.send_message(id2, 'Гонка началась')
            power1 = all_cards[card1][5] * user1[16]
            power2 = all_cards[card2][5] * user2[16]
            chances = [50, 50]
            if power1 > power2 : chances = [100 - (power2 / power1) * 100, power2 / power1 * 100]
            elif power1 < power2: chances = [100 - (power1 / power2) * 100, power1 / power2 * 100]
            participants = [1, 2]
            winner = random.choices(participants, k=1, weights=chances)
            msg1 = bot.send_message(callback.message.chat.id, 'Гонка закончится через 5...')
            msg2 = bot.send_message(id2, 'Гонка закончится через 5...')
            for i in range(4, 0, -1):
                time.sleep(1.0)
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=msg1.message_id, text=f'Гонка закончится через {i}...')
                bot.edit_message_text(chat_id=id2, message_id=msg2.message_id, text=f'Гонка закончится через {i}...')
            bot.delete_message(callback.message.chat.id, msg1.message_id)
            bot.delete_message(id2, msg2.message_id)
            if winner == 1: win_username = user1[15]
            else: win_username = user2[15]
            bot.send_message(callback.message.chat.id, f'<b>Победил</b> {win_username}', parse_mode='html')
            msg = bot.send_message(id2, f'<b>Победил</b> {win_username}', parse_mode='html')
            cards1 = json.loads(user1[2])
            cards2 = json.loads(user2[2])
            if winner == 1:
                if str(card2) in list(map(lambda x: x[0], cards1.items())):
                    cards1[card2] += 1
                else:
                    cards1[card2] = 1
                cards2[card2] -= 1
                if cards2[card2] == 0: del cards2[card2]
                cur.execute("UPDATE users SET number_of_cards = number_of_cards + 1 WHERE id = '%i'" % callback.message.chat.id)
                conn.commit()
                cur.execute("UPDATE users SET number_of_cards = number_of_cards - 1 WHERE id = '%i'" % id2)
                conn.commit()
            else:
                if str(card1) in list(map(lambda x: x[0], cards2.items())):
                    cards2[card1] += 1
                else:
                    cards2[card1] = 1
                cards1[card1] -= 1
                if cards1[card1] == 0: del cards1[card1]
                cur.execute("UPDATE users SET number_of_cards = number_of_cards + 1 WHERE id = '%i'" % id2)
                conn.commit()
                cur.execute("UPDATE users SET number_of_cards = number_of_cards - 1 WHERE id = '%i'" % callback.message.chat.id)
                conn.commit()
            cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards1), callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards2), id2))
            conn.commit()
            cur.execute("UPDATE users SET dueling_with_id = '%i' WHERE id = '%i'" % (0, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET dueling_with_card = '%s' WHERE id = '%i'" % ('0', callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET dueling_with_id = '%i' WHERE id = '%i'" % (0, id2))
            conn.commit()
            cur.execute("UPDATE users SET dueling_with_card = '%s' WHERE id = '%i'" % ('0', id2))
            conn.commit()
            bot.register_next_step_handler(callback.message, on_click)
            bot.register_next_step_handler(msg, on_click)
    elif json.loads(callback.data)[0] == 'leave_duel':
        user1 = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        id2 = int(user1[20])
        user2 = cur.execute("SELECT * FROM users WHERE id = '%i'" % id2).fetchone()
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        cur.execute("UPDATE users SET dueling_with_id = '%i' WHERE id = '%i'" % (0, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET dueling_with_card = '%s' WHERE id = '%i'" % ('0', callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET dueling_with_id = '%i' WHERE id = '%i'" % (0, id2))
        conn.commit()
        cur.execute("UPDATE users SET dueling_with_card = '%s' WHERE id = '%i'" % ('0', id2))
        conn.commit()
        bot.register_next_step_handler(callback.message, on_click)
        msg = bot.send_message(id2, 'Твой оппонент вышел из дуэли')
        del_id = int(user2[22])
        bot.delete_message(id2, del_id)
        bot.register_next_step_handler(msg, on_click)
    elif json.loads(callback.data)[0] == 'shop':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        influence_points = int(user[18])
        markup = types.InlineKeyboardMarkup()
        upgrade_skill = types.InlineKeyboardButton('⏫ Повысить уровень навыка вождения', callback_data=json.dumps(['up_skill', '']))
        upgrade_time = types.InlineKeyboardButton('⏬ Уменьшить время между получением новых карт', callback_data=json.dumps(['up_time', '']))
        markup.row(upgrade_skill)
        markup.row(upgrade_time)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, f'🛒 Магазин гаража, здесь ты можешь купить разные улучшения за очки влияния\nТвои очки влияния: {influence_points}', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'up_skill':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        driving_skill = int(user[16])
        if driving_skill != 10:
            markup = types.InlineKeyboardMarkup()
            buy = types.InlineKeyboardButton('✅ Приобрести улучшение', callback_data=json.dumps(['buy_skill', '']))
            cancel = types.InlineKeyboardButton('🚫 Отменить действие', callback_data=json.dumps(['cancel', '']))
            markup.add(buy, cancel)
            bot.send_message(callback.message.chat.id, f'🆙 Улучшение навыка вождения до {driving_skill + 1} уровня за {skill_prices[driving_skill - 1]} очков влияния', reply_markup=markup)
        else:
            bot.send_message(callback.message.chat.id, 'У тебя максимальный навык вождения')
    elif json.loads(callback.data)[0] == 'up_time':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cooldown_level = int(user[19])
        if cooldown_level != 3:
            markup = types.InlineKeyboardMarkup()
            buy = types.InlineKeyboardButton('✅ Приобрести улучшение', callback_data=json.dumps(['buy_cooldown', '']))
            cancel = types.InlineKeyboardButton('🚫 Отменить действие', callback_data=json.dumps(['cancel', '']))
            markup.add(buy, cancel)
            bot.send_message(callback.message.chat.id, f'⏱️ Уменьшение времени между получением новых карт до {cooldown_level + 1} уровня за {cooldown_prices[cooldown_level - 1]} очков влияния', reply_markup=markup)
        else:
            bot.send_message(callback.message.chat.id, 'У тебя максимальный уровень уменьшения времени между получением новых карт')
    elif json.loads(callback.data)[0] == 'buy_skill':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        driving_skill = int(user[16])
        influence_points = int(user[18])
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        if influence_points >= skill_prices[driving_skill - 1]:
            influence_points -= skill_prices[driving_skill - 1]
            driving_skill += 1
            cur.execute("UPDATE users SET influence_points = '%i' WHERE id = '%i'" % (influence_points, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET driving_skill = '%i' WHERE id = '%i'" % (driving_skill, callback.message.chat.id))
            conn.commit()
            bot.send_message(callback.message.chat.id, f'✅ Улучшение навыка вождения до {driving_skill} уровня успешно приобретено')
        else:
            bot.send_message(callback.message.chat.id, f'У тебя не хватает очков влияния для покупки этого улучшения, тебе нужно ещё {skill_prices[driving_skill - 1] - influence_points}')
    elif json.loads(callback.data)[0] == 'buy_cooldown':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        card_cooldown_level = int(user[16])
        influence_points = int(user[18])
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        if influence_points >= cooldown_prices[card_cooldown_level - 1]:
            influence_points -= cooldown_prices[card_cooldown_level - 1]
            card_cooldown_level += 1
            cur.execute("UPDATE users SET influence_points = '%i' WHERE id = '%i'" % (influence_points, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET card_cooldown_level = '%i' WHERE id = '%i'" % (card_cooldown_level, callback.message.chat.id))
            conn.commit()
            bot.send_message(callback.message.chat.id, f'✅ Улучшение навыка вождения до {card_cooldown_level} уровня успешно приобретено')
        else:
            bot.send_message(callback.message.chat.id, f'У тебя не хватает очков влияния для покупки этого улучшения, тебе нужно ещё {cooldown_prices[card_cooldown_level - 1] - influence_points}')
    elif json.loads(callback.data)[0] == 'sell_cards':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        do_not_have_cards = False
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cards = set()
        if json.loads(user[2]):
            cards = json.loads(user[2])
        else:
            do_not_have_cards = True
        if not do_not_have_cards:
            markup = types.InlineKeyboardMarkup()
            items = list(map(lambda x: x[0], cards.items()))
            num = 0
            number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
            if len(items) > 1:
                next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card_sell', '']))
                markup.row(number_of_card, next_card)
            else:
                markup.add(number_of_card)
            if cards[items[num]] > 1:
                sell_all_but_one = types.InlineKeyboardButton('Продать все дубликаты', callback_data=json.dumps(['sell_all_but_one', items[num]]))
                sell_all = types.InlineKeyboardButton('Продать все карты', callback_data=json.dumps(['sell_all', items[num]]))
                markup.row(sell_all_but_one)
                markup.row(sell_all)
            else:
                sell_one = types.InlineKeyboardButton('Продать карту', callback_data=json.dumps(['sell_one', items[num]]))
                markup.row(sell_one)
            bot.send_photo(callback.message.chat.id, open(f'./{items[num]}.jpg', 'rb'), f'{all_cards[str(items[num])][0]}\nКоличество: {cards[items[num]]}', reply_markup=markup)
            cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET item_1 = '%s' WHERE id = '%i'" % (json.dumps(items), callback.message.chat.id))
            conn.commit()
        else:
            bot.send_message(callback.message.chat.id, 'У тебя нет карт')
    elif json.loads(callback.data)[0] == 'next_card_sell':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        items = json.loads(user[5])
        num = int(user[10]) + 1
        cards = json.loads(user[2])
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        if num + 1 != len(items):
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card_sell', '']))
            previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['previous_card_sell', '']))
            markup.row(previous_card, number_of_card, next_card)
        else:
            previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['previous_card_sell', '']))
            markup.row(previous_card, number_of_card)
        if cards[items[num]] > 1:
            sell_all_but_one = types.InlineKeyboardButton('Продать все дубликаты', callback_data=json.dumps(['sell_all_but_one', items[num]]))
            sell_all = types.InlineKeyboardButton('Продать все карты', callback_data=json.dumps(['sell_all', items[num]]))
            markup.row(sell_all_but_one)
            markup.row(sell_all)
        else:
            sell_one = types.InlineKeyboardButton('Продать карту', callback_data=json.dumps(['sell_one', items[num]]))
            markup.row(sell_one)
        file = types.InputMedia(type='photo', media=open(f'./{items[num]}.jpg', 'rb'), caption=f'{all_cards[str(items[num])][0]}\nКоличество: {cards[items[num]]}')
        bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'previous_card_sell':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        items = json.loads(user[5])
        num = int(user[10]) - 1
        cards = json.loads(user[2])
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        if num != 0:
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card_sell', '']))
            previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['previous_card_sell', '']))
            markup.row(previous_card, number_of_card, next_card)
        else:
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['next_card_sell', '']))
            markup.row(number_of_card, next_card)
        if cards[items[num]] > 1:
            sell_all_but_one = types.InlineKeyboardButton('Продать все дубликаты', callback_data=json.dumps(['sell_all_but_one', items[num]]))
            sell_all = types.InlineKeyboardButton('Продать все карты', callback_data=json.dumps(['sell_all', items[num]]))
            markup.row(sell_all_but_one)
            markup.row(sell_all)
        else:
            sell_one = types.InlineKeyboardButton('Продать карту', callback_data=json.dumps(['sell_one', items[num]]))
            markup.row(sell_one)
        file = types.InputMedia(type='photo', media=open(f'./{items[num]}.jpg', 'rb'),caption=f'{all_cards[str(items[num])][0]}\nКоличество: {cards[items[num]]}')
        bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'sell_all':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        num = int(user[10]) - 1
        item_num = json.loads(callback.data)[1]
        cards = json.loads(user[2])
        items = list(map(lambda x: x[0], cards.items()))
        num_cards = cards[item_num]
        price_of_card = cards_prices[all_cards[item_num][4]]
        del cards[item_num]
        cur.execute("UPDATE users SET influence_points = influence_points + '%i' WHERE id = '%i'" % (num_cards * price_of_card, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET number_of_cards = number_of_cards - '%i' WHERE id = '%i'" % (num_cards, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards), callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET item_1 = '%s' WHERE id = '%i'" % (json.dumps(items), callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        if len(cards) != 0:
            sell_more = types.InlineKeyboardButton('↩️ Продать ещё карты', callback_data=json.dumps(['sell_cards', '']))
            markup.add(sell_more)
        bot.send_message(callback.message.chat.id, f'Ты продал карты на сумму {num_cards * price_of_card} очков влияния', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'sell_one':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        item_num = json.loads(callback.data)[1]
        num = int(user[10]) - 1
        cards = json.loads(user[2])
        items = list(map(lambda x: x[0], cards.items()))
        price_of_card = cards_prices[all_cards[item_num][4]]
        del cards[item_num]
        cur.execute("UPDATE users SET influence_points = influence_points + '%i' WHERE id = '%i'" % (price_of_card, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET number_of_cards = number_of_cards - 1 WHERE id = '%i'" % callback.message.chat.id)
        conn.commit()
        cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards), callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET item_1 = '%s' WHERE id = '%i'" % (json.dumps(items), callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        if len(cards) != 0:
            sell_more = types.InlineKeyboardButton('↩️ Продать ещё карты', callback_data=json.dumps(['sell_cards', '']))
            markup.add(sell_more)
        bot.send_message(callback.message.chat.id, f'Ты продал карту за {price_of_card} очков влияния', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'sell_all_but_one':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        item_num = json.loads(callback.data)[1]
        cards = json.loads(user[2])
        num_cards = cards[item_num] - 1
        price_of_card = cards_prices[all_cards[item_num][4]]
        cards[item_num] = 1
        cur.execute("UPDATE users SET influence_points = influence_points + '%i' WHERE id = '%i'" % (num_cards * price_of_card, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET number_of_cards = number_of_cards - '%i' WHERE id = '%i'" % (num_cards, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards), callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        if len(cards) != 0:
            sell_more = types.InlineKeyboardButton('↩️ Продать ещё карты', callback_data=json.dumps(['sell_cards', '']))
            markup.add(sell_more)
        bot.send_message(callback.message.chat.id, f'Ты продал карты на сумму {num_cards * price_of_card} очков влияния', reply_markup=markup)
    cur.close()
    conn.close()


def duels(message):
    conn = sqlite3.connect('garage_data_base.sql')
    cur = conn.cursor()
    bot.delete_message(message.chat.id, message.message_id - 1)
    if message.text[0] == '@':
        if cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username = '%s')" % message.text).fetchone()[0]:
            user = cur.execute("SELECT * FROM users WHERE username = '%s'" % message.text).fetchone()
            if int(user[1]) == 0:
                bot.send_message(message.chat.id, 'У этого пользователя ещё нет карт')
                bot.register_next_step_handler(message, on_click)
            else:
                ida = int(user[0])
                markup = types.InlineKeyboardMarkup()
                accept = types.InlineKeyboardButton('✅ Принять', callback_data=json.dumps(['accept', message.from_user.id, ida, message.text]))
                decline = types.InlineKeyboardButton('❌ Отклонить', callback_data=json.dumps(['decline', message.from_user.id, message.text]))
                markup.row(accept, decline)
                bot.send_message(ida, f'❗️ Пользователь {message.from_user.username} предложил вам провести дуэль', reply_markup=markup)
                bot.clear_step_handler_by_chat_id(ida)
                markup = types.InlineKeyboardMarkup()
                cancel_offer = types.InlineKeyboardButton('🚫 Отменить предложение', callback_data=json.dumps(['cancel_offer', ida]))
                markup.add(cancel_offer)
                bot.send_message(message.chat.id, 'Предложение успешно отправлено', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Пользователь с таким @username ещё ни разу не запускал эту игру(')
            bot.register_next_step_handler(message, on_click)
    else:
        markup = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton('🚫 Отменить действие', callback_data=json.dumps(['cancel', '']))
        markup.add(cancel)
        bot.send_message(message.chat.id, 'Ты ввёл @username неправильно, попробуй ещё раз, возможно ты забыл знак @', reply_markup=markup)
        bot.register_next_step_handler(message, duels)
    cur.close()
    conn.close()


bot.polling(none_stop=True)
