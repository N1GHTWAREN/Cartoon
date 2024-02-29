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
    '39': ('Mercedes-Benz E-Класс (2018)', '1992 - настоящее время', '🇩🇪', '2.0 л / 184 л.с. / бензин', 'epic', 184),
    '40': ('Lexus RX (2018)', '1997 - настоящее время', '🇯🇵', '2.0 л / 238 л.с. / бензин', 'rare', 238),
    '41': ('Lexus LX (2019)', '1995 - настоящее время', '🇯🇵', '5.7 л / 367 л.с. / бензин', 'epic', 367),
    '42': ('Dodge Viper (2017)', '1992 - 2017', '🇺🇸', '8.3 л / 507 л.с. / Бензин', 'epic', 507),
    '43': ('Rolls-Royce Ghost (2013)', '2010 - настоящее время', '🇬🇧', '6.6 л / 570 л.с. / Бензин', 'epic', 570),
    '44': ('Aston Martin DB11 (2017)', '2016 - 2023', '🇬🇧', '5.2 л / 608 л.с. / Бензин', 'epic', 608),
    '45': ('Bentley Bentayga (2019)', '2015 - настоящее время', '🇬🇧', '4.0 л / 435 л.с. / Бензин', 'epic', 435),
    '46': ('Checker Marathon (1982)', '1960 - 1982', '🇺🇸', '5.7 л / 250 л.с. / Дизель', 'common', 250),
    '47': ('Volkswagen Transporter T1 (1967)', '1950 - 1967', '🇩🇪', '1.5 л / 44 л.с. / Бензин', 'common', 44),
    '48': ('Mercedes-Benz S-класс (2019)', '1991 - настоящее время', '🇩🇪', '2.9 л / 340 л.с. / бензин', 'epic', 340),
    '49': ('Mercedes-Benz V-класс (2014)', '1996 - настоящее время', '🇩🇪', '2.1 л / 190 л.с. / дизель', 'rare', 190),
    '50': ('Mercedes-Benz G-класс AMG (2017)', '1994 - настоящее время', '🇩🇪', '5.5 л / 571 л.с. / бензин', 'epic', 571),
    '51': ('BMW X5 G05 (2018)', '1999 - настоящее время', '🇩🇪', '3.0 л / 340 л.с. / бензин', 'epic', 340),
    '52': ('Audi RS3 (2016)', '2011 - настоящее время', '🇩🇪', '2.5 л / 340 л.с. / бензин', 'rare', 340),
    '53': ('Volkswagen Passat (2015)', '2008 - настоящее время', '🇩🇪', '2.0 л / 170 л.с. / дизель', 'common', 170),
    '54': ('Ford Focus (2013)', '1998 - настоящее время', '🇺🇸', '1.6 л / 125 л.с. / бензин', 'common', 125),
    '55': ('BMW M5 F90 (2019)', '1985 - настоящее время', '🇩🇪', '4.4 л / 625 л.с. / Бензин', 'epic', 625),
    '56': ('Lamborghini Veneno (2014)', '2013 - 2014', '🇮🇹', '6.5 л / 750 л.с. / Бензин', 'special', 750),
    '57': ('Pagani Zonda (2019)', '1999 - 2019', '🇮🇹', '7.3 л / 602 л.с. / Бензин', 'special', 602),
    '58': ('Koenigsegg One:1 (2016)', '2014 - 2016', '🇸🇪', '5.0 л / 1360 л.с. / Бензин', 'special', 1360)
}
for_random = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55']
rarities = (0.1, 4, 4, 4, 4, 4, 2.27, 0.1, 2.27, 2.27, 4, 4, 0.12, 0.1, 0.1, 0.12, 4, 0.12, 0.12, 4, 4, 2.27, 0.12, 0.1, 0.12, 4, 0.12, 4, 0.12, 2.27, 2.27, 0.12, 2.27, 0.12, 4, 2.27, 4, 0.12, 0.12, 2.27, 0.12, 0.12, 0.12, 0.12, 0.12, 4, 4, 0.12, 2.27, 0.12, 0.12, 2.27, 4, 4, 0.12)
epic_random = ['13', '16', '18', '19', '23', '25', '27', '29', '32', '34', '38', '39', '41', '42', '43', '44', '45', '48', '50', '51', '55']
legendary_random = ['1', '8', '14', '15', '24']
skill_prices = [1000, 3000, 5000, 10000, 15000, 25000, 35000, 50000, 75000]
cooldown_prices = [100000, 200000]
time_for_cooldown_lvls = [14400, 10800, 7200]
cards_prices = {'common': 1000,
                'rare': 2500,
                'epic': 5000,
                'legendary': 10000,
                'special': 15000}
rarity_test = {'legendary': ('Легендарная', 3000),
               'epic': ('Эпическая', 1500),
               'rare': ('Редкая', 500),
               'common': ('Обычная', 250),
               'special': ('Специальная', 5000)}
specials = ['56', '57', '58']


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
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int primary key, number_of_cards int, cards VARCHAR, rating int, last_time VARCHAR, item_1 VARCHAR, item_2 VARCHAR, item_3 VARCHAR, item_4 VARCHAR, item_5 VARCHAR, num_1 int, num_2 int, num_3 int, num_4 int, num_5 int, username VARCHAR, driving_skill int, duel_wins int, influence_points int, card_cooldown_level int, dueling_with_id int, dueling_with_card VARCHAR, msg_to_delete int, rolls int, last_dice VARCHAR, using_for_craft_common int, using_for_craft_rare int, using_for_craft_epic int, using_for_craft_legendary int, using_for_trade VARCHAR, details int, slots_rolls int)')
    conn.commit()
    if cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE id = '%i')" % message.from_user.id).fetchone()[0] == 0:
        now = datetime.datetime.today() - datetime.timedelta(hours=4)
        now1 = datetime.datetime.today() - datetime.timedelta(days=7)
        cur.execute("INSERT INTO users (id, number_of_cards, cards, rating, last_time, item_1, item_2, item_3, item_4, item_5, num_1, num_2, num_3, num_4, num_5, username, driving_skill, duel_wins, influence_points, card_cooldown_level, dueling_with_id, dueling_with_card, msg_to_delete, rolls, last_dice, using_for_craft_common, using_for_craft_rare, using_for_craft_epic, using_for_craft_legendary, using_for_trade, details, slots_rolls) VALUES ('%i', '%i', '%s', '%i', '%s', '%s', '%s', '%s', '%s', '%s', '%i', '%i', '%i', '%i', '%i', '%s', '%i', '%i', '%i', '%i', '%i', '%s', '%i', '%i', '%s', '%i', '%i', '%i', '%i', '%s', '%i', '%i')" % (message.from_user.id, 0, '{}', 0, json.dumps((now.year, now.month, now.day, now.hour - 4, now.minute, now.second)), '[]', '[]', '[]', '[]', '[]', 0, 0, 0, 0, 0, '@' + message.from_user.username, 1, 0, 0, 1, 0, '0', 0, 0, json.dumps((now1.year, now1.month, now1.day, now1.hour, now1.minute, now1.second)), 0, 0, 0, 0, '0', 10000, 0))
        conn.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    new_card = types.KeyboardButton('Получить новую карту 🚗')
    menu = types.KeyboardButton('Главное меню 🏠')
    markup.add(new_card, menu)
    bot.send_message(message.chat.id, f'👋 Привет, <b><em>{message.from_user.first_name}</em></b>, рад тебя видеть в гараже!\n\n🎮 Здесь ты можешь собрать коллекцию из своих любимых машин, устраивать дуэли с друзьями, торговать своими карточками и играть в мини игры.\n\n🃏 Всего 4 вида карт: обычные, редкие, эпические и легендарные. За получение карточки ты поднимаешь свой <b><em>рейтинг</em></b>, чем реже карта, тем больше ты получишь за нее рейтинга.\n\n💰 Ты можешь продавать дупликаты или не нужные тебе карты в твоей коллекции, за продажу карт, а также за еженедельные задания ты можешь получать <b><em>очки влияния</em></b>, за которые, в свою очередь, можешь купить улучшения твоего персонажа или гаража.\n\nНу что, ты готов получить свою первую машину? Нажимай кнопку <b><em>"Получить новую карту"</em></b>, приятной игры! 🍀\n\n🧠 Если хочешь указать на ошибку или предложить что-то новое, то можешь написать нам на почту:\ncartoongaragehelp@mail.ru', parse_mode='html', reply_markup=markup)
    bot.clear_step_handler_by_chat_id(message.chat.id)
    user = cur.execute("SELECT * FROM users WHERE id = '%i'" % message.from_user.id).fetchone()
    if int(user[20]) != 0:
        id2 = int(user[20])
        cur.execute("UPDATE users SET dueling_with_id = 0 WHERE id = '%i'" % message.chat.id)
        conn.commit()
        cur.execute("UPDATE users SET dueling_with_id = 0 WHERE id = '%i'" % id2)
        conn.commit()
        msg = bot.send_message(id2, 'Пользователь перезапустил бота')
        bot.clear_step_handler_by_chat_id(id2)
        bot.register_next_step_handler(msg, on_click)
    bot.register_next_step_handler(message, on_click)
    cur.close()
    conn.close()


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
    elif message.text[:12] == '/sendmailing':
        return mailing(message)
    elif message.text == 'Получить новую карту 🚗':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % message.from_user.id).fetchone()
        rolls = int(user[23])
        cards = json.loads(user[2])
        last_time = datetime.datetime(*json.loads(user[4]))
        cooldown_lvl = int(user[19])
        if rolls != 0:
            rolls -= 1
            card_num = random.choices(for_random, weights=rarities)[0]
            card = all_cards[str(card_num)]
            rarity_of_card = rarity_test[card[4]]
            with open(f'{card_num}.jpg', 'rb') as photo:
                bot.send_photo(message.chat.id, photo, f'Ты получил новую карту: {card[0]}\nГоды выпуска: {card[1]}\nСтрана: {card[2]}\nДвигатель: {card[3]}\nРедкость: {rarity_of_card[0]}\nРейтинг + {str(rarity_of_card[1])}')
            cur.execute("UPDATE users SET number_of_cards = number_of_cards + 1 WHERE id = '%i'" % message.chat.id)
            conn.commit()
            cur.execute("UPDATE users SET rating = rating + '%i' WHERE id = '%i'" % (rarity_of_card[1], message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET rolls = '%i' WHERE id = '%i'" % (rolls, message.chat.id))
            conn.commit()
            if str(card_num) in list(map(lambda x: x[0], cards.items())):
                cards[str(card_num)] += 1
            else:
                cards[str(card_num)] = 1
            cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards), message.chat.id))
            conn.commit()
        else:
            # time_for_cooldown_lvls[cooldown_lvl - 1]
            if (datetime.datetime.now() - last_time).seconds >= 0:
                card_num = random.choices(for_random, weights=rarities)[0]
                card = all_cards[str(card_num)]
                rarity_of_card = rarity_test[card[4]]
                with open(f'{card_num}.jpg', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, f'Ты получил новую карту: {card[0]}\nГоды выпуска: {card[1]}\nСтрана: {card[2]}\nДвигатель: {card[3]}\nРедкость: {rarity_of_card[0]}\nРейтинг + {str(rarity_of_card[1])}\n⏳ До следующей попытки {time_for_cooldown_lvls[cooldown_lvl - 1] // 3600} часа')
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
                bot.send_message(message.chat.id, f'До следующей попытки {time_conversion(0 - (datetime.datetime.now() - last_time).seconds)}')
    elif message.text == 'Главное меню 🏠':
        markup = types.InlineKeyboardMarkup()
        prof = types.InlineKeyboardButton('Профиль 👤', callback_data=json.dumps(['profile', '']))
        deck = types.InlineKeyboardButton('Коллекция 🗃️', callback_data=json.dumps(['deck', '']))
        duel = types.InlineKeyboardButton('Начать дуэль ⚔️', callback_data=json.dumps(['duel', '']))
        shop = types.InlineKeyboardButton('Магазин 🛍', callback_data=json.dumps(['shop', '']))
        dice = types.InlineKeyboardButton('Получить попытки 🎲', callback_data=json.dumps(['dice', '']))
        trade = types.InlineKeyboardButton('Обмен карт 🤝', callback_data=json.dumps(['trade', '']))
        mini_games = types.InlineKeyboardButton('Мини игры 🎮', callback_data=json.dumps(['games', '']))
        markup.row(prof, deck).row(duel).row(shop).row(dice).row(trade).row(mini_games)
        with open('./garage_main.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, '🤔💭 Доступные действия:', reply_markup=markup)
    cur.close()
    conn.close()
    bot.register_next_step_handler(message, on_click)


conn = sqlite3.connect('garage_data_base.sql')
cur = conn.cursor()
exist = cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''').fetchone()
if exist[0] == 1:
    ids = cur.execute('SELECT id FROM users').fetchall()
    for id in ids:
        id = id[0]
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % id).fetchone()
        cur.execute("UPDATE users SET dueling_with_id = 0 WHERE id = '%i'" % id)
        conn.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        new_card = types.KeyboardButton('Получить новую карту 🚗')
        menu = types.KeyboardButton('Главное меню 🏠')
        markup.add(new_card, menu)
        msg = bot.send_message(id, 'Бот был перезапущен', disable_notification=True, reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(id, on_click)
cur.close()
conn.close()


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
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        if user[1] == 0: bot.answer_callback_query(callback.id, 'У тебя пока нет карт')
        else:
            markup = types.InlineKeyboardMarkup()
            show_all = types.InlineKeyboardButton('🌌 Показать все карты', callback_data=json.dumps(['show', 'all', '1']))
            show_legendary = types.InlineKeyboardButton('✨ Показать легендарные карты', callback_data=json.dumps(['show', 'legendary', '5']))
            show_epic = types.InlineKeyboardButton('☄️ Показать эпические карты', callback_data=json.dumps(['show', 'epic', '4']))
            show_rare = types.InlineKeyboardButton('🌎 Показать редкие карты', callback_data=json.dumps(['show', 'rare', '3']))
            show_common = types.InlineKeyboardButton('🚀 Показать обычные карты', callback_data=json.dumps(['show', 'common', '2']))
            sell_cards = types.InlineKeyboardButton('💵 Продать карты', callback_data=json.dumps(['sell_cards', '']))
            craft = types.InlineKeyboardButton('🛠️ Крафт', callback_data=json.dumps(['craft', '']))
            markup.row(show_all).row(show_common).row(show_rare).row(show_epic).row(show_legendary).row(sell_cards).row(craft)
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            if str(user[1])[-1] != '1':
                bot.send_message(callback.message.chat.id, f'Твоя коллеция состоит из {user[1]} карт', reply_markup=markup)
            else:
                bot.send_message(callback.message.chat.id, f'Твоя коллеция состоит из {user[1]} карты', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'show':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cards = json.loads(user[2])
        markup = types.InlineKeyboardMarkup()
        items = []
        if json.loads(callback.data)[1] == 'all': items = list(map(lambda x: x[0], cards.items()))
        else:
            for i in cards.items():
                if all_cards[str(i[0])][4] == json.loads(callback.data)[1]: items.append(str(i[0]))
        text = ''
        if json.loads(callback.data)[1] == 'common': text = 'обычных'
        elif json.loads(callback.data)[1] == 'rare': text = 'редких'
        elif json.loads(callback.data)[1] == 'epic': text = 'эпических'
        elif json.loads(callback.data)[1] == 'legendary': text = 'легендарных'
        if not items: bot.answer_callback_query(callback.id, f'У тебя нет {text} карт')
        else:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            num = 0
            number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card', json.loads(callback.data)[2], 1]))
            skip_card = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card', json.loads(callback.data)[2], 5]))
            if len(items) > 5:
                markup.row(number_of_card, next_card, skip_card)
            elif len(items) > 1:
                markup.row(number_of_card, next_card)
            else:
                markup.add(number_of_card)
            with open(f'./{items[num]}.jpg', 'rb') as photo:
                bot.send_photo(callback.message.chat.id, photo, all_cards[str(items[num])][0], reply_markup=markup)
            cur.execute("UPDATE users SET num_%s = '%i' WHERE id = '%i'" % (json.loads(callback.data)[2], num, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET item_%s = '%s' WHERE id = '%i'" % (json.loads(callback.data)[2], json.dumps(items), callback.message.chat.id))
            conn.commit()
    elif json.loads(callback.data)[0] == 'move_card':
        item_num = int(json.loads(callback.data)[1])
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        items = json.loads(user[4 + item_num])
        num = int(user[9 + item_num]) + int(json.loads(callback.data)[2])
        cur.execute("UPDATE users SET num_%i = '%i' WHERE id = '%i'" % (item_num, num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card', item_num, 1]))
        previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['move_card', item_num, -1]))
        skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card', item_num, 5]))
        skip_card_b = types.InlineKeyboardButton('<<<', callback_data=json.dumps(['move_card', item_num, -5]))
        if int(json.loads(callback.data)[2]) > 0:
            if num + 1 != len(items):
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                else:
                    markup.row(previous_card, number_of_card, next_card)
            elif num - 5 >= 0:
                markup.row(skip_card_b, previous_card, number_of_card)
            else:
                markup.row(previous_card, number_of_card)
        else:
            if num != 0:
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                else:
                    markup.row(previous_card, number_of_card, next_card)
            elif num + 5 < len(items):
                markup.row(number_of_card, next_card, skip_card_f)
            else:
                markup.row(number_of_card, next_card)
        with open(f'./{items[num]}.jpg', 'rb') as photo:
            file = types.InputMedia(type='photo', media=photo, caption=all_cards[str(items[num])][0])
            bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'duel':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        if user[1] == 0: bot.answer_callback_query(callback.id, 'У тебя пока нет карт')
        elif int(user[20]) != 0: bot.answer_callback_query(callback.id, 'Ты обмениваешься картами, сейчас ты не можешь учавстовать в дуэли')
        else:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            markup = types.InlineKeyboardMarkup()
            cancel = types.InlineKeyboardButton('🚫 Отменить действие', callback_data=json.dumps(['cancel', '']))
            markup.add(cancel)
            bot.send_message(callback.message.chat.id, '🛣️ Ты зашел в режим дуэли\n\n🏁 Здесь ты можешь учасвстовать в гонках 1 на 1 с другими пользователями\n\n🏆 Победитель определяется случайно, шансы зависят от навыка вождения и от двигателя выбранного автомобиля\n\n🎭 Победивший игрок забирает карту проигравшего\n\nУдачных заездов 🍀\n\n🏎 Введи @username пользователя, с которым хочешь начать дуэль', reply_markup=markup)
            bot.clear_step_handler_by_chat_id(callback.message.chat.id)
            bot.register_next_step_handler(callback.message, duels)
    elif json.loads(callback.data)[0] == 'cancel':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.clear_step_handler_by_chat_id(callback.message.chat.id)
        bot.register_next_step_handler(callback.message, on_click)
    elif json.loads(callback.data)[0] == 'cancel_offer':
        bot.delete_message(int(json.loads(callback.data)[1]), int(json.loads(callback.data)[2]))
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.clear_step_handler_by_chat_id(callback.message.chat.id)
        bot.register_next_step_handler(callback.message, on_click)
        msg = bot.send_message(int(json.loads(callback.data)[1]), 'Отправитель отменил предложение')
        bot.clear_step_handler_by_chat_id(int(json.loads(callback.data)[1]))
        bot.register_next_step_handler(msg, on_click)
    elif json.loads(callback.data)[0] == 'accept_duel':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(int(json.loads(callback.data)[1]), f'✅ {json.loads(callback.data)[2]} принял твое предложение')
        id1 = int(json.loads(callback.data)[1])
        id2 = callback.message.chat.id
        user1 = cur.execute("SELECT * FROM users WHERE id = '%i'" % id1).fetchone()
        user2 = cur.execute("SELECT * FROM users WHERE id = '%i'" % id2).fetchone()
        bot.delete_message(int(json.loads(callback.data)[1]), int(user1[22]))
        cards = json.loads(user1[2])
        markup = types.InlineKeyboardMarkup()
        items = list(map(lambda x: x[0], cards.items()))
        num = 0
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        choose = types.InlineKeyboardButton('👉 Выбрать карту для дуэли', callback_data=json.dumps(['choose', num]))
        leave = types.InlineKeyboardButton('🚪 Выйти из дуэли', callback_data=json.dumps(['leave_duel', '']))
        next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_duel', 1]))
        skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_duel', 5]))
        if len(items) > 5:
            markup.row(number_of_card, next_card, skip_card_f)
        elif len(items) > 1:
            markup.row(number_of_card, next_card)
        else:
            markup.row(number_of_card)
        markup.row(choose)
        markup.row(leave)
        with open(f'./{items[num]}.jpg', 'rb') as photo:
            msg1 = bot.send_photo(id1, photo, f'{all_cards[items[num]][0]}\nДвигатель: {all_cards[items[num]][3]}', reply_markup=markup)
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
        next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_duel', 1]))
        skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_duel', 5]))
        if len(items) > 5:
            markup.row(number_of_card, next_card, skip_card_f)
        elif len(items) > 1:
            markup.row(number_of_card, next_card)
        else:
            markup.row(number_of_card)
        markup.row(choose).row(leave)
        with open(f'./{items[num]}.jpg', 'rb') as photo:
            msg2 = bot.send_photo(id2, photo, f'{all_cards[items[num]][0]}\nДвигатель: {all_cards[items[num]][3]}', reply_markup=markup)
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, id2))
        conn.commit()
        cur.execute("UPDATE users SET item_1 = '%s' WHERE id = '%i'" % (json.dumps(items), id2))
        conn.commit()
        cur.execute("UPDATE users SET msg_to_delete = '%i' WHERE id = '%i'" % (msg2.message_id, id2))
        conn.commit()
    elif json.loads(callback.data)[0] == 'decline':
        cur.execute("UPDATE users SET dueling_with_id = 0 WHERE id = '%i'" % callback.message.chat.id)
        conn.commit()
        cur.execute("UPDATE users SET dueling_with_id = 0 WHERE id = '%i'" % int(json.loads(callback.data)[1]))
        conn.commit()
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user2 = cur.execute("SELECT * FROM users WHERE id = '%i'" % int(json.loads(callback.data)[1])).fetchone()
        bot.delete_message(int(json.loads(callback.data)[1]), int(user2[22]))
        msg = bot.send_message(int(json.loads(callback.data)[1]), f'❌ {json.loads(callback.data)[2]} отклонил твое предложение')
        bot.clear_step_handler_by_chat_id(int(json.loads(callback.data)[1]))
        bot.register_next_step_handler(msg, on_click)
        bot.clear_step_handler_by_chat_id(callback.message.chat.id)
        bot.register_next_step_handler(callback.message, on_click)
    elif json.loads(callback.data)[0] == 'move_card_duel':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        items = json.loads(user[5])
        num = int(user[10]) + int(json.loads(callback.data)[1])
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_duel', 1]))
        previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['move_card_duel', -1]))
        skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_duel', 5]))
        skip_card_b = types.InlineKeyboardButton('<<<', callback_data=json.dumps(['move_card_duel', -5]))
        choose = types.InlineKeyboardButton('👉 Выбрать карту для дуэли', callback_data=json.dumps(['choose', num]))
        leave = types.InlineKeyboardButton('🚪 Выйти из дуэли', callback_data=json.dumps(['leave_duel', '']))
        if int(json.loads(callback.data)[1]) > 0:
            if num + 1 != len(items):
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                else:
                    markup.row(previous_card, number_of_card, next_card)
            elif num - 5 >= 0:
                markup.row(skip_card_b, previous_card, number_of_card)
            else:
                markup.row(previous_card, number_of_card)
        else:
            if num != 0:
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                else:
                    markup.row(previous_card, number_of_card, next_card)
            elif num + 5 < len(items):
                markup.row(number_of_card, next_card, skip_card_f)
            else:
                markup.row(number_of_card, next_card)
        markup.row(choose).row(leave)
        with open(f'./{items[num]}.jpg', 'rb') as photo:
            file = types.InputMedia(type='photo', media=photo, caption=f'{all_cards[items[num]][0]}\nДвигатель: {all_cards[items[num]][3]}')
            bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'choose':
        user1 = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        id2 = int(user1[20])
        user2 = cur.execute("SELECT * FROM users WHERE id = '%i'" % id2).fetchone()
        card1 = json.loads(user1[5])[int(json.loads(callback.data)[1])]
        cur.execute("UPDATE users SET dueling_with_card = '%s' WHERE id = '%i'" % (card1, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        leave = types.InlineKeyboardButton('🚪 Выйти из дуэли', callback_data=json.dumps(['leave_duel', '']))
        markup.add(leave)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        with open(f'./{card1}.jpg', 'rb') as photo:
            bot.send_photo(callback.message.chat.id, photo, f'<b>Ты выбрал</b>\n{all_cards[card1][0]}\nДвигатель: {all_cards[card1][3]}', parse_mode='html', reply_markup=markup)
        if user2[21] != '0':
            card2 = user2[21]
            with open(f'./{card2}.jpg', 'rb') as photo:
                bot.send_photo(callback.message.chat.id, photo, f'<b>Твой противник выбрал</b>\n{all_cards[card2][0]}\nДвигатель: {all_cards[card2][3]}', parse_mode='html')
            with open(f'./{card1}.jpg', 'rb') as photo:
                bot.send_photo(id2, photo, f'<b>Твой противник выбрал</b>\n{all_cards[card1][0]}\nДвигатель: {all_cards[card1][3]}', parse_mode='html')
            bot.send_message(callback.message.chat.id, 'Гонка началась')
            bot.send_message(id2, 'Гонка началась')
            power1 = all_cards[card1][5] * user1[16]
            power2 = all_cards[card2][5] * user2[16]
            chances = [50, 50]
            if power1 > power2 : chances = [100 - (power2 / power1) * 100, (power2 / power1) * 100]
            elif power1 < power2: chances = [100 - (power1 / power2) * 100, (power1 / power2) * 100]
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
            cur.execute("UPDATE users SET dueling_with_id = 0 WHERE id = '%i'" % callback.message.chat.id)
            conn.commit()
            cur.execute("UPDATE users SET dueling_with_card = '%s' WHERE id = '%i'" % ('0', callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET dueling_with_id = 0 WHERE id = '%i'" % id2)
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
        bot.delete_message(id2, int(user2[22]))
        msg = bot.send_message(id2, 'Твой оппонент вышел из дуэли')
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
        if driving_skill == 10: bot.answer_callback_query(callback.id, 'У тебя максимальный навык вождения')
        else:
            markup = types.InlineKeyboardMarkup()
            buy = types.InlineKeyboardButton('✅ Приобрести улучшение', callback_data=json.dumps(['buy_skill', '']))
            cancel = types.InlineKeyboardButton('🚫 Отменить действие', callback_data=json.dumps(['cancel', '']))
            markup.add(buy, cancel)
            bot.send_message(callback.message.chat.id, f'🆙 Улучшение навыка вождения до {driving_skill + 1} уровня за {skill_prices[driving_skill - 1]} очков влияния', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'up_time':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cooldown_level = int(user[19])
        if cooldown_level == 3: bot.answer_callback_query(callback.id, 'У тебя максимальный уровень уменьшения времени между получением новых карт')
        else:
            markup = types.InlineKeyboardMarkup()
            buy = types.InlineKeyboardButton('✅ Приобрести улучшение', callback_data=json.dumps(['buy_cooldown', '']))
            cancel = types.InlineKeyboardButton('🚫 Отменить действие', callback_data=json.dumps(['cancel', '']))
            markup.add(buy, cancel)
            bot.send_message(callback.message.chat.id, f'⏱️ Уменьшение времени между получением новых карт до {cooldown_level + 1} уровня за {cooldown_prices[cooldown_level - 1]} очков влияния', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'buy_skill':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        driving_skill = int(user[16])
        influence_points = int(user[18])
        if influence_points < skill_prices[driving_skill - 1]: bot.answer_callback_query(callback.id, f'У тебя не хватает очков влияния для покупки этого улучшения, тебе нужно ещё {skill_prices[driving_skill - 1] - influence_points}')
        else:
            influence_points -= skill_prices[driving_skill - 1]
            driving_skill += 1
            cur.execute("UPDATE users SET influence_points = '%i' WHERE id = '%i'" % (
            influence_points, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET driving_skill = '%i' WHERE id = '%i'" % (driving_skill, callback.message.chat.id))
            conn.commit()
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            bot.send_message(callback.message.chat.id, f'✅ Улучшение навыка вождения до {driving_skill} уровня успешно приобретено')
    elif json.loads(callback.data)[0] == 'buy_cooldown':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        card_cooldown_level = int(user[19])
        influence_points = int(user[18])
        if influence_points < cooldown_prices[card_cooldown_level - 1]: bot.answer_callback_query(callback.id, f'У тебя не хватает очков влияния для покупки этого улучшения, тебе нужно ещё {cooldown_prices[card_cooldown_level - 1] - influence_points}')
        else:
            influence_points -= cooldown_prices[card_cooldown_level - 1]
            card_cooldown_level += 1
            cur.execute("UPDATE users SET influence_points = '%i' WHERE id = '%i'" % (
            influence_points, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET card_cooldown_level = '%i' WHERE id = '%i'" % (
            card_cooldown_level, callback.message.chat.id))
            conn.commit()
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            bot.send_message(callback.message.chat.id, f'✅ Улучшение навыка вождения до {card_cooldown_level} уровня успешно приобретено')
    elif json.loads(callback.data)[0] == 'sell_cards':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cards = json.loads(user[2])
        markup = types.InlineKeyboardMarkup()
        items = list(map(lambda x: x[0], cards.items()))
        num = 0
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_sell', 1]))
        skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_sell', 5]))
        if len(items) > 5:
            markup.row(number_of_card, next_card, skip_card_f)
        elif len(items) > 1:
            markup.row(number_of_card, next_card)
        else:
            markup.row(number_of_card)
        if cards[items[num]] > 1:
            sell_all_but_one = types.InlineKeyboardButton('Продать все дубликаты', callback_data=json.dumps(['sell', items[num], int(cards[items[num]]) - 1]))
            sell_all = types.InlineKeyboardButton('Продать все карты', callback_data=json.dumps(['sell', items[num], cards[items[num]]]))
            markup.row(sell_all_but_one)
            markup.row(sell_all)
        else:
            sell_one = types.InlineKeyboardButton('Продать карту', callback_data=json.dumps(['sell', items[num], 1]))
            markup.row(sell_one)
        with open(f'./{items[num]}.jpg', 'rb') as photo:
            bot.send_photo(callback.message.chat.id, photo, f'{all_cards[items[num]][0]}\nКоличество: {cards[items[num]]}', reply_markup=markup)
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET item_1 = '%s' WHERE id = '%i'" % (json.dumps(items), callback.message.chat.id))
        conn.commit()
    elif json.loads(callback.data)[0] == 'move_card_sell':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        items = json.loads(user[5])
        cards = json.loads(user[2])
        num = int(user[10]) + int(json.loads(callback.data)[1])
        cur.execute("UPDATE users SET num_1 = '%i' WHERE id = '%i'" % (num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_sell', 1]))
        previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['move_card_sell', -1]))
        skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_sell', 5]))
        skip_card_b = types.InlineKeyboardButton('<<<', callback_data=json.dumps(['move_card_sell', -5]))
        if int(json.loads(callback.data)[1]) > 0:
            if num + 1 != len(items):
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                else:
                    markup.row(previous_card, number_of_card, next_card)
            elif num - 5 >= 0:
                markup.row(skip_card_b, previous_card, number_of_card)
            else:
                markup.row(previous_card, number_of_card)
        else:
            if num != 0:
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                else:
                    markup.row(previous_card, number_of_card, next_card)
            elif num + 5 < len(items):
                markup.row(number_of_card, next_card, skip_card_f)
            else:
                markup.row(number_of_card, next_card)
        if cards[items[num]] > 1:
            sell_all_but_one = types.InlineKeyboardButton('Продать все дубликаты', callback_data=json.dumps(['sell', items[num], int(cards[items[num]]) - 1]))
            sell_all = types.InlineKeyboardButton('Продать все карты', callback_data=json.dumps(['sell', items[num], cards[items[num]]]))
            markup.row(sell_all_but_one).row(sell_all)
        else:
            sell_one = types.InlineKeyboardButton('Продать карту', callback_data=json.dumps(['sell', items[num], 1]))
            markup.row(sell_one)
        with open(f'./{items[num]}.jpg', 'rb') as photo:
            file = types.InputMedia(type='photo', media=photo, caption=f'{all_cards[items[num]][0]}\nКоличество: {cards[items[num]]}')
            bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'sell':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        num = int(user[10]) - 1
        item_num = json.loads(callback.data)[1]
        cards = json.loads(user[2])
        items = list(map(lambda x: x[0], cards.items()))
        quantity = int(json.loads(callback.data)[2])
        price_of_card = cards_prices[all_cards[item_num][4]]
        if int(cards[item_num]) == quantity: del cards[item_num]
        else: cards[item_num] = 1
        cur.execute("UPDATE users SET influence_points = influence_points + '%i' WHERE id = '%i'" % (quantity * price_of_card, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET number_of_cards = number_of_cards - '%i' WHERE id = '%i'" % (quantity, callback.message.chat.id))
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
        if quantity == 1: text = 'карту'
        else: text = 'карты'
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, f'Ты продал {text} на сумму {quantity * price_of_card} очков влияния', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'dice':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        last_time_dice = datetime.datetime(*json.loads(user[24]))
        if (datetime.datetime.now() - last_time_dice).days >= 7:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            msg = bot.send_dice(callback.message.chat.id, '🎲')
            cur.execute("UPDATE users SET rolls = rolls + '%i' WHERE id = '%i'" % (msg.dice.value, callback.message.chat.id))
            conn.commit()
            now = datetime.datetime.now()
            cur.execute("UPDATE users SET last_dice = '%s' WHERE id = '%i'" % (json.dumps([now.year, now.month, now.day, now.hour, now.minute, now.second]), callback.message.chat.id))
            conn.commit()
            if msg.dice.value == 1: text = 'попытку'
            elif msg.dice.value in (2, 3, 4) : text = 'попытки'
            else: text = 'попыток'
            time.sleep(3.5)
            bot.send_message(callback.message.chat.id, f'Ты получил {msg.dice.value} {text}')
        else: bot.answer_callback_query(callback.id, 'Ты уже получал попытки на этой неделе')
    elif json.loads(callback.data)[0] == 'craft':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        craft_rolls_common = types.InlineKeyboardButton('🔄 5 попыток из 10 обычных карт', callback_data=json.dumps(['do_craft', 1]))
        craft_rolls_rare = types.InlineKeyboardButton('🔄 5 попыток из 5 редких карт', callback_data=json.dumps(['do_craft', 2]))
        craft_epic = types.InlineKeyboardButton('🟣 Эпическую карту из 5 редких', callback_data=json.dumps(['do_craft', 3]))
        craft_legendary = types.InlineKeyboardButton('🟡 Легендарную карту из 5 эпических', callback_data=json.dumps(['do_craft', 4]))
        markup.row(craft_rolls_common).row(craft_rolls_rare).row(craft_epic).row(craft_legendary)
        bot.send_message(callback.message.chat.id, '⚙️ Выбери крафт', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'do_craft':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        which = int(json.loads(callback.data)[1])
        using = int(user[24 + which])
        cards = json.loads(user[2])
        quantity = 5
        if which == 1:
            rarity = 'common'
            text = 'обычных'
            for_num = 2
            quantity = 10
        elif which == 2 or which == 3:
            rarity = 'rare'
            text = 'редких'
            for_num = 3
        else:
            rarity = 'epic'
            text = 'эпических'
            for_num = 4
        items = []
        for i in cards.items():
            if all_cards[str(i[0])][4] == rarity: items.append(str(i[0]))
        count = 0
        for i in items:
            count += int(cards[i])
        if count < quantity - using: bot.answer_callback_query(callback.id, f'У тебя недостаточно {text} карт для крафта')
        else:
            num = 0
            markup = types.InlineKeyboardMarkup()
            number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_craft', 1, for_num, which]))
            skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_craft', 5, for_num, which]))
            if len(items) > 5:
                markup.row(number_of_card, next_card, skip_card_f)
            elif len(items) > 1:
                markup.row(number_of_card, next_card)
            else:
                markup.row(number_of_card)
            if cards[items[num]] > 1:
                use_all_but_one = types.InlineKeyboardButton('Использовать все дубликаты', callback_data=json.dumps(['use_craft', items[num], int(cards[items[num]]) - 1, which]))
                use_all = types.InlineKeyboardButton('Использовать все карты',callback_data=json.dumps(['use_craft', items[num], cards[items[num]], which]))
                markup.row(use_all_but_one).row(use_all)
            else:
                use_one = types.InlineKeyboardButton('Использовать карту',callback_data=json.dumps(['use_craft', items[num], 1, which]))
                markup.row(use_one)
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            with open(f'./{items[num]}.jpg', 'rb') as photo:
                bot.send_photo(callback.message.chat.id, photo, f'{all_cards[str(items[num])][0]}\nКоличество: {cards[items[num]]}', reply_markup=markup)
            cur.execute("UPDATE users SET num_%i = '%i' WHERE id = '%i'" % (for_num, num, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET item_%i = '%s' WHERE id = '%i'" % (for_num, json.dumps(items), callback.message.chat.id))
            conn.commit()
    elif json.loads(callback.data)[0] == 'move_card_craft':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        for_num = int(json.loads(callback.data)[2])
        items = json.loads(user[4 + for_num])
        cards = json.loads(user[2])
        which = int(json.loads(callback.data)[3])
        num = int(user[9 + for_num]) + int(json.loads(callback.data)[1])
        cur.execute("UPDATE users SET num_%i = '%i' WHERE id = '%i'" % (for_num, num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_craft', 1, for_num, which]))
        previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['move_card_craft', -1, for_num, which]))
        skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_craft', 5, for_num, which]))
        skip_card_b = types.InlineKeyboardButton('<<<', callback_data=json.dumps(['move_card_craft', -5, for_num, which]))
        if int(json.loads(callback.data)[1]) > 0:
            if num + 1 != len(items):
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                else:
                    markup.row(previous_card, number_of_card, next_card)
            elif num - 5 >= 0:
                markup.row(skip_card_b, previous_card, number_of_card)
            else:
                markup.row(previous_card, number_of_card)
        else:
            if num != 0:
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                else:
                    markup.row(previous_card, number_of_card, next_card)
            elif num + 5 < len(items):
                markup.row(number_of_card, next_card, skip_card_f)
            else:
                markup.row(number_of_card, next_card)
        if cards[items[num]] > 1:
            use_all_but_one = types.InlineKeyboardButton('Использовать все дубликаты', callback_data=json.dumps(['use_craft', items[num], int(cards[items[num]]) - 1, which]))
            use_all = types.InlineKeyboardButton('Использовать все карты', callback_data=json.dumps(['use_craft', items[num], cards[items[num]], which]))
            markup.row(use_all_but_one).row(use_all)
        else:
            use_one = types.InlineKeyboardButton('Использовать карту', callback_data=json.dumps(['use_craft', items[num], 1, which]))
            markup.row(use_one)
        with open(f'./{items[num]}.jpg', 'rb') as photo:
            file = types.InputMedia(type='photo', media=photo, caption=f'{all_cards[str(items[num])][0]}\nКоличество: {cards[items[num]]}')
            bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'use_craft':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        which = int(json.loads(callback.data)[3])
        using = int(user[24 + which])
        for_craft = 5
        if which == 1:
            for_using = 'common'
            rarity = 'common'
            for_craft = 10
            for_data = 2
        elif which == 2:
            for_using = 'rare'
            rarity = 'rare'
            for_data = 3
        elif which == 3:
            for_using = 'epic'
            rarity = 'rare'
            for_data = 3
        else:
            for_using = 'legendary'
            rarity = 'epic'
            for_data = 4
        quantity = int(json.loads(callback.data)[2])
        card_num = json.loads(callback.data)[1]
        cards = json.loads(user[2])
        cards_num = cards[card_num]
        need = for_craft - using
        if quantity >= need:
            cards_num -= need
            if cards_num == 0: del cards[card_num]
            else: cards[card_num] = cards_num
            cur.execute("UPDATE users SET number_of_cards = number_of_cards - '%i' WHERE id = '%i'" % (need, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET using_for_craft_%s = 0 WHERE id = '%i'" % (for_using, callback.message.chat.id))
            conn.commit()
            if which == 1 or which == 2:
                cur.execute("UPDATE users SET rolls = rolls + 5 WHERE id = '%i'" % callback.message.chat.id)
                conn.commit()
                text = '10 обычных'
                if which == 2: text = '5 редких'
                bot.delete_message(callback.message.chat.id, callback.message.message_id)
                bot.send_message(callback.message.chat.id, f'✅ Ты скрафтил 5 попыток из {text} карт')
            else:
                if which == 3:
                    random_card = random.choice(epic_random)
                    text = 'эпическую карту из 5 редких'
                else:
                    random_card = random.choice(legendary_random)
                    text = 'легендарную карту из 5 эпических'
                try:
                    if cards[random_card]: cards[random_card] += 1
                except:
                    cards[random_card] = 1
                bot.delete_message(callback.message.chat.id, callback.message.message_id)
                with open(f'{random_card}.jpg', 'rb') as photo:
                    bot.send_photo(callback.message.chat.id, photo, f'✅ Ты скрафтил {text} карт:\n\n{all_cards[random_card][0]}\nГоды выпуска: {all_cards[random_card][1]}\nСтрана: {all_cards[random_card][2]}\nДвигатель: {all_cards[random_card][3]}')
            cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards), callback.message.chat.id))
            conn.commit()
        else:
            need -= quantity
            cards_num -= quantity
            items = json.loads(user[4 + for_data])
            num = int(user[9 + for_data])
            if cards_num == 0:
                del cards[card_num]
                items = []
                for i in cards.items():
                    if all_cards[str(i[0])][4] == rarity: items.append(str(i[0]))
                if num != 0: num -= 1
            else: cards[card_num] = cards_num
            using = for_craft - need
            cur.execute("UPDATE users SET number_of_cards = number_of_cards - '%i' WHERE id = '%i'" % (quantity, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards), callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET using_for_craft_%s = '%i' WHERE id = '%i'" % (for_using, using, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET num_%i = '%i' WHERE id = '%i'" % (for_data, num, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET item_%i = '%s' WHERE id = '%i'" % (for_data, json.dumps(items), callback.message.chat.id))
            conn.commit()
            text = 'карт'
            if need == 1: text = 'карту'
            elif need in (2, 3, 4): text = 'карты'
            markup = types.InlineKeyboardMarkup()
            number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_craft', 1, for_data, which]))
            previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps( ['move_card_craft', -1, for_data, which]))
            skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_craft', 5, for_data, which]))
            skip_card_b = types.InlineKeyboardButton('<<<', callback_data=json.dumps(['move_card_craft', -5, for_data, which]))
            if num + 1 != len(items):
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    elif num != 0:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                elif num != 0:
                    markup.row(previous_card, number_of_card, next_card)
                else:
                    markup.row(number_of_card, next_card)
            elif num - 5 >= 0:
                markup.row(skip_card_b, previous_card, number_of_card)
            elif num != 0:
                markup.row(previous_card, number_of_card)
            else:
                markup.row(number_of_card)
            if cards[items[num]] > 1:
                use_all_but_one = types.InlineKeyboardButton('Использовать все дубликаты', callback_data=json.dumps(['use_craft', items[num], int(cards[items[num]]) - 1, which]))
                use_all = types.InlineKeyboardButton('Использовать все карты', callback_data=json.dumps(['use_craft', items[num], cards[items[num]], which]))
                markup.row(use_all_but_one).row(use_all)
            else:
                use_one = types.InlineKeyboardButton('Использовать карту', callback_data=json.dumps(['use_craft', items[num], 1, which]))
                markup.row(use_one)
            with open(f'./{items[num]}.jpg', 'rb') as photo:
                file = types.InputMedia(type='photo', media=photo, caption=f'{all_cards[str(items[num])][0]}\nКоличество: {cards[items[num]]}')
                bot.answer_callback_query(callback.id, f'Тебе осталось выбрать {need} {text}')
                bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'trade':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        if user[1] == 0: bot.answer_callback_query(callback.id, 'У тебя пока нет карт')
        elif int(user[20]) != 0: bot.answer_callback_query(callback.id, 'Ты уже обмениваешься картами')
        else:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            markup = types.InlineKeyboardMarkup()
            epic_epic = types.InlineKeyboardButton('Эпическую карту на эпическую карту', callback_data=json.dumps(['trade_request', 'epic']))
            legendary_legendary = types.InlineKeyboardButton('Легендарную карту на легендарную карту', callback_data=json.dumps(['trade_request', 'legendary']))
            cancel = types.InlineKeyboardButton('🚫 Отменить действие', callback_data=json.dumps(['cancel', '']))
            markup.row(epic_epic).row(legendary_legendary).row(cancel)
            bot.send_message(callback.message.chat.id, '💱 Ты зашел в трейды\n\n♻️ Здесь ты можешь обмениваться картами с другими пользователями\n\n⚖️ Обменивать можно только эпические и легендарныые карты\n\n👀 Выбери вариант обмена', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'trade_request':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        cards = json.loads(user[2])
        rarity = json.loads(callback.data)[1]
        items = []
        for i in cards.items():
            if all_cards[str(i[0])][4] == rarity: items.append(str(i[0]))
        text = 'эпических'
        which = 4
        if rarity == 'legendary':
            text = 'легендарных'
            which = 5
        if not items: bot.answer_callback_query(callback.id, f'У тебя нет {text} карт для трейда')
        else:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            num = 0
            markup = types.InlineKeyboardMarkup()
            number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
            next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_trade', 1, which, rarity, '1']))
            skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_trade', 5, which, rarity, '1']))
            if len(items) > 5:
                markup.row(number_of_card, next_card, skip_card_f)
            elif len(items) > 1:
                markup.row(number_of_card, next_card)
            else:
                markup.row(number_of_card)
            use = types.InlineKeyboardButton('Использовать карту', callback_data=json.dumps(['use_trade', items[num], '1', rarity]))
            markup.row(use)
            with open(f'./{items[num]}.jpg', 'rb') as photo:
                bot.send_photo(callback.message.chat.id, photo, f'{all_cards[str(items[num])][0]}', reply_markup=markup)
            cur.execute("UPDATE users SET num_%i = '%i' WHERE id = '%i'" % (which, num, callback.message.chat.id))
            conn.commit()
            cur.execute("UPDATE users SET item_%i = '%s' WHERE id = '%i'" % (which, json.dumps(items), callback.message.chat.id))
            conn.commit()
    elif json.loads(callback.data)[0] == 'move_card_trade':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        which = int(json.loads(callback.data)[2])
        rarity = json.loads(callback.data)[3]
        who = json.loads(callback.data)[4]
        items = json.loads(user[4 + which])
        num = int(user[9 + which]) + int(json.loads(callback.data)[1])
        cur.execute("UPDATE users SET num_%i = '%i' WHERE id = '%i'" % (which, num, callback.message.chat.id))
        conn.commit()
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_trade', 1, which, rarity, who]))
        previous_card = types.InlineKeyboardButton('<', callback_data=json.dumps(['move_card_trade', -1, which, rarity, who]))
        skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_trade', 5, which, rarity, who]))
        skip_card_b = types.InlineKeyboardButton('<<<', callback_data=json.dumps(['move_card_trade', -5, which, rarity, who]))
        if int(json.loads(callback.data)[1]) > 0:
            if num + 1 != len(items):
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                else:
                    markup.row(previous_card, number_of_card, next_card)
            elif num - 5 >= 0:
                markup.row(skip_card_b, previous_card, number_of_card)
            else:
                markup.row(previous_card, number_of_card)
        else:
            if num != 0:
                if num + 5 < len(items):
                    if num - 5 >= 0:
                        markup.row(skip_card_b, previous_card, number_of_card, next_card, skip_card_f)
                    else:
                        markup.row(previous_card, number_of_card, next_card, skip_card_f)
                elif num - 5 >= 0:
                    markup.row(skip_card_b, previous_card, number_of_card, next_card)
                else:
                    markup.row(previous_card, number_of_card, next_card)
            elif num + 5 < len(items):
                markup.row(number_of_card, next_card, skip_card_f)
            else:
                markup.row(number_of_card, next_card)
        use = types.InlineKeyboardButton('Использовать карту', callback_data=json.dumps(['use_trade', items[num], who, rarity]))
        markup.row(use)
        with open(f'./{items[num]}.jpg', 'rb') as photo:
            file = types.InputMedia(type='photo', media=photo, caption=all_cards[str(items[num])][0])
            bot.edit_message_media(file, callback.message.chat.id, callback.message.message_id, reply_markup=markup)
    elif json.loads(callback.data)[0] == 'use_trade':
        user1 = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        user2 = cur.execute("SELECT * FROM users WHERE id = '%i'" % int(user1[20])).fetchone()
        card_num = json.loads(callback.data)[1]
        who = json.loads(callback.data)[2]
        cur.execute("UPDATE users SET using_for_trade = '%s' WHERE id = '%i'" % (card_num, callback.message.chat.id))
        conn.commit()
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        if who == '1':
            bot.send_message(callback.message.chat.id, '🔄 Введи @username пользователя, которому хочешь предложить обмен')
            bot.clear_step_handler_by_chat_id(callback.message.chat.id)
            bot.register_next_step_handler(callback.message, trade)
        else:
            bot.answer_callback_query(callback.id, 'Пользователь получил предложение')
            bot.register_next_step_handler(callback.message, on_click)
            markup = types.InlineKeyboardMarkup()
            accept = types.InlineKeyboardButton('✅ Принять', callback_data=json.dumps(['end_trade', callback.message.chat.id]))
            decline = types.InlineKeyboardButton('❌ Отклонить', callback_data=json.dumps(['decline_trade', callback.message.from_user.id, user2[15]]))
            markup.row(accept).row(decline)
            with open(f'{json.loads(callback.data)[1]}.jpg', 'rb') as photo:
                bot.send_photo(int(user1[20]), photo, f'Пользователь {callback.message.from_user.username} предлагает\n{all_cards[json.loads(callback.data)[1]][0]}', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'accept_trade':
        bot.send_message(int(json.loads(callback.data)[1]), f'✅ {json.loads(callback.data)[2]} принял предложение на обмен')
        user1 = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        user2 = cur.execute("SELECT * FROM users WHERE id = '%i'" % int(json.loads(callback.data)[1])).fetchone()
        rarity = json.loads(callback.data)[3]
        which = 4
        if rarity == 'legendary': which = 5
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.delete_message(int(json.loads(callback.data)[1]), int(user2[22]))
        cur.execute("UPDATE users SET dueling_with_id = '%i' WHERE id = '%i'" % (int(user1[0]), int(user2[0])))
        conn.commit()
        cur.execute("UPDATE users SET dueling_with_id = '%i' WHERE id = '%i'" % (int(user2[0]), int(user1[0])))
        conn.commit()
        bot.clear_step_handler_by_chat_id(callback.message.chat.id)
        bot.clear_step_handler_by_chat_id(int(json.loads(callback.data)[1]))
        cards = json.loads(user1[2])
        items = []
        for i in cards.items():
            if all_cards[str(i[0])][4] == rarity: items.append(str(i[0]))
        items.remove(user2[29])
        num = 0
        markup = types.InlineKeyboardMarkup()
        number_of_card = types.InlineKeyboardButton(f'{num + 1} / {len(items)}', callback_data=json.dumps(['nothing', '']))
        next_card = types.InlineKeyboardButton('>', callback_data=json.dumps(['move_card_trade', 1, which, rarity, '2']))
        skip_card_f = types.InlineKeyboardButton('>>>', callback_data=json.dumps(['move_card_trade', 5, which, rarity, '2']))
        if len(items) > 5:
            markup.row(number_of_card, next_card, skip_card_f)
        elif len(items) > 1:
            markup.row(number_of_card, next_card)
        else:
            markup.row(number_of_card)
        use = types.InlineKeyboardButton('Использовать карту', callback_data=json.dumps(['use_trade', items[num], '2', rarity]))
        markup.row(use)
        with open(f'./{items[num]}.jpg', 'rb') as photo:
            bot.send_photo(callback.message.chat.id, photo, f'{all_cards[str(items[num])][0]}', reply_markup=markup)
        cur.execute("UPDATE users SET num_%i = '%i' WHERE id = '%i'" % (which, num, callback.message.chat.id))
        conn.commit()
        cur.execute("UPDATE users SET item_%i = '%s' WHERE id = '%i'" % (which, json.dumps(items), callback.message.chat.id))
        conn.commit()
    elif json.loads(callback.data)[0] == 'end_trade':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user1 = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        user2 = cur.execute("SELECT * FROM users WHERE id = '%i'" % int(json.loads(callback.data)[1])).fetchone()
        cards1 = json.loads(user1[2])
        cards2 = json.loads(user2[2])
        card1 = user1[29]
        card2 = user2[29]
        if card2 in cards1:
            cards1[card2] += 1
        else:
            cards1[card2] = 1
        if card1 in cards2:
            cards2[card1] += 1
        else:
            cards2[card1] = 1
        if cards1[card1] == 1:
            del cards1[card1]
        else:
            cards1[card1] -= 1
        if cards2[card2] == 1:
            del cards2[card2]
        else:
            cards2[card2] -= 1
        cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards1), int(user1[0])))
        conn.commit()
        cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards2), int(user2[0])))
        conn.commit()
        bot.send_message(int(user1[0]), 'Обмен прошел успешно')
        bot.send_message(int(user2[0]), 'Обмен прошел успешно')
        bot.register_next_step_handler(callback.message, on_click)
    elif json.loads(callback.data)[0] == 'games':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        markup = types.InlineKeyboardMarkup()
        slots = types.InlineKeyboardButton('Слоты 🎰', callback_data=json.dumps(['slots', '']))
        field = types.InlineKeyboardButton('Минное поле 🔢', callback_data=json.dumps(['field', '']))
        markup.row(slots).row(field)
        bot.send_message(callback.message.chat.id, '🕹️ Выбери игру:', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'slots':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        markup = types.InlineKeyboardMarkup()
        play = types.InlineKeyboardButton('Играть 🃏', callback_data=json.dumps(['play_slots', '']))
        get_details = types.InlineKeyboardButton('Пополнить баланс деталей ⚙️', callback_data=json.dumps(['details', '']))
        markup.row(play).row(get_details)
        bot.send_message(callback.message.chat.id, f'🎰 Запусти слоты, если автомаст выдаст три одинаковых слота, ты выиграешь 10 попыток\n\n⚙️ Стоимость одной игры 49 деталей\n\nУ тебя {user[30]} деталей и {user[31]} бесплатных прокруток', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'play_slots':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        details = int(user[30])
        if details < 49: bot.answer_callback_query(callback.id, 'У тебя недостаточно деталей для игры')
        else:
            cur.execute("UPDATE users SET details = details - 49 WHERE id = '%i'" % int(user[0]))
            conn.commit()
            msg = bot.send_dice(callback.message.chat.id, '🎰')
            markup = types.InlineKeyboardMarkup()
            play = types.InlineKeyboardButton('Играть 🃏', callback_data=json.dumps(['play_slots', '']))
            get_details = types.InlineKeyboardButton('Пополнить баланс деталей ⚙️', callback_data=json.dumps(['details', '']))
            markup.row(play).row(get_details)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f'🎰 Запусти слоты, если автомаст выдаст три одинаковых слота, ты выиграешь 10 попыток\n\n⚙️ Стоимость одной игры 49 деталей\n\nУ тебя {details - 49} деталей и {user[31]} бесплатных прокруток', reply_markup=markup)
            time.sleep(2.25)
            if msg.dice.value in (1, 22, 43, 64):
                bot.send_message(callback.message.chat.id, 'Ты получил 10 попыток!')
                cur.execute("UPDATE users SET rolls = rolls + 10 WHERE id = '%i'" % int(user[0]))
                conn.commit()
            else: bot.send_message(callback.message.chat.id, 'Три одинаковых слота не выпало, повезет в следующий раз!')
    elif json.loads(callback.data)[0] == 'field':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        markup = types.InlineKeyboardMarkup()
        play = types.InlineKeyboardButton('Играть 💣', callback_data=json.dumps(['play_field', '']))
        get_details = types.InlineKeyboardButton('Пополнить баланс деталей ⚙️', callback_data=json.dumps(['details', '']))
        markup.row(play).row(get_details)
        bot.send_message(callback.message.chat.id, f'🔢 Это минное поле, здесь ты можешь получить специальные карты, всего две карты на 9 полей\n\n⚙️ Стоимость одной игры 79 деталей\n\nУ тебя {user[30]} деталей и {user[31]} бесплатных попыток', reply_markup=markup)
    elif json.loads(callback.data)[0] == 'play_field':
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        details = int(user[30])
        if details < 79: bot.answer_callback_query(callback.id, 'У тебя недостаточно деталей для игры')
        else:
            cur.execute("UPDATE users SET details = details - 79 WHERE id = '%i'" % int(user[0]))
            conn.commit()
            markup = types.InlineKeyboardMarkup()
            play = types.InlineKeyboardButton('Играть 💣', callback_data=json.dumps(['play_field', '']))
            get_details = types.InlineKeyboardButton('Пополнить баланс деталей ⚙️', callback_data=json.dumps(['details', '']))
            markup.row(play).row(get_details)
            bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f'🔢 Это минное поле, здесь ты можешь получить специальные карты, всего две карты на 9 полей\n\n⚙️ Стоимость одной игры 79 деталей\n\nУ тебя {details - 79} деталей и {user[31]} бесплатных попыток', reply_markup=markup)
            field_markup = types.InlineKeyboardMarkup()
            spot1 = types.InlineKeyboardButton('❓', callback_data=json.dumps(['field_card', '']))
            spot2 = types.InlineKeyboardButton('❓', callback_data=json.dumps(['field_card', '']))
            spot3 = types.InlineKeyboardButton('❓', callback_data=json.dumps(['field_none', '']))
            spot4 = types.InlineKeyboardButton('❓', callback_data=json.dumps(['field_none', '']))
            spot5 = types.InlineKeyboardButton('❓', callback_data=json.dumps(['field_none', '']))
            spot6 = types.InlineKeyboardButton('❓', callback_data=json.dumps(['field_none', '']))
            spot7 = types.InlineKeyboardButton('❓', callback_data=json.dumps(['field_none', '']))
            spot8 = types.InlineKeyboardButton('❓', callback_data=json.dumps(['field_none', '']))
            spot9 = types.InlineKeyboardButton('❓', callback_data=json.dumps(['field_none', '']))
            spots = [spot1, spot2, spot3, spot4, spot5, spot6, spot7, spot8, spot9]
            random.shuffle(spots)
            field_markup.row(spots[0], spots[1], spots[2]).row(spots[3], spots[4], spots[5]).row(spots[6], spots[7], spots[8])
            bot.send_message(callback.message.chat.id, '🤔 Выбери поле', reply_markup=field_markup)
    elif json.loads(callback.data)[0] == 'field_card':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        user = cur.execute("SELECT * FROM users WHERE id = '%i'" % callback.message.chat.id).fetchone()
        card = random.choices(specials, k=1)[0]
        cards = json.loads(user[2])
        if card in cards: cards[card] += 1
        else: cards[card] = 1
        cur.execute("UPDATE users SET cards = '%s' WHERE id = '%i'" % (json.dumps(cards), int(user[0])))
        conn.commit()
        cur.execute("UPDATE users SET rating = rating + 1 WHERE id = '%i'" % int(user[0]))
        conn.commit()
        cur.execute("UPDATE users SET number_of_cards = number_of_cards + 1 WHERE id = '%i'" % int(user[0]))
        conn.commit()
        with open(f'./{card}.jpg', 'rb') as photo:
            bot.send_photo(callback.message.chat.id, photo, f'Ты получил особую карту!:\n{all_cards[card][0]}\nГоды выпуска: {all_cards[card][1]}\nСтрана: {all_cards[card][2]}\nДвигатель: {all_cards[card][3]}\nРейтинг: 5000')
    elif json.loads(callback.data)[0] == 'field_none':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Ты выбрал поле без карты')
    cur.close()
    conn.close()


def duels(message):
    conn = sqlite3.connect('garage_data_base.sql')
    cur = conn.cursor()
    user1 = cur.execute("SELECT * FROM users WHERE id = '%i'" % message.chat.id).fetchone()
    bot.delete_message(message.chat.id, message.message_id - 1)
    if message.text[0] == '@':
        if user1[15] == message.text:
            bot.send_message(message.chat.id, 'Ты не можешь провести дуэль с самим собой 😐')
            bot.register_next_step_handler(message, on_click)
        elif cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username = '%s')" % message.text).fetchone()[0]:
            user2 = cur.execute("SELECT * FROM users WHERE username = '%s'" % message.text).fetchone()
            if int(user2[1]) == 0:
                bot.send_message(message.chat.id, 'У этого пользователя ещё нет карт')
                bot.register_next_step_handler(message, on_click)
            elif int(user2[20]) != 0:
                bot.send_message(message.chat.id, 'Этот пользователь сейчас находится в дуэли либо обменивается картами')
                bot.register_next_step_handler(message, on_click)
            else:
                cur.execute("UPDATE users SET dueling_with_id = '%i' WHERE id = '%i'" % (int(user1[0]), int(user2[0])))
                conn.commit()
                cur.execute("UPDATE users SET dueling_with_id = '%i' WHERE id = '%i'" % (int(user2[0]), int(user1[0])))
                conn.commit()
                ida = int(user2[0])
                markup = types.InlineKeyboardMarkup()
                accept = types.InlineKeyboardButton('✅ Принять', callback_data=json.dumps(['accept_duel', message.from_user.id, message.text]))
                decline = types.InlineKeyboardButton('❌ Отклонить', callback_data=json.dumps(['decline', message.from_user.id, message.text]))
                markup.row(accept, decline)
                bot.send_message(ida, f'❗️ Пользователь {message.from_user.username} предложил вам провести дуэль', reply_markup=markup)
                bot.clear_step_handler_by_chat_id(ida)
                markup = types.InlineKeyboardMarkup()
                cancel_offer = types.InlineKeyboardButton('🚫 Отменить предложение', callback_data=json.dumps(['cancel_offer', ida]))
                markup.add(cancel_offer)
                msg = bot.send_message(message.chat.id, 'Предложение успешно отправлено', reply_markup=markup)
                cur.execute("UPDATE users SET msg_to_delete = '%i' WHERE id = '%i'" % (msg.message_id, message.from_user.id))
                conn.commit()
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


def trade(message):
    conn = sqlite3.connect('garage_data_base.sql')
    cur = conn.cursor()
    user1 = cur.execute("SELECT * FROM users WHERE id = '%i'" % message.chat.id).fetchone()
    if message.text[0] == '@':
        if user1[15] == message.text:
            bot.send_message(message.chat.id, 'Ты не можешь обменяться картами с самим собой 😐')
            bot.register_next_step_handler(message, on_click)
        elif cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username = '%s')" % message.text).fetchone()[0]:
            user2 = cur.execute("SELECT * FROM users WHERE username = '%s'" % message.text).fetchone()
            if int(user2[1]) == 0:
                bot.send_message(message.chat.id, 'У этого пользователя ещё нет карт')
                bot.register_next_step_handler(message, on_click)
            else:
                cards = json.loads(user2[2])
                items = []
                rarity = all_cards[user1[29]][4]
                text = 'эпических'
                if rarity == 'legendary': text = 'легендарных'
                for i in cards.items():
                    if all_cards[str(i[0])][4] == rarity: items.append(str(i[0]))
                items.remove(user1[29])
                if int(user2[20]) != 0:
                    bot.send_message(message.chat.id, 'Этот пользователь сейчас находится в дуэли или обменивается картами')
                    bot.register_next_step_handler(message, on_click)
                elif not items:
                    bot.send_message(message.chat.id, f'У этого пользователя ещё нет {text} карт, или у него есть только такая же карта')
                    bot.register_next_step_handler(message, on_click)
                else:
                    card = all_cards[user1[29]]
                    ida = int(user2[0])
                    markup = types.InlineKeyboardMarkup()
                    accept = types.InlineKeyboardButton('✅ Принять', callback_data=json.dumps(['accept_trade', message.from_user.id, message.text, rarity]))
                    decline = types.InlineKeyboardButton('❌ Отклонить', callback_data=json.dumps(['decline', message.from_user.id, message.text]))
                    cur.execute("UPDATE users SET msg_to_delete = '%i' WHERE id = '%i'" % (message.message_id, message.from_user.id))
                    conn.commit()
                    markup.row(accept, decline)
                    with open(f'{user1[29]}.jpg', 'rb') as photo:
                        msg = bot.send_photo(ida, photo, f'❗️ Пользователь {message.from_user.username} предложил вам обменять эпическую карту на эпическую карту\n\nПредлагаемая карта: {card[0]}', reply_markup=markup)
                    markup = types.InlineKeyboardMarkup()
                    cancel_offer = types.InlineKeyboardButton('🚫 Отменить предложение', callback_data=json.dumps(['cancel_offer', ida, msg.message_id]))
                    markup.add(cancel_offer)
                    msg = bot.send_message(message.chat.id, 'Предложение успешно отправлено', reply_markup=markup)
                    cur.execute("UPDATE users SET msg_to_delete = '%i' WHERE id = '%i'" % (msg.message_id, message.from_user.id))
                    conn.commit()
                    bot.register_next_step_handler(message, on_click)
        else:
            bot.send_message(message.chat.id, 'Пользователь с таким @username ещё ни разу не запускал эту игру(')
            bot.register_next_step_handler(message, on_click)
    else:
        markup = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton('🚫 Отменить действие', callback_data=json.dumps(['cancel', '']))
        markup.add(cancel)
        bot.send_message(message.chat.id, 'Ты ввёл @username неправильно, попробуй ещё раз, возможно ты забыл знак @', reply_markup=markup)
        bot.register_next_step_handler(message, trade)
    cur.close()
    conn.close()


@bot.message_handler(commands=['sendmailing'])
def mailing(message):
    conn = sqlite3.connect('garage_data_base.sql')
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    ids = cur.execute('SELECT id FROM users').fetchall()
    text = message.text[13:]
    for id in ids:
        bot.send_message(id, text)
    bot.register_next_step_handler(message, on_click)
    cur.close()
    conn.close()


bot.polling(none_stop=True)
