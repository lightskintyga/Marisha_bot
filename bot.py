import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import state

TOKEN = None

with open('token.txt') as file:
    TOKEN = file.read().strip()
    file.close()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

connect = sqlite3.connect('data.db')
cursor = connect.cursor()

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    cursor.execute("""CREATE TABLE IF NOT EXISTS data(
        id INTEGER,
        checker INTEGER,
        correct_answers INTEGER,
        written_attempts INTEGER,
        electronics_count INTEGER,
        viewing_blocks INTEGER,
        viewing_ivt_block INTEGER,
        viewing_applied_inf_block INTEGER,
        viewing_software_engineering_block INTEGER,
        viewing_information_security_block INTEGER,
        viewing_electronics_block INTEGER,
        viewing_management_block INTEGER,
        viewing_production_technology_block INTEGER,
        viewing_communication_systems_block INTEGER,
        viewing_construction_block INTEGER,
        viewing_radio_block INTEGER,
        quiz_ivt_block INTEGER,
        quiz_applied_inf_block INTEGER,
        quiz_software_engineering_block INTEGER,
        quiz_information_security_block INTEGER,
        quiz_electronics_block INTEGER,
        quiz_management_block INTEGER,
        quiz_production_technology_block INTEGER,
        quiz_communication_systems_block INTEGER,
        quiz_construction_block INTEGER,
        quiz_radio_block INTEGER,
        quiz_ivt_block_next_task INTEGER,
        quiz_applied_inf_block_next_task INTEGER,
        quiz_software_engineering_block_next_task INTEGER,
        quiz_information_security_block_next_task INTEGER,
        quiz_electronics_block_next_task INTEGER,
        quiz_management_block_next_task INTEGER,
        quiz_production_technology_block_next_task INTEGER
    )""")

    connect.commit()

    people_id = msg.chat.id
    cursor.execute(f"SELECT id FROM data WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        values = [msg.chat.id, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0]
        cursor.execute("INSERT INTO data VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                       "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", values)
        connect.commit()

        mess = 'Привет, <b>{} {}</b>! Ты уже окончил школу или совсем скоро окончишь. ' \
               'Перед тобой появится сложный выбор – "Куда поступить?". ' \
               'Мы можем помочь тебе с этим и расскажем об ИРИТ-РТФ!'.format(msg.from_user.first_name,
                                                                             msg.from_user.last_name)
        await msg.answer_photo(open('pictures/logo/entrant_irit-rtf.jpg', 'rb'), caption=mess, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Поехали 🚀')
        keyboard.add(button)

        await msg.answer('Нажми "Поехали 🚀", чтобы начать путешествие по ИРИТ-РТФ!', reply_markup=keyboard)
    else:
        await msg.answer('Ты уже пользовался ботом. К сожалению, начать прохождение квеста заново нельзя.')


@dp.message_handler(commands=['points'])
async def actual_points(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
    correct_answers = cursor.fetchone()[0]
    mess = 'Количество баллов на данный момент: <b>{}</b>'.format(correct_answers)
    await msg.answer(mess, parse_mode='html')


@dp.message_handler(lambda msg: msg.text == 'Поехали 🚀')
async def block_2(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 0:
        cursor.execute(f"UPDATE data SET checker = 1 WHERE id = {people_id}")
        connect.commit()
        mess_1 = 'Привет, я Мариша! Я буду сопровождать тебя всю нашу экскурсию по ИРИТ-РТФ и расскажу тебе обо всем.'
        await msg.answer_photo(open('pictures/marisha/render_1.2.png', 'rb'),
                               caption=mess_1,
                               reply_markup=types.ReplyKeyboardRemove())

        mess_2 = 'Для начала тебе предстоит узнать об институте из вступительного ролика. ' \
                 'В этом нам поможет директор института – <b>Обабков Илья Николаевич</b>.'
        keyboard_1 = types.InlineKeyboardMarkup()
        button_1_1 = types.InlineKeyboardButton(text='Ссылка на ролик', url='https://vk.com/video-165382372_456239062')
        keyboard_1.add(button_1_1)
        await msg.answer(mess_2, reply_markup=keyboard_1, parse_mode='html')

        keyboard_2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button_2_1 = types.KeyboardButton('✅')
        keyboard_2.add(button_2_1)

        await msg.answer('Нажми "✅", если ты посмотрел видео и готов ответить на первый вопрос!',
                         reply_markup=keyboard_2)


@dp.message_handler(lambda msg: msg.text == '✅')
async def block_3(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 1:
        cursor.execute(f"UPDATE data SET checker = 2 WHERE id = {people_id}")
        connect.commit()
        mess = 'Ооокей, теперь Вы немного знаете об ИРИТ-РТФ.\n' \
               'Но как же звучит один из его лозунгов, о котором рассказывается в видео?\n\nНапиши его!'
        await msg.answer(mess, reply_markup=types.ReplyKeyboardRemove())

        @dp.message_handler(lambda msg: msg.text == 'здесь ты выбираешь сам' or msg.text == 'здесь ты выбираешь сам!'
                                        or msg.text == 'здесь ты выбираешь сам.' or msg.text == 'Здесь ты выбираешь сам'
                                        or msg.text == 'Здесь ты выбираешь сам!' or msg.text == 'Здесь ты выбираешь сам.')
        async def block_4(msg: types.Message):
            people_id = msg.chat.id
            cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
            checker = cursor.fetchone()[0]
            if checker == 2:
                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET checker = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
                correct_answers = cursor.fetchone()[0]
                mess = 'Поздравляю, ты ответил верно! Количество очков на данный момент: <b>{}</b>\n\nКстати, ' \
                       'используя команду /points, ты всегда можешь узнать текущее количество баллов!' \
                    .format(correct_answers)
                await msg.answer(mess, parse_mode='html')

                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button = types.KeyboardButton('Далее')
                keyboard.add(button)

                await msg.answer('Нажми "Далее", чтобы продолжить наше путешествие 🌠', reply_markup=keyboard)


        @dp.message_handler(lambda msg: msg.text != 'здесь ты выбираешь сам' and msg.text != 'здесь ты выбираешь сам!'
                                        and msg.text != 'здесь ты выбираешь сам.' and msg.text != 'Здесь ты выбираешь сам'
                                        and msg.text != 'Здесь ты выбираешь сам!' and msg.text != 'Здесь ты выбираешь сам.')
        async def block_4_wrong(msg: types.Message):
            people_id = msg.chat.id
            cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
            checker = cursor.fetchone()[0]

            cursor.execute(f"SELECT written_attempts FROM data WHERE id = {people_id}")
            written_attempts = cursor.fetchone()[0]
            if checker == 2 and written_attempts == 3:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                await msg.answer('Неправильный ответ, попробуй ещё раз! У тебя осталось <b>2</b> попытки.',
                                 parse_mode='html')
            elif checker == 2 and written_attempts == 2:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 2 WHERE id = {people_id}")
                connect.commit()
                await msg.answer('Неправильный ответ. Хорошо обдумай следующий вариант, '
                                 'ведь у тебя осталась <b>последняя</b> попытка!',
                                 parse_mode='html')
            elif checker == 2 and written_attempts == 0:
                cursor.execute(f"UPDATE data SET checker = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                await msg.answer('К сожалению, попытки закончились. Правильный ответ: '
                                 '<b>здесь ты выбираешь сам</b>.', parse_mode='html')
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button = types.KeyboardButton('Далее')
                keyboard.add(button)

                await msg.answer('Нажми "Далее", чтобы продолжить наше путешествие 🌠', reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Далее')
async def block_5(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 3:
        cursor.execute(f"UPDATE data SET checker = 4 WHERE id = {people_id}")
        connect.commit()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Что это ¿ ?')
        keyboard.add(button)
        await msg.answer_photo(open('pictures/info/iot.png', 'rb'), reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Что это ¿ ?')
async def block_6(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 4:
        cursor.execute(f"UPDATE data SET checker = 5 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/iot_2.png', 'rb'), reply_markup=types.ReplyKeyboardRemove())

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Продолжить')
        keyboard.add(button)
        await msg.answer('Время двигаться дальше! Нажми "Продолжить".', reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Продолжить')
async def block_7(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 5:
        cursor.execute(f"UPDATE data SET checker = 6 WHERE id = {people_id}")
        connect.commit()
        mess = 'Ладно, ладно. ИОТ — это круто.\n\nНо иногда после сдачи лабораторной работы по физике или рефакторинга ' \
               'кода хочется отдохнуть и поиграть в компьютерные игры.\n\nИ тут ИРИТ-РТФ тоже может тебе помочь!'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Как же?')
        keyboard.add(button)
        await msg.answer_photo(open('pictures/cybersport/win.png', 'rb'), caption=mess, reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Как же?')
async def block_8(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 6:
        cursor.execute(f"UPDATE data SET checker = 7 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/tournaments.png', 'rb'), reply_markup=types.ReplyKeyboardRemove())

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Где же?')
        keyboard.add(button)
        await msg.answer('Где же узнавать о всех событиях, которые проходят в институте?', reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Где же?')
async def block_9(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 7:
        cursor.execute(f"UPDATE data SET checker = 8 WHERE id = {people_id}")
        connect.commit()
        mess = "<a href='https://t.me/Iritatoday'>Telegram-канал</a> о " \
               "самых актуальных новостях Института радиоэлектроники и " \
               "информационных технологий. ИРИТ-РТФ УрФУ."
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Продолжим')
        keyboard.add(button)
        await msg.answer_photo(open('pictures/logo/news.png', 'rb'),
                               caption=mess,
                               reply_markup=keyboard, parse_mode='html')


@dp.message_handler(lambda msg: msg.text == 'Продолжим')
async def block_10(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 8:
        cursor.execute(f"UPDATE data SET checker = 9 WHERE id = {people_id}")
        connect.commit()
        mess = "Вернемся к любимой учёбе!\n\nПорой перед выбором института, хочется узнать о тех, кто его " \
               "закончил.\nОб этом тебе расскажут выпускники ИРИТ-РТФ в кратком <a href=" \
               "'https://vk.com/video/@iritrtf_urfu?z=video-165382372_456239060%2Fclub165382372%2Fpl_-165382372_-2'>" \
               "видео-ролике</a>" \
               "\nПодробнее можешь прочитать <a href='https://priem-rtf.urfu.ru/index.php?id=26065'>тут</a>"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('А что там с деньгами?')
        keyboard.add(button)
        await msg.answer_photo(open('pictures/logo/urfu.png', 'rb'),
                               caption=mess,
                               reply_markup=keyboard,
                               parse_mode='html')


@dp.message_handler(lambda msg: msg.text == 'А что там с деньгами?')
async def block_11(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 9:
        cursor.execute(f"UPDATE data SET checker = 10 WHERE id = {people_id}")
        connect.commit()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Что еще?')
        keyboard.add(button)
        await msg.answer_photo(open('pictures/info/money.png', 'rb'), reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Что еще?')
async def block_12(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 10:
        cursor.execute(f"UPDATE data SET checker = 11 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/money_pro.png', 'rb'), reply_markup=types.ReplyKeyboardRemove())

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Узнать')
        keyboard.add(button)
        await msg.answer('А если ты еще не определился с выбором направления? '
                         'Как быть?\nМы тебе поможем!\n\nУзнать о направлениях ИРИТ-РТФ', reply_markup=keyboard)


async def list_of_destinations(msg):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton('ИВТ 🖥️')
    button_2 = types.KeyboardButton('Прикладная информатика 💻')
    button_3 = types.KeyboardButton('Программная инженерия 💻')
    button_4 = types.KeyboardButton('Информационная безопасность 🔒')
    button_5 = types.KeyboardButton('Электроника, радиотехника и системы связи 📡')
    button_6 = types.KeyboardButton('Управление в технических системах 📟')
    button_7 = types.KeyboardButton('Технология полиграфического и упаковочного производства 📄')
    keyboard.row(button_1, button_2)
    keyboard.row(button_3, button_4)
    keyboard.row(button_5, button_6)
    keyboard.row(button_7)
    await msg.answer('Выбери направление:', reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Узнать')
async def block_13(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]
    if checker == 11:
        cursor.execute(f"UPDATE data SET checker = 12 WHERE id = {people_id}")
        connect.commit()
        await list_of_destinations(msg)


@dp.message_handler(lambda msg: msg.text == 'Назад')
async def calling_list_of_destinations(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_blocks FROM data WHERE id = {people_id}")
    viewing_blocks = cursor.fetchone()[0]

    if checker == 12 and viewing_blocks != 7:
        await list_of_destinations(msg)
    elif checker == 12 and viewing_blocks == 7:
        cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
        correct_answers = cursor.fetchone()[0]

        await msg.answer('Поздравляем, абитуриент, ты успешно справился с нашим небольшим квестом! '
                         '\n\nНадеемся, что мы помогли тебе определиться с выбором направления! '
                         '\n\nЖдем тебя в стенах Уральского Федерального ❤️'
                         '\n\nОбщее количество набранных тобою очков за этот квест: <b>{}</b>'.format(correct_answers),
                         parse_mode='html')


@dp.message_handler(lambda msg: msg.text == 'Quiz')
async def quiz(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT quiz_ivt_block FROM data WHERE id = {people_id}")
    quiz_ivt_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_applied_inf_block FROM data WHERE id = {people_id}")
    quiz_applied_inf_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_software_engineering_block FROM data WHERE id = {people_id}")
    quiz_software_engineering_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_information_security_block FROM data WHERE id = {people_id}")
    quiz_information_security_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_management_block FROM data WHERE id = {people_id}")
    quiz_management_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_production_technology_block FROM data WHERE id = {people_id}")
    quiz_production_technology_block = cursor.fetchone()[0]
    if quiz_ivt_block == 1:
        cursor.execute(f"UPDATE data SET quiz_ivt_block = 2 WHERE id = {people_id}")
        connect.commit()
        question = '<b>Основные направления ИВТ:</b>\n\n1. Электроника, программирование, ' \
                   'работа в команде\n2. Экономика в проектах, информационные технологии, ' \
                   'презентация проектов\n3. Технические дисциплины, дизайн, основы управления производством\n\n\n' \
                   '<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    elif quiz_applied_inf_block == 1:
        cursor.execute(f"UPDATE data SET quiz_applied_inf_block = 2 WHERE id = {people_id}")
        connect.commit()
        question = '<b>Прикладная информатика затрагивает множество разнообразных сфер деятельности. Каких?</b>' \
                   '\n\n1. Информационные технологии, экономика, дизайн и гуманитарные науки\n2. ' \
                   'Разработка программ, проектирование интерфейсов, работа в команде\n3. Безопасность ' \
                   'к операциям в киберпространстве для самых разных отраслей экономики и управления' \
                   '\n\n<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    elif quiz_software_engineering_block == 1:
        cursor.execute(f"UPDATE data SET quiz_software_engineering_block = 2 WHERE id = {people_id}")
        connect.commit()
        question = '<b>Основные обязанности специалиста в данном направлении:</b>\n\n' \
                   '1. Контроль всех этапов процесса производства IT ' \
                   'продукта\n2. Безопасность к операциям в киберпространстве для самых разных ' \
                   'отраслей экономики и управления\n3. Управление производством, ' \
                   'дизайн\n\n<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    elif quiz_information_security_block == 1:
        cursor.execute(f"UPDATE data SET quiz_information_security_block = 2 WHERE id = {people_id}")
        connect.commit()
        question = '<b>Чем занимаются выпускники направления «Информационная безопасность»?</b>' \
                   '\n\n1. Анализируют потребности пользователей, разрабатывают программное ' \
                   'обеспечение, внедряют, проверяют на качество и поддерживают его\n2. ' \
                   'Разработка разнообразных радиотехнических систем разного назначения: ' \
                   'наземного, морского, авиационного и космического базирования\n3. Заботятся ' \
                   'о наших персональных данных и обеспечивают безопасность автоматизированных ' \
                   'систем управления технологическими процессами\n\n<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    elif quiz_management_block == 1:
        cursor.execute(f"UPDATE data SET quiz_management_block = 2 WHERE id = {people_id}")
        connect.commit()
        question = '<b>Что изучают студенты в рамках данной образовательной программы?</b>\n\n1. ' \
                   'Моделирования, экспериментального исследования, ввод в эксплуатацию на действующих' \
                   ' объектах и техническое обслуживание\n2. Системы автоматизации, управления, контроля, ' \
                   'технического диагностирования и информационного обеспечения\n3. Все из ' \
                   'перечисленного\n\n<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    elif quiz_production_technology_block == 1:
        cursor.execute(f"UPDATE data SET quiz_production_technology_block = 2 WHERE id = {people_id}")
        connect.commit()
        question = '<b>Кем ты можешь стать, окончив данное направление?</b>\n\n1. ' \
                   'frontend-разработчиком\n2. Колористом\n3. ' \
                   'Менеджером продаж\n\n<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')


@dp.message_handler(lambda msg: msg.text == '1')
async def answer_1(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT quiz_ivt_block FROM data WHERE id = {people_id}")
    quiz_ivt_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_applied_inf_block FROM data WHERE id = {people_id}")
    quiz_applied_inf_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_software_engineering_block FROM data WHERE id = {people_id}")
    quiz_software_engineering_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_information_security_block FROM data WHERE id = {people_id}")
    quiz_information_security_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_management_block FROM data WHERE id = {people_id}")
    quiz_management_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_production_technology_block FROM data WHERE id = {people_id}")
    quiz_production_technology_block = cursor.fetchone()[0]

    if quiz_ivt_block == 2:
        cursor.execute(f"UPDATE data SET quiz_ivt_block = 3 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
        correct_answers = cursor.fetchone()[0]

        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_applied_inf_block == 2:
        cursor.execute(f"UPDATE data SET quiz_applied_inf_block = 3 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
        correct_answers = cursor.fetchone()[0]

        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_software_engineering_block == 2:
        cursor.execute(f"UPDATE data SET quiz_software_engineering_block = 3 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
        correct_answers = cursor.fetchone()[0]

        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_information_security_block == 2:
        cursor.execute(f"UPDATE data SET quiz_information_security_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>3. Заботятся о наших персональных ' \
                     'данных и обеспечивают безопасность автоматизированных ' \
                     'систем управления технологическими процессами</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_management_block == 2:
        cursor.execute(f"UPDATE data SET quiz_management_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>3. Все из перечисленного</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_production_technology_block == 2:
        cursor.execute(f"UPDATE data SET quiz_production_technology_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>2. Колористом</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == '2')
async def answer_2(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT quiz_ivt_block FROM data WHERE id = {people_id}")
    quiz_ivt_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_applied_inf_block FROM data WHERE id = {people_id}")
    quiz_applied_inf_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_software_engineering_block FROM data WHERE id = {people_id}")
    quiz_software_engineering_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_information_security_block FROM data WHERE id = {people_id}")
    quiz_information_security_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_management_block FROM data WHERE id = {people_id}")
    quiz_management_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_production_technology_block FROM data WHERE id = {people_id}")
    quiz_production_technology_block = cursor.fetchone()[0]

    if quiz_ivt_block == 2:
        cursor.execute(f"UPDATE data SET quiz_ivt_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Электроника, программирование, работа в команде</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_applied_inf_block == 2:
        cursor.execute(f"UPDATE data SET quiz_applied_inf_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Информационные технологии, экономика, дизайн и гуманитарные науки</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_software_engineering_block == 2:
        cursor.execute(f"UPDATE data SET quiz_software_engineering_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Контроль всех этапов процесса производства IT</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_information_security_block == 2:
        cursor.execute(f"UPDATE data SET quiz_information_security_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>3. Заботятся о наших персональных ' \
                     'данных и обеспечивают безопасность автоматизированных ' \
                     'систем управления технологическими процессами</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_management_block == 2:
        cursor.execute(f"UPDATE data SET quiz_management_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>3. Все из перечисленного</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_production_technology_block == 2:
        cursor.execute(f"UPDATE data SET quiz_production_technology_block = 3 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
        correct_answers = cursor.fetchone()[0]

        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == '3')
async def answer_3(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT quiz_ivt_block FROM data WHERE id = {people_id}")
    quiz_ivt_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_applied_inf_block FROM data WHERE id = {people_id}")
    quiz_applied_inf_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_software_engineering_block FROM data WHERE id = {people_id}")
    quiz_software_engineering_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_information_security_block FROM data WHERE id = {people_id}")
    quiz_information_security_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_management_block FROM data WHERE id = {people_id}")
    quiz_management_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_production_technology_block FROM data WHERE id = {people_id}")
    quiz_production_technology_block = cursor.fetchone()[0]

    if quiz_ivt_block == 2:
        cursor.execute(f"UPDATE data SET quiz_ivt_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Электроника, программирование, работа в команде</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_applied_inf_block == 2:
        cursor.execute(f"UPDATE data SET quiz_applied_inf_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Информационные технологии, экономика, дизайн и гуманитарные науки</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_software_engineering_block == 2:
        cursor.execute(f"UPDATE data SET quiz_software_engineering_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Контроль всех этапов процесса производства IT</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_information_security_block == 2:
        cursor.execute(f"UPDATE data SET quiz_information_security_block = 3 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
        correct_answers = cursor.fetchone()[0]

        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_management_block == 2:
        cursor.execute(f"UPDATE data SET quiz_management_block = 3 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
        correct_answers = cursor.fetchone()[0]

        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif quiz_production_technology_block == 2:
        cursor.execute(f"UPDATE data SET quiz_production_technology_block = 3 WHERE id = {people_id}")
        connect.commit()

        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>2. Колористом</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Следующая задача')
async def next_task(msg: types.Message):
    @dp.message_handler()
    async def check_answer(msg: types.Message):
        people_id = msg.chat.id
        cursor.execute(f"SELECT quiz_ivt_block_next_task FROM data WHERE id = {people_id}")
        quiz_ivt_block_next_task = cursor.fetchone()[0]

        cursor.execute(f"SELECT quiz_applied_inf_block_next_task FROM data WHERE id = {people_id}")
        quiz_applied_inf_block_next_task = cursor.fetchone()[0]

        cursor.execute(f"SELECT quiz_software_engineering_block_next_task FROM data WHERE id = {people_id}")
        quiz_software_engineering_block_next_task = cursor.fetchone()[0]

        cursor.execute(f"SELECT quiz_information_security_block_next_task FROM data WHERE id = {people_id}")
        quiz_information_security_block_next_task = cursor.fetchone()[0]

        cursor.execute(f"SELECT quiz_management_block_next_task FROM data WHERE id = {people_id}")
        quiz_management_block_next_task = cursor.fetchone()[0]

        cursor.execute(f"SELECT quiz_production_technology_block_next_task FROM data WHERE id = {people_id}")
        quiz_production_technology_block_next_task = cursor.fetchone()[0]

        cursor.execute(f"SELECT written_attempts FROM data WHERE id = {people_id}")
        written_attempts = cursor.fetchone()[0]

        # блок по ИВТ
        if quiz_ivt_block_next_task == 1 and msg.text == '25' and written_attempts != 0:
            cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET quiz_ivt_block_next_task = 2 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
            correct_answers = cursor.fetchone()[0]

            info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
                .format(correct_answers)
            await msg.answer(info, parse_mode='html')

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif quiz_ivt_block_next_task == 1 and msg.text != '25':
            if written_attempts == 3:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()

                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось <b>2</b> попытки.'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 2:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась <b>последняя</b> попытка!'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 1:
                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET quiz_ivt_block_next_task = 2 WHERE id = {people_id}")
                connect.commit()

                info = 'К сожалению, попытки закончились. Правильный ответ: <b>25</b>'
                await msg.answer(info, parse_mode='html')

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        # блок по прикладной информатике
        elif quiz_applied_inf_block_next_task == 1 and msg.text == '9' and written_attempts != 0:
            cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET quiz_applied_inf_block_next_task = 2 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
            correct_answers = cursor.fetchone()[0]

            info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
                .format(correct_answers)
            await msg.answer(info, parse_mode='html')

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_back = types.KeyboardButton('Следующая задача')
            keyboard_back.add(button_back)

            await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                             reply_markup=keyboard_back)
        elif quiz_applied_inf_block_next_task == 1 and msg.text != '9':
            if written_attempts == 3:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось <b>2</b> попытки.'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 2:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась <b>последняя</b> попытка!'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 1:
                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET quiz_applied_inf_block_next_task = 2 WHERE id = {people_id}")
                connect.commit()

                info = 'К сожалению, попытки закончились. Правильный ответ: <b>9</b>'
                await msg.answer(info, parse_mode='html')

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button_back = types.KeyboardButton('Следующая задача')
                keyboard_back.add(button_back)

                await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                                 reply_markup=keyboard_back)
        elif quiz_applied_inf_block_next_task == 3 and msg.text == '44' and written_attempts != 0:
            cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET quiz_applied_inf_block_next_task = 4 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
            correct_answers = cursor.fetchone()[0]

            info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
                .format(correct_answers)
            await msg.answer(info, parse_mode='html')

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif quiz_applied_inf_block_next_task == 3 and msg.text != '44':
            if written_attempts == 3:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось <b>2</b> попытки.'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 2:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась <b>последняя</b> попытка!'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 1:
                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET quiz_applied_inf_block_next_task = 4 WHERE id = {people_id}")
                connect.commit()

                info = 'К сожалению, попытки закончились. Правильный ответ: <b>44</b>'
                await msg.answer(info, parse_mode='html')

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        # блок по программной инженерии
        elif quiz_software_engineering_block_next_task == 1 and msg.text == '88999' and written_attempts != 0:
            cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET quiz_software_engineering_block_next_task = 2 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
            correct_answers = cursor.fetchone()[0]

            info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
                .format(correct_answers)
            await msg.answer(info, parse_mode='html')

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif quiz_software_engineering_block_next_task == 1 and msg.text != '88999':
            if written_attempts == 3:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось <b>2</b> попытки.'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 2:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась <b>последняя</b> попытка!'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 1:
                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET quiz_software_engineering_block_next_task = 2 WHERE id = {people_id}")
                connect.commit()

                info = 'К сожалению, попытки закончились. Правильный ответ: <b>88999</b>'
                await msg.answer(info, parse_mode='html')

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        elif quiz_software_engineering_block_next_task == 3 and msg.text == '24' and written_attempts != 0:
            cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET quiz_software_engineering_block_next_task = 4 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
            correct_answers = cursor.fetchone()[0]

            info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
                .format(correct_answers)
            await msg.answer(info, parse_mode='html')

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif quiz_software_engineering_block_next_task == 3 and msg.text != '24':
            if written_attempts == 3:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось <b>2</b> попытки.'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 2:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась <b>последняя</b> попытка!'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 1:
                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET quiz_software_engineering_block_next_task = 4 WHERE id = {people_id}")
                connect.commit()

                info = 'К сожалению, попытки закончились. Правильный ответ: <b>24</b>'
                await msg.answer(info, parse_mode='html')

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        # блок по информационной безопасности
        elif quiz_information_security_block_next_task == 1 and msg.text == '70' and written_attempts != 0:
            cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET quiz_information_security_block_next_task = 2 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
            correct_answers = cursor.fetchone()[0]

            info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
                .format(correct_answers)
            await msg.answer(info, parse_mode='html')

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif quiz_information_security_block_next_task == 1 and msg.text != '70':
            if written_attempts == 3:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось <b>2</b> попытки.'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 2:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась <b>последняя</b> попытка!'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 1:
                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET quiz_information_security_block_next_task = 2 WHERE id = {people_id}")
                connect.commit()

                info = 'К сожалению, попытки закончились. Правильный ответ: <b>70</b>'
                await msg.answer(info, parse_mode='html')

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        elif quiz_information_security_block_next_task == 3 and msg.text == '4' and written_attempts != 0:
            cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET quiz_information_security_block_next_task = 4 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
            correct_answers = cursor.fetchone()[0]

            info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
                .format(correct_answers)
            await msg.answer(info, parse_mode='html')

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif quiz_information_security_block_next_task == 3 and msg.text != '4':
            if written_attempts == 3:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось <b>2</b> попытки.'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 2:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась <b>последняя</b> попытка!'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 1:
                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET quiz_information_security_block_next_task = 4 WHERE id = {people_id}")
                connect.commit()

                info = 'К сожалению, попытки закончились. Правильный ответ: <b>4</b>'
                await msg.answer(info, parse_mode='html')

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        # блок по управлению в системах
        elif quiz_management_block_next_task == 1 and msg.text == '90' and written_attempts != 0:
            cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET quiz_management_block_next_task = 2 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
            correct_answers = cursor.fetchone()[0]

            info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
                .format(correct_answers)
            await msg.answer(info, parse_mode='html')

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif quiz_management_block_next_task == 1 and msg.text != '90':
            if written_attempts == 3:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось <b>2</b> попытки.'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 2:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась <b>последняя</b> попытка!'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 1:
                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET quiz_management_block_next_task = 2 WHERE id = {people_id}")
                connect.commit()

                info = 'К сожалению, попытки закончились. Правильный ответ: <b>90</b>'
                await msg.answer(info, parse_mode='html')

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        # блок по полиграфии
        elif quiz_production_technology_block_next_task == 1 and msg.text == '24' and written_attempts != 0:
            cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET quiz_production_technology_block_next_task = 2 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"UPDATE data SET correct_answers = correct_answers + 1 WHERE id = {people_id}")
            connect.commit()

            cursor.execute(f"SELECT correct_answers FROM data WHERE id = {people_id}")
            correct_answers = cursor.fetchone()[0]

            info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
                .format(correct_answers)
            await msg.answer(info, parse_mode='html')

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif quiz_production_technology_block_next_task == 1 and msg.text != '24':
            if written_attempts == 3:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось <b>2</b> попытки.'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 2:
                cursor.execute(f"UPDATE data SET written_attempts = written_attempts - 1 WHERE id = {people_id}")
                connect.commit()
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась <b>последняя</b> попытка!'
                await msg.answer(info, parse_mode='html')
            elif written_attempts == 1:
                cursor.execute(f"UPDATE data SET written_attempts = 3 WHERE id = {people_id}")
                connect.commit()

                cursor.execute(f"UPDATE data SET quiz_production_technology_block_next_task = 2 WHERE id = {people_id}")
                connect.commit()

                info = 'К сожалению, попытки закончились. Правильный ответ: <b>24</b>'
                await msg.answer(info, parse_mode='html')

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)

    people_id = msg.chat.id
    cursor.execute(f"SELECT quiz_ivt_block FROM data WHERE id = {people_id}")
    quiz_ivt_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_ivt_block_next_task FROM data WHERE id = {people_id}")
    quiz_ivt_block_next_task = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_applied_inf_block FROM data WHERE id = {people_id}")
    quiz_applied_inf_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_applied_inf_block_next_task FROM data WHERE id = {people_id}")
    quiz_applied_inf_block_next_task = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_software_engineering_block FROM data WHERE id = {people_id}")
    quiz_software_engineering_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_software_engineering_block_next_task FROM data WHERE id = {people_id}")
    quiz_software_engineering_block_next_task = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_information_security_block FROM data WHERE id = {people_id}")
    quiz_information_security_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_information_security_block_next_task FROM data WHERE id = {people_id}")
    quiz_information_security_block_next_task = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_management_block FROM data WHERE id = {people_id}")
    quiz_management_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_management_block_next_task FROM data WHERE id = {people_id}")
    quiz_management_block_next_task = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_production_technology_block FROM data WHERE id = {people_id}")
    quiz_production_technology_block = cursor.fetchone()[0]

    cursor.execute(f"SELECT quiz_production_technology_block_next_task FROM data WHERE id = {people_id}")
    quiz_production_technology_block_next_task = cursor.fetchone()[0]

    if quiz_ivt_block == 3 and quiz_ivt_block_next_task == 0:
        cursor.execute(f"UPDATE data SET quiz_ivt_block_next_task = 1 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/task_ivt.png', 'rb'), 'Реши задачу:')
    elif quiz_applied_inf_block == 3 and quiz_applied_inf_block_next_task == 0:
        cursor.execute(f"UPDATE data SET quiz_applied_inf_block_next_task = 1 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/task_applied_inf.png', 'rb'), 'Реши задачу:')
    elif quiz_applied_inf_block == 3 and quiz_applied_inf_block_next_task == 2:
        cursor.execute(f"UPDATE data SET quiz_applied_inf_block_next_task = 3 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/task_applied_inf_2.png', 'rb'), 'Реши задачу:')
    elif quiz_software_engineering_block == 3 and quiz_software_engineering_block_next_task == 0:
        cursor.execute(f"UPDATE data SET quiz_software_engineering_block_next_task = 1 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/task_software_engineering.png', 'rb'), 'Реши задачу:')
    elif quiz_software_engineering_block == 3 and quiz_software_engineering_block_next_task == 2:
        cursor.execute(f"UPDATE data SET quiz_software_engineering_block_next_task = 3 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/task_software_engineering_2.png', 'rb'), 'Реши задачу:')
    elif quiz_information_security_block == 3 and quiz_information_security_block_next_task == 0:
        cursor.execute(f"UPDATE data SET quiz_information_security_block_next_task = 1 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/task_information_security.png', 'rb'), 'Реши задачу:')
    elif quiz_information_security_block == 3 and quiz_information_security_block_next_task == 2:
        cursor.execute(f"UPDATE data SET quiz_information_security_block_next_task = 3 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/task_information_security_2.png', 'rb'), 'Реши задачу:')
    elif quiz_management_block == 3 and quiz_management_block_next_task == 0:
        cursor.execute(f"UPDATE data SET quiz_management_block_next_task = 1 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/task_management.png', 'rb'), 'Реши задачу:')
    elif quiz_production_technology_block == 3 and quiz_production_technology_block_next_task == 0:
        cursor.execute(f"UPDATE data SET quiz_production_technology_block_next_task = 1 WHERE id = {people_id}")
        connect.commit()
        await msg.answer_photo(open('pictures/info/task_printing_technologies.png', 'rb'), 'Реши задачу:')


@dp.message_handler(lambda msg: msg.text == 'ИВТ 🖥️')
async def ivt_block(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_ivt_block FROM data WHERE id = {people_id}")
    viewing_ivt_block = cursor.fetchone()[0]
    if checker == 12 and viewing_ivt_block == 0:
        cursor.execute(f"UPDATE data SET viewing_blocks = viewing_blocks + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET quiz_ivt_block = 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET viewing_ivt_block = 1 WHERE id = {people_id}")
        connect.commit()

        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://priem-rtf.urfu.ru/ru/baccalaureate/courses/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239068')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/ivt.png', 'rb'),
                               reply_markup=keyboard)

        keyboard_quiz = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_quiz = types.KeyboardButton('Quiz')
        keyboard_quiz.add(button_quiz)

        await msg.answer('Чтобы проверить свои знания по направлению нажми на кнопку "Quiz"',
                         reply_markup=keyboard_quiz)
    elif checker == 12 and viewing_ivt_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Прикладная информатика 💻')
async def applied_inf_block(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_applied_inf_block FROM data WHERE id = {people_id}")
    viewing_applied_inf_block = cursor.fetchone()[0]
    if checker == 12 and viewing_applied_inf_block == 0:
        cursor.execute(f"UPDATE data SET viewing_blocks = viewing_blocks + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET quiz_applied_inf_block = 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET viewing_applied_inf_block = 1 WHERE id = {people_id}")
        connect.commit()

        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/9796/documents/2021/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239065')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/applied_inf.png', 'rb'),
                               reply_markup=keyboard)

        keyboard_quiz = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_quiz = types.KeyboardButton('Quiz')
        keyboard_quiz.add(button_quiz)

        await msg.answer('Чтобы проверить свои знания по направлению нажми на кнопку "Quiz"',
                         reply_markup=keyboard_quiz)
    elif checker == 12 and viewing_applied_inf_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Программная инженерия 💻')
async def software_engineering_block(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_software_engineering_block FROM data WHERE id = {people_id}")
    viewing_software_engineering_block = cursor.fetchone()[0]
    if checker == 12 and viewing_software_engineering_block == 0:
        cursor.execute(f"UPDATE data SET viewing_blocks = viewing_blocks + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET quiz_software_engineering_block = 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET viewing_software_engineering_block = 1 WHERE id = {people_id}")
        connect.commit()

        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/9797/documents/2021/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239066')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/software_engineering.png', 'rb'),
                               reply_markup=keyboard)

        keyboard_quiz = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_quiz = types.KeyboardButton('Quiz')
        keyboard_quiz.add(button_quiz)

        await msg.answer('Чтобы проверить свои знания по направлению нажми на кнопку "Quiz"',
                         reply_markup=keyboard_quiz)
    elif checker == 12 and viewing_software_engineering_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Информационная безопасность 🔒')
async def information_security_block(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_information_security_block FROM data WHERE id = {people_id}")
    viewing_information_security_block = cursor.fetchone()[0]
    if checker == 12 and viewing_information_security_block == 0:
        cursor.execute(f"UPDATE data SET viewing_blocks = viewing_blocks + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET quiz_information_security_block = 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET viewing_information_security_block = 1 WHERE id = {people_id}")
        connect.commit()

        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/10216/documents/2021/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239076')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/information_security.png', 'rb'),
                               reply_markup=keyboard)

        keyboard_quiz = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_quiz = types.KeyboardButton('Quiz')
        keyboard_quiz.add(button_quiz)

        await msg.answer('Чтобы проверить свои знания по направлению нажми на кнопку "Quiz"',
                         reply_markup=keyboard_quiz)
    elif checker == 12 and viewing_information_security_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


async def electronics(msg):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_1 = types.KeyboardButton('Инфокоммуникационные технологии и системы связи')
    button_2 = types.KeyboardButton('Конструирование и технология электронных средств')
    button_3 = types.KeyboardButton('Радиотехника')
    keyboard.add(button_1)
    keyboard.add(button_2)
    keyboard.add(button_3)

    await msg.answer('Выбери направление:', reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Электроника, радиотехника и системы связи 📡')
async def electronics_block(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_electronics_block FROM data WHERE id = {people_id}")
    viewing_electronics_block = cursor.fetchone()[0]
    if checker == 12 and viewing_electronics_block == 0:
        cursor.execute(f"UPDATE data SET viewing_blocks = viewing_blocks + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET quiz_electronics_block = 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET viewing_electronics_block = 1 WHERE id = {people_id}")
        connect.commit()

        await electronics(msg)

    elif checker == 12 and viewing_electronics_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Инфокоммуникационные технологии и системы связи')
async def communication_systems(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_communication_systems_block FROM data WHERE id = {people_id}")
    viewing_communication_systems_block = cursor.fetchone()[0]
    if checker == 12 and viewing_communication_systems_block == 0:
        cursor.execute(f"UPDATE data SET electronics_count = electronics_count + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET quiz_communication_systems_block = 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET viewing_communication_systems_block = 1 WHERE id = {people_id}")
        connect.commit()

        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/9813/documents/2021/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239077')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/communication.png', 'rb'),
                               reply_markup=keyboard)
        cursor.execute(f"SELECT electronics_count FROM data WHERE id = {people_id}")
        electronics_count = cursor.fetchone()[0]
        if electronics_count != 3:
            await electronics(msg)
        else:
            await list_of_destinations(msg)
    elif checker == 12 and viewing_communication_systems_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Конструирование и технология электронных средств')
async def construction(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_construction_block FROM data WHERE id = {people_id}")
    viewing_construction_block = cursor.fetchone()[0]
    if checker == 12 and viewing_construction_block == 0:
        cursor.execute(f"UPDATE data SET electronics_count = electronics_count + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET quiz_construction_block = 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET viewing_construction_block = 1 WHERE id = {people_id}")
        connect.commit()

        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/9814/documents/2021/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239077')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/construction.png', 'rb'),
                               reply_markup=keyboard)
        cursor.execute(f"SELECT electronics_count FROM data WHERE id = {people_id}")
        electronics_count = cursor.fetchone()[0]
        if electronics_count != 3:
            await electronics(msg)
        else:
            await list_of_destinations(msg)
    elif checker == 12 and viewing_construction_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Радиотехника')
async def radio(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_radio_block FROM data WHERE id = {people_id}")
    viewing_radio_block = cursor.fetchone()[0]
    if checker == 12 and viewing_radio_block == 0:
        cursor.execute(f"UPDATE data SET electronics_count = electronics_count + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET quiz_radio_block = 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET viewing_radio_block = 1 WHERE id = {people_id}")
        connect.commit()

        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/9812/documents/2021/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239077')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/radio.png', 'rb'),
                               reply_markup=keyboard)
        cursor.execute(f"SELECT electronics_count FROM data WHERE id = {people_id}")
        electronics_count = cursor.fetchone()[0]
        if electronics_count != 3:
            await electronics(msg)
        else:
            await list_of_destinations(msg)
    elif checker == 12 and viewing_radio_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Управление в технических системах 📟')
async def management_block(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_management_block FROM data WHERE id = {people_id}")
    viewing_management_block = cursor.fetchone()[0]
    if checker == 12 and viewing_management_block == 0:
        cursor.execute(f"UPDATE data SET viewing_blocks = viewing_blocks + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET quiz_management_block = 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET viewing_management_block = 1 WHERE id = {people_id}")
        connect.commit()

        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/9846/documents/2021/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239070')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/management.png', 'rb'),
                               reply_markup=keyboard)

        keyboard_quiz = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_quiz = types.KeyboardButton('Quiz')
        keyboard_quiz.add(button_quiz)

        await msg.answer('Чтобы проверить свои знания по направлению нажми на кнопку "Quiz"',
                         reply_markup=keyboard_quiz)
    elif checker == 12 and viewing_management_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Технология полиграфического и упаковочного производства 📄')
async def production_technology_block(msg: types.Message):
    people_id = msg.chat.id
    cursor.execute(f"SELECT checker FROM data WHERE id = {people_id}")
    checker = cursor.fetchone()[0]

    cursor.execute(f"SELECT viewing_production_technology_block FROM data WHERE id = {people_id}")
    viewing_production_technology_block = cursor.fetchone()[0]
    if checker == 12 and viewing_production_technology_block == 0:
        cursor.execute(f"UPDATE data SET viewing_blocks = viewing_blocks + 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET quiz_production_technology_block = 1 WHERE id = {people_id}")
        connect.commit()

        cursor.execute(f"UPDATE data SET viewing_production_technology_block = 1 WHERE id = {people_id}")
        connect.commit()

        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/9833/documents/2020/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239071')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/printing_technologies.png', 'rb'),
                               reply_markup=keyboard)

        keyboard_quiz = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_quiz = types.KeyboardButton('Quiz')
        keyboard_quiz.add(button_quiz)

        await msg.answer('Чтобы проверить свои знания по направлению нажми на кнопку "Quiz"',
                         reply_markup=keyboard_quiz)
    elif checker == 12 and viewing_production_technology_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


if __name__ == '__main__':
    executor.start_polling(dp)
