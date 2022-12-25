import asyncio
from aiogram import Bot, Dispatcher, types, executor
import Values

TOKEN = None

with open('token.txt') as file:
    TOKEN = file.read().strip()
    file.close()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# весь код будет разбит на несколько файлов, просто гораздо удобнее было писать все в одном месте,
# ибо есть зависимость от определенных блоков.
# так же будут в каких-то блоках заменю вложенные декораторы на стейты. Все изменения будут сделаны до основной защиты.



@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    mess = 'Привет, <b>{} {}</b>! Ты уже окончил школу или совсем скоро окончишь. ' \
           'Перед тобой появится сложный выбор – "Куда поступить?". ' \
           'Мы можем помочь тебе с этим и расскажем об ИРИТ-РТФ!'.format(msg.from_user.first_name,
                                                                         msg.from_user.last_name)
    await msg.answer_photo(open('pictures/logo/entrant_irit-rtf.jpg', 'rb'), caption=mess, parse_mode='html')

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Поехали 🚀')
    keyboard.add(button)

    await msg.answer('Нажми "Поехали 🚀", чтобы начать путешествие по ИРИТ-РТФ!', reply_markup=keyboard)


@dp.message_handler(commands=['points'])
async def actual_points(msg: types.Message):
    mess = 'Количество баллов на данный момент: <b>{}</b>'.format(Values.correct_answers)
    await msg.answer(mess, parse_mode='html')


@dp.message_handler(lambda msg: msg.text == 'Поехали 🚀')
async def block_2(msg: types.Message):
    if Values.checker == 0:
        Values.checker = 1
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

        keyboard_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_2_1 = types.KeyboardButton('✅')
        keyboard_2.add(button_2_1)

        await msg.answer('Нажми "✅", если ты посмотрел видео и готов ответить на первый вопрос!',
                         reply_markup=keyboard_2)


@dp.message_handler(lambda msg: msg.text == '✅')
async def block_3(msg: types.Message):
    if Values.checker == 1:
        Values.checker = 2
        mess = 'Ооокей, теперь Вы немного знаете об ИРИТ-РТФ.\n' \
               'Но как же звучит один из его лозунгов, о котором рассказывается в видео?\n\nНапиши его!'
        await msg.answer(mess, reply_markup=types.ReplyKeyboardRemove())

        @dp.message_handler(lambda msg: msg.text == 'здесь ты выбираешь сам' or msg.text == 'здесь ты выбираешь сам!'
                                        or msg.text == 'здесь ты выбираешь сам.' or msg.text == 'Здесь ты выбираешь сам'
                                        or msg.text == 'Здесь ты выбираешь сам!' or msg.text == 'Здесь ты выбираешь сам.')
        async def block_4(msg: types.Message):
            if Values.checker == 2:
                Values.checker = 3
                Values.correct_answers += 1
                mess = 'Поздравляю, ты ответил верно! Количество очков на данный момент: <b>{}</b>\n\nКстати, ' \
                       'используя команду /points, ты всегда можешь узнать текущее количество баллов!' \
                    .format(Values.correct_answers)
                await msg.answer(mess, parse_mode='html')

                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button = types.KeyboardButton('Далее')
                keyboard.add(button)

                await msg.answer('Нажми "Далее", чтобы продолжить наше путешествие 🌠', reply_markup=keyboard)

        # @dp.message_handler(lambda msg: msg.text != 'здесь ты выбираешь сам' or msg.text != 'здесь ты выбираешь сам!'
        #                                 or msg.text != 'здесь ты выбираешь сам.' or msg.text != 'Здесь ты выбираешь сам'
        #                                 or msg.text != 'Здесь ты выбираешь сам!' or msg.text != 'Здесь ты выбираешь сам.')
        # async def block_4_wrong(msg: types.Message):
        #     if Values.checker == 2 and Values.written_attempts == 3:
        #         Values.written_attempts -= 1
        #         await msg.answer('Неправильный ответ, попробуй ещё раз! У тебя осталось <b>{}</b> попытки.'
        #                          .format(Values.written_attempts), parse_mode='html')
        #     elif Values.checker == 2 and Values.written_attempts == 2:
        #         Values.written_attempts -= 2
        #         await msg.answer(
        #             'Неправильный ответ. Хорошо обдумай следующий вариант, ведь у тебя осталась последняя попытка!')
        #     elif Values.checker == 2 and Values.written_attempts == 0:
        #         Values.checker = 3
        #         Values.written_attempts = 3
        #         await msg.answer('К сожалению, попытки закончились. Правильный ответ: '
        #                          '<b>здесь ты выбираешь сам</b>.', parse_mode='html')
        #         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #         button = types.KeyboardButton('Далее')
        #         keyboard.add(button)
        #
        #         await msg.answer('Нажми "Далее", чтобы продолжить наше путешествие 🌠', reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Далее')
async def block_5(msg: types.Message):
    if Values.checker == 3:
        Values.checker = 4
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Что это ¿ ?')
        keyboard.add(button)
        await msg.answer_photo(open('pictures/info/iot.png', 'rb'), reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Что это ¿ ?')
async def block_6(msg: types.Message):
    if Values.checker == 4:
        Values.checker = 5
        await msg.answer_photo(open('pictures/info/iot_2.png', 'rb'), reply_markup=types.ReplyKeyboardRemove())

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Продолжить')
        keyboard.add(button)
        await msg.answer('Время двигаться дальше! Нажми "Продолжить".', reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Продолжить')
async def block_7(msg: types.Message):
    if Values.checker == 5:
        Values.checker = 6
        mess = 'Ладно, ладно. ИОТ — это круто.\n\nНо иногда после сдачи лабораторной работы по физике или рефакторинга ' \
               'кода хочется отдохнуть и поиграть в компьютерные игры.\n\nИ тут ИРИТ-РТФ тоже может тебе помочь!'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Как же?')
        keyboard.add(button)
        await msg.answer_photo(open('pictures/cybersport/win.png', 'rb'), caption=mess, reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Как же?')
async def block_8(msg: types.Message):
    if Values.checker == 6:
        Values.checker = 7
        await msg.answer_photo(open('pictures/info/tournaments.png', 'rb'), reply_markup=types.ReplyKeyboardRemove())

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Где же?')
        keyboard.add(button)
        await msg.answer('Где же узнавать о всех событиях, которые проходят в институте?', reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Где же?')
async def block_9(msg: types.Message):
    if Values.checker == 7:
        Values.checker = 8
        mess = "<a href='https://t.me/Iritatoday'>Telegram-канал</a> о " \
               "самых актуальных новостях Института радиоэлектроники и " \
               "информационных технологий. ИРИТ-РТФ УрФУ."
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Продолжим')
        keyboard.add(button)
        await msg.answer_photo(open('pictures/logo/news.png', 'rb'),
                               caption=mess,
                               reply_markup=keyboard, parse_mode='html')


@dp.message_handler(lambda msg: msg.text == 'Продолжим')
async def block_10(msg: types.Message):
    if Values.checker == 8:
        Values.checker = 9
        mess = "Вернемся к любимой учёбе!\n\nПорой перед выбором института, хочется узнать о тех, кто его " \
               "закончил.\nОб этом тебе расскажут выпускники ИРИТ-РТФ в кратком <a href=" \
               "'https://vk.com/video/@iritrtf_urfu?z=video-165382372_456239060%2Fclub165382372%2Fpl_-165382372_-2'>" \
               "видео-ролике</a>" \
               "\nПодробнее можешь прочитать <a href='https://priem-rtf.urfu.ru/index.php?id=26065'>тут</a>"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('А что там с деньгами?')
        keyboard.add(button)
        await msg.answer_photo(open('pictures/logo/urfu.png', 'rb'),
                               caption=mess,
                               reply_markup=keyboard,
                               parse_mode='html')


@dp.message_handler(lambda msg: msg.text == 'А что там с деньгами?')
async def block_11(msg: types.Message):
    if Values.checker == 9:
        Values.checker = 10
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Что еще?')
        keyboard.add(button)
        await msg.answer_photo(open('pictures/info/money.png', 'rb'), reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == 'Что еще?')
async def block_12(msg: types.Message):
    if Values.checker == 10:
        Values.checker = 11
        await msg.answer_photo(open('pictures/info/money_pro.png', 'rb'), reply_markup=types.ReplyKeyboardRemove())

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
    if Values.checker == 11:
        Values.checker = 12
        await list_of_destinations(msg)


@dp.message_handler(lambda msg: msg.text == 'Назад')
async def calling_list_of_destinations(msg: types.Message):
    if Values.checker == 12:
        await list_of_destinations(msg)


@dp.message_handler(lambda msg: msg.text == 'Quiz')
async def quiz(msg: types.Message):
    if Values.quiz_ivt_block == 1:
        Values.quiz_ivt_block = 2
        question = '<b>Основные направления ИВТ:</b>\n\n1. Электроника, программирование, ' \
                   'работа в команде\n2. Экономика в проектах, информационные технологии, ' \
                   'презентация проектов\n3. Технические дисциплины, дизайн, основы управления производством\n\n\n' \
                   '<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    elif Values.quiz_applied_inf_block == 1:
        Values.quiz_applied_inf_block = 2
        question = '<b>Прикладная информатика затрагивает множество разнообразных сфер деятельности. Каких?</b>' \
                   '\n\n1. Информационные технологии, экономика, дизайн и гуманитарные науки\n2. ' \
                   'Разработка программ, проектирование интерфейсов, работа в команде\n3. Безопасность ' \
                   'к операциям в киберпространстве для самых разных отраслей экономики и управления' \
                   '\n\n<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    elif Values.quiz_software_engineering_block == 1:
        Values.quiz_software_engineering_block = 2
        question = '<b>Основные обязанности специалиста в данном направлении:</b>\n\n' \
                   '1. Контроль всех этапов процесса производства IT ' \
                   'продукта\n2. Безопасность к операциям в киберпространстве для самых разных ' \
                   'отраслей экономики и управления\n3. Управление производством, ' \
                   'дизайн\n\n<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    elif Values.quiz_information_security_block == 1:
        Values.quiz_information_security_block = 2
        question = '<b>Чем занимаются выпускники направления «Информационная безопасность»?</b>' \
                   '\n\n1. Анализируют потребности пользователей, разрабатывают программное ' \
                   'обеспечение, внедряют, проверяют на качество и поддерживают его\n2. ' \
                   'Разработка разнообразных радиотехнических систем разного назначения: ' \
                   'наземного, морского, авиационного и космического базирования\n3. Заботятся ' \
                   'о наших персональных данных и обеспечивают безопасность автоматизированных ' \
                   'систем управления технологическими процессами\n\n<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    elif Values.quiz_management_block == 1:
        Values.quiz_management_block = 2
        question = '<b>Что изучают студенты в рамках данной образовательной программы?</b>\n\n1. ' \
                   'Моделирования, экспериментального исследования, ввод в эксплуатацию на действующих' \
                   ' объектах и техническое обслуживание\n2. Системы автоматизации, управления, контроля, ' \
                   'технического диагностирования и информационного обеспечения\n3. Все из ' \
                   'перечисленного\n\n<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
    elif Values.quiz_production_technology_block == 1:
        Values.quiz_production_technology_block = 2
        question = '<b>Кем ты можешь стать, окончив данное направление?</b>\n\n1. ' \
                   'frontend-разработчиком\n2. Колористом\n3. ' \
                   'Менеджером продаж\n\n<i>Напиши номер правильного ответа!</i>'
        await msg.answer(question, reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')


@dp.message_handler(lambda msg: msg.text == '1')
async def answer_1(msg: types.Message):
    if Values.quiz_ivt_block == 2:
        Values.quiz_ivt_block = 3
        Values.correct_answers += 1
        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(Values.correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_applied_inf_block == 2:
        Values.quiz_applied_inf_block = 3
        Values.correct_answers += 1
        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(Values.correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_software_engineering_block == 2:
        Values.quiz_software_engineering_block = 3
        Values.correct_answers += 1
        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(Values.correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_information_security_block == 2:
        Values.quiz_information_security_block = 3
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
    elif Values.quiz_management_block == 2:
        Values.quiz_management_block = 3
        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>3. Все из перечисленного</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_production_technology_block == 2:
        Values.quiz_production_technology_block = 3
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
    if Values.quiz_ivt_block == 2:
        Values.quiz_ivt_block = 3
        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Электроника, программирование, работа в команде</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_applied_inf_block == 2:
        Values.quiz_applied_inf_block = 3
        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Информационные технологии, экономика, дизайн и гуманитарные науки</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_software_engineering_block == 2:
        Values.quiz_software_engineering_block = 3
        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Контроль всех этапов процесса производства IT</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_information_security_block == 2:
        Values.quiz_information_security_block = 3
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
    elif Values.quiz_management_block == 2:
        Values.quiz_management_block = 3
        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>3. Все из перечисленного</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_production_technology_block == 2:
        Values.quiz_production_technology_block = 3
        Values.correct_answers += 1
        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(Values.correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)


@dp.message_handler(lambda msg: msg.text == '3')
async def answer_3(msg: types.Message):
    if Values.quiz_ivt_block == 2:
        Values.quiz_ivt_block = 3
        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Электроника, программирование, работа в команде</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_applied_inf_block == 2:
        Values.quiz_applied_inf_block = 3
        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Информационные технологии, экономика, дизайн и гуманитарные науки</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_software_engineering_block == 2:
        Values.quiz_software_engineering_block = 3
        wrong_info = 'К сожалению, ты ответил неверно. ' \
                     'Правильный ответ:\n\n<b>1. Контроль всех этапов процесса производства IT</b>'
        await msg.answer(wrong_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_information_security_block == 2:
        Values.quiz_information_security_block = 3
        Values.correct_answers += 1
        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(Values.correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_management_block == 2:
        Values.quiz_management_block = 3
        Values.correct_answers += 1
        right_info = 'Ты ответил верно! Количество баллов на данный момент: <b>{}</b>' \
            .format(Values.correct_answers)
        await msg.answer(right_info, parse_mode='html')

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = types.KeyboardButton('Следующая задача')
        keyboard.add(button)

        await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                         reply_markup=keyboard)
    elif Values.quiz_production_technology_block == 2:
        Values.quiz_production_technology_block = 3
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
        # блок по ИВТ
        if Values.quiz_ivt_block_next_task == 1 and msg.text == '25' and Values.written_attempts != 0:
            Values.written_attempts = 3
            Values.quiz_ivt_block_next_task = 2
            Values.correct_answers += 1
            info = 'Ты ответил верно! Количество баллов на данный момент: {}' \
                .format(Values.correct_answers)
            await msg.answer(info)

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif Values.quiz_ivt_block_next_task == 1 and msg.text != '25':
            if Values.written_attempts == 3:
                Values.written_attempts -= 1
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось {} попытки.' \
                    .format(Values.written_attempts)
                await msg.answer(info)
            elif Values.written_attempts == 2:
                Values.written_attempts -= 1
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась последняя попытка!'
                await msg.answer(info)
            elif Values.written_attempts == 1:
                Values.written_attempts = 3
                Values.quiz_ivt_block_next_task = 2
                info = 'К сожалению, попытки закончились. Правильный ответ: 25'
                await msg.answer(info)

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        # блок по прикладной информатике
        elif Values.quiz_applied_inf_block_next_task == 1 and msg.text == '9' and Values.written_attempts != 0:
            Values.written_attempts = 3
            Values.quiz_applied_inf_block_next_task = 2
            Values.correct_answers += 1
            info = 'Ты ответил верно! Количество баллов на данный момент: {}' \
                .format(Values.correct_answers)
            await msg.answer(info)

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_back = types.KeyboardButton('Следующая задача')
            keyboard_back.add(button_back)

            await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                             reply_markup=keyboard_back)
        elif Values.quiz_applied_inf_block_next_task == 1 and msg.text != '9':
            if Values.written_attempts == 3:
                Values.written_attempts -= 1
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось {} попытки.' \
                    .format(Values.written_attempts)
                await msg.answer(info)
            elif Values.written_attempts == 2:
                Values.written_attempts -= 1
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась последняя попытка!'
                await msg.answer(info)
            elif Values.written_attempts == 1:
                Values.written_attempts = 3
                Values.quiz_applied_inf_block_next_task = 2
                info = 'К сожалению, попытки закончились. Правильный ответ: 9'
                await msg.answer(info)

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                button_back = types.KeyboardButton('Следующая задача')
                keyboard_back.add(button_back)

                await msg.answer('Если ты готов к выполнению очередного задания, нажми на кнопку "Следующая задача"!',
                                 reply_markup=keyboard_back)
        elif Values.quiz_applied_inf_block_next_task == 3 and msg.text == '44' and Values.written_attempts != 0:
            Values.written_attempts = 3
            Values.quiz_applied_inf_block_next_task = 4
            Values.correct_answers += 1
            info = 'Ты ответил верно! Количество баллов на данный момент: {}' \
                .format(Values.correct_answers)
            await msg.answer(info)

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif Values.quiz_applied_inf_block_next_task == 3 and msg.text != '44':
            if Values.written_attempts == 3:
                Values.written_attempts -= 1
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось {} попытки.' \
                    .format(Values.written_attempts)
                await msg.answer(info)
            elif Values.written_attempts == 2:
                Values.written_attempts -= 1
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась последняя попытка!'
                await msg.answer(info)
            elif Values.written_attempts == 1:
                Values.written_attempts = 3
                Values.quiz_applied_inf_block_next_task = 4
                info = 'К сожалению, попытки закончились. Правильный ответ: 44'
                await msg.answer(info)

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        # блок по программной инженерии
        elif Values.quiz_software_engineering_block_next_task == 1 and msg.text == '88999' and Values.written_attempts != 0:
            Values.written_attempts = 3
            Values.quiz_software_engineering_block_next_task = 2
            Values.correct_answers += 1
            info = 'Ты ответил верно! Количество баллов на данный момент: {}' \
                .format(Values.correct_answers)
            await msg.answer(info)

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif Values.quiz_software_engineering_block_next_task == 1 and msg.text != '88999':
            if Values.written_attempts == 3:
                Values.written_attempts -= 1
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось {} попытки.' \
                    .format(Values.written_attempts)
                await msg.answer(info)
            elif Values.written_attempts == 2:
                Values.written_attempts -= 1
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась последняя попытка!'
                await msg.answer(info)
            elif Values.written_attempts == 1:
                Values.written_attempts = 3
                Values.quiz_software_engineering_block_next_task = 2
                info = 'К сожалению, попытки закончились. Правильный ответ: 88999'
                await msg.answer(info)

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        elif Values.quiz_software_engineering_block_next_task == 3 and msg.text == '24' and Values.written_attempts != 0:
            Values.written_attempts = 3
            Values.quiz_software_engineering_block_next_task = 4
            Values.correct_answers += 1
            info = 'Ты ответил верно! Количество баллов на данный момент: {}' \
                .format(Values.correct_answers)
            await msg.answer(info)

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif Values.quiz_software_engineering_block_next_task == 3 and msg.text != '24':
            if Values.written_attempts == 3:
                Values.written_attempts -= 1
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось {} попытки.' \
                    .format(Values.written_attempts)
                await msg.answer(info)
            elif Values.written_attempts == 2:
                Values.written_attempts -= 1
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась последняя попытка!'
                await msg.answer(info)
            elif Values.written_attempts == 1:
                Values.written_attempts = 3
                Values.quiz_software_engineering_block_next_task = 4
                info = 'К сожалению, попытки закончились. Правильный ответ: 24'
                await msg.answer(info)

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        # блок по информационной безопасности
        elif Values.quiz_information_security_block_next_task == 1 and msg.text == '70' and Values.written_attempts != 0:
            Values.written_attempts = 3
            Values.quiz_information_security_block_next_task = 2
            Values.correct_answers += 1
            info = 'Ты ответил верно! Количество баллов на данный момент: {}' \
                .format(Values.correct_answers)
            await msg.answer(info)

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif Values.quiz_information_security_block_next_task == 1 and msg.text != '70':
            if Values.written_attempts == 3:
                Values.written_attempts -= 1
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось {} попытки.' \
                    .format(Values.written_attempts)
                await msg.answer(info)
            elif Values.written_attempts == 2:
                Values.written_attempts -= 1
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась последняя попытка!'
                await msg.answer(info)
            elif Values.written_attempts == 1:
                Values.written_attempts = 3
                Values.quiz_information_security_block_next_task = 2
                info = 'К сожалению, попытки закончились. Правильный ответ: 70'
                await msg.answer(info)

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        elif Values.quiz_information_security_block_next_task == 3 and msg.text == '4' and Values.written_attempts != 0:
            Values.written_attempts = 3
            Values.quiz_information_security_block_next_task = 4
            Values.correct_answers += 1
            info = 'Ты ответил верно! Количество баллов на данный момент: {}' \
                .format(Values.correct_answers)
            await msg.answer(info)

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif Values.quiz_information_security_block_next_task == 3 and msg.text != '4':
            if Values.written_attempts == 3:
                Values.written_attempts -= 1
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось {} попытки.' \
                    .format(Values.written_attempts)
                await msg.answer(info)
            elif Values.written_attempts == 2:
                Values.written_attempts -= 1
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась последняя попытка!'
                await msg.answer(info)
            elif Values.written_attempts == 1:
                Values.written_attempts = 3
                Values.quiz_information_security_block_next_task = 4
                info = 'К сожалению, попытки закончились. Правильный ответ: 4'
                await msg.answer(info)

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        # блок по управлению в системах
        elif Values.quiz_management_block_next_task == 1 and msg.text == '90' and Values.written_attempts != 0:
            Values.written_attempts = 3
            Values.quiz_management_block_next_task = 2
            Values.correct_answers += 1
            info = 'Ты ответил верно! Количество баллов на данный момент: {}' \
                .format(Values.correct_answers)
            await msg.answer(info)

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif Values.quiz_management_block_next_task == 1 and msg.text != '90':
            if Values.written_attempts == 3:
                Values.written_attempts -= 1
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось {} попытки.' \
                    .format(Values.written_attempts)
                await msg.answer(info)
            elif Values.written_attempts == 2:
                Values.written_attempts -= 1
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась последняя попытка!'
                await msg.answer(info)
            elif Values.written_attempts == 1:
                Values.written_attempts = 3
                Values.quiz_management_block_next_task = 2
                info = 'К сожалению, попытки закончились. Правильный ответ: 90'
                await msg.answer(info)

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)
        # блок по полиграфии
        elif Values.quiz_production_technology_block_next_task == 1 and msg.text == '24' and Values.written_attempts != 0:
            Values.written_attempts = 3
            Values.quiz_production_technology_block_next_task = 2
            Values.correct_answers += 1
            info = 'Ты ответил верно! Количество баллов на данный момент: {}' \
                .format(Values.correct_answers)
            await msg.answer(info)

            keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_back = types.KeyboardButton('Назад')
            keyboard_back.add(button_back)

            await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                             reply_markup=keyboard_back)
        elif Values.quiz_production_technology_block_next_task == 1 and msg.text != '24':
            if Values.written_attempts == 3:
                Values.written_attempts -= 1
                info = 'Неправильный ответ, попробуй еще раз! У тебя осталось {} попытки.' \
                    .format(Values.written_attempts)
                await msg.answer(info)
            elif Values.written_attempts == 2:
                Values.written_attempts -= 1
                info = 'Неправильный ответ. Хорошо обдумай следующий вариант, ' \
                       'ведь у тебя осталась последняя попытка!'
                await msg.answer(info)
            elif Values.written_attempts == 1:
                Values.written_attempts = 3
                Values.quiz_production_technology_block_next_task = 2
                info = 'К сожалению, попытки закончились. Правильный ответ: 24'
                await msg.answer(info)

                keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_back = types.KeyboardButton('Назад')
                keyboard_back.add(button_back)

                await msg.answer('Нажми "Назад", чтобы ознакомиться с другими направлениями!',
                                 reply_markup=keyboard_back)

    if Values.quiz_ivt_block == 3 and Values.quiz_ivt_block_next_task == 0:
        Values.quiz_ivt_block_next_task = 1
        await msg.answer_photo(open('pictures/info/task_ivt.png', 'rb'), 'Реши задачу:')
    elif Values.quiz_applied_inf_block == 3 and Values.quiz_applied_inf_block_next_task == 0:
        Values.quiz_applied_inf_block_next_task = 1
        await msg.answer_photo(open('pictures/info/task_applied_inf.png', 'rb'), 'Реши задачу:')
    elif Values.quiz_applied_inf_block == 3 and Values.quiz_applied_inf_block_next_task == 2:
        Values.quiz_applied_inf_block_next_task = 3
        await msg.answer_photo(open('pictures/info/task_applied_inf_2.png', 'rb'), 'Реши задачу:')
    elif Values.quiz_software_engineering_block == 3 and Values.quiz_software_engineering_block_next_task == 0:
        Values.quiz_software_engineering_block_next_task = 1
        await msg.answer_photo(open('pictures/info/task_software_engineering.png', 'rb'), 'Реши задачу:')
    elif Values.quiz_software_engineering_block == 3 and Values.quiz_software_engineering_block_next_task == 2:
        Values.quiz_software_engineering_block_next_task = 3
        await msg.answer_photo(open('pictures/info/task_software_engineering_2.png.png', 'rb'), 'Реши задачу:')
    elif Values.quiz_information_security_block == 3 and Values.quiz_information_security_block_next_task == 0:
        Values.quiz_information_security_block_next_task = 1
        await msg.answer_photo(open('pictures/info/task_information_security.png', 'rb'), 'Реши задачу:')
    elif Values.quiz_information_security_block == 3 and Values.quiz_information_security_block_next_task == 2:
        Values.quiz_information_security_block_next_task = 3
        await msg.answer_photo(open('pictures/info/task_information_security_2.png.png.png', 'rb'), 'Реши задачу:')
    elif Values.quiz_management_block == 3 and Values.quiz_management_block_next_task == 0:
        Values.quiz_management_block_next_task = 1
        await msg.answer_photo(open('pictures/info/task_management.png', 'rb'), 'Реши задачу:')
    elif Values.quiz_production_technology_block == 3 and Values.quiz_production_technology_block_next_task == 0:
        Values.quiz_production_technology_block_next_task = 1
        await msg.answer_photo(open('pictures/info/task_printing_technologies.png', 'rb'), 'Реши задачу:')


@dp.message_handler(lambda msg: msg.text == 'ИВТ 🖥️')
async def ivt_block(msg: types.Message):
    if Values.checker == 12 and Values.viewing_ivt_block == 0:
        Values.quiz_ivt_block = 1
        Values.viewing_ivt_block = 1
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
    elif Values.checker == 12 and Values.viewing_ivt_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Прикладная информатика 💻')
async def ivt_block(msg: types.Message):
    if Values.checker == 12 and Values.viewing_applied_inf_block == 0:
        Values.quiz_applied_inf_block = 1
        Values.viewing_applied_inf_block = 1
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
    elif Values.checker == 12 and Values.viewing_applied_inf_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Программная инженерия 💻')
async def software_engineering_block(msg: types.Message):
    if Values.checker == 12 and Values.viewing_software_engineering_block == 0:
        Values.quiz_software_engineering_block = 1
        Values.viewing_software_engineering_block = 1
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
    elif Values.checker == 12 and Values.viewing_software_engineering_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Информационная безопасность 🔒')
async def information_security_block(msg: types.Message):
    if Values.checker == 12 and Values.viewing_information_security_block == 0:
        Values.quiz_information_security_block = 1
        Values.viewing_information_security_block = 1
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
    elif Values.checker == 12 and Values.viewing_information_security_block == 1:
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
    if Values.checker == 12 and Values.viewing_electronics_block == 0:
        Values.quiz_electronics_block = 1
        Values.viewing_electronics_block = 1

        await electronics(msg)

    elif Values.checker == 12 and Values.viewing_electronics_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Инфокоммуникационные технологии и системы связи')
async def communication_systems(msg: types.Message):
    if Values.checker == 12 and Values.viewing_communication_systems_block == 0:
        Values.electronics_count += 1
        Values.quiz_communication_systems_block = 1
        Values.viewing_communication_systems_block = 1
        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/9813/documents/2021/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239077')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/communication.png', 'rb'),
                               reply_markup=keyboard)
        if Values.electronics_count != 3:
            await electronics(msg)
        else:
            await list_of_destinations(msg)
    elif Values.checker == 12 and Values.viewing_communication_systems_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Конструирование и технология электронных средств')
async def construction(msg: types.Message):
    if Values.checker == 12 and Values.viewing_construction_block == 0:
        Values.electronics_count += 1
        Values.quiz_construction_block = 1
        Values.viewing_construction_block = 1
        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/9814/documents/2021/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239077')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/construction.png', 'rb'),
                               reply_markup=keyboard)
        if Values.electronics_count != 3:
            await electronics(msg)
        else:
            await list_of_destinations(msg)
    elif Values.checker == 12 and Values.viewing_construction_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Радиотехника')
async def construction(msg: types.Message):
    if Values.checker == 12 and Values.viewing_radio_block == 0:
        Values.electronics_count += 1
        Values.quiz_radio_block = 1
        Values.viewing_radio_block = 1
        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Основные дисциплины',
                                              url='https://programs.edu.urfu.ru/ru/9812/documents/2021/')
        button_2 = types.InlineKeyboardButton(text='Краткий видео-ролик',
                                              url='https://vk.com/video-165382372_456239077')
        keyboard.row(button_1)
        keyboard.row(button_2)
        await msg.answer_photo(open('pictures/info/radio.png', 'rb'),
                               reply_markup=keyboard)
        if Values.electronics_count != 3:
            await electronics(msg)
        else:
            await list_of_destinations(msg)
    elif Values.checker == 12 and Values.viewing_construction_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Управление в технических системах 📟')
async def management_block(msg: types.Message):
    if Values.checker == 12 and Values.viewing_management_block == 0:
        Values.quiz_management_block = 1
        Values.viewing_management_block = 1
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
    elif Values.checker == 12 and Values.viewing_information_security_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


@dp.message_handler(lambda msg: msg.text == 'Технология полиграфического и упаковочного производства 📄')
async def production_technology_block(msg: types.Message):
    if Values.checker == 12 and Values.viewing_production_technology_block == 0:
        Values.quiz_production_technology_block = 1
        Values.viewing_production_technology_block = 1
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
    elif Values.checker == 12 and Values.viewing_production_technology_block == 1:
        await msg.answer('Ты уже ознакомился с этим направлением. Выбери другое!')


if __name__ == '__main__':
    executor.start_polling(dp)
