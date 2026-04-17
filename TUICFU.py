import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackQueryHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

# Пути к фото
ZAYAVKA_PHOTO = "KOZ.jpg"
MAIN_PHOTO = "InfoBot.jpg"

# Текст для заявки
APPLY_TEXT = (
    "˚₊‧✩ ˚₊‧꒰ა ʚიᵋº⁠⁠⁠⁠⁠⁠ᵌɞྀ ໒꒱ ‧₊˚ ✩‧₊˚\n"
    "Как подать заявку на участие в разработке?\n"
    "— Для подачи своей заявки Вам нужно заполнить соответствующую форму "
    "(https://docs.google.com/forms/d/e/1FAIpQLSfk5D5YOwZgedpSFmkmrCR6Rews0qq8NbhIOS-4pQ8ZE0pldA/viewform?usp=publish-editor). "
    "В случае одобрения Вашей заявки с Вами обязательно свяжутся (⁎˃ᴗ˂⁎)"
)

# Приветственный текст (caption для главной картинки)
WELCOME_TEXT = (
    "˚₊‧✩ ˚₊‧꒰ა ʚიᵋº⁠⁠⁠⁠⁠⁠ᵌɞྀ ໒꒱ ‧₊˚ ✩‧₊˚\n"
    "Здравствуй! Я информационный бот, Ваш виртуальный ассистент. "
    "Я помогу Вам разобраться с вакансиями и как оставить заявку для участия "
    "в нашей команде разработки! (⁎˃ᴗ˂⁎)\n\n"
    "Выбери соответствующую кнопку, чтобы подробнее узнать о проекте, "
    "вакансиях и требованиях к ним или же как подать заявку в сам проект"
)

# Текст + фото О проекте
ABOUT_TEXT = (
    "«TUICFU» или же «The Universe Is Crying for Us» - приключенческая игра в жанре драмы и психологического хоррора.\n"
    "Краткий сюжет:\n"
    "Прилежному ученику и воспитаннику приюта, Октанту, уготована особая роль – стать сосудом для угасающего Божества. Вот только это значит пожертвовать своей привычной жизнью, с чем Октант не готов мириться. Сможет ли он противостоять судьбе и спасти не только себя?\n\n"
    "Часто задаваемые вопросы:\n"
    "1) Сколько человек в команде?\n"
    "— На данный момент нас восемь человек. Два сценариста, два композитора, два художника, два программиста. Информация будет обновляться!\n\n"
    "2) Оплачивается ли работа?\n"
    "— Здесь сугубо по желанию. На данный момент большая часть команды работает для опыта/на энтузиазме. Однако, по желанию работа оплачивается, свой прайс Вы можете озвучить после того, как Вас примут в команду.\n"
    "ВАЖНАЯ ОГОВОРКА. С оплатой могут быть задержки или выплата частями, т.к. организатор проекта является студентом, у которого нет возможности совмещать работу и учебу. Имейте это в виду и спасибо за понимание!!\n\n"
    "3) Берете ли без портфолио?\n"
    "— Берём, но не на все должности! К примеру, путь в композиторы, художники и геймдизайнеры Вам точно будет закрыт при отсутствии портфолио!"
)
ABOUT_PHOTO = "OProecte.jpg"

BUTTON_DATA = {
    "org": (
        "Organizator.jpg",
        "˚₊‧✩ ˚₊‧꒰ა ʚიᵋº⁠⁠⁠⁠⁠⁠ᵌɞྀ ໒꒱ ‧₊˚ ✩‧₊˚\n"
        "Очень-очень ответственная роль! Организатор отвечает за ведение рабочего процесса, а именно: отслеживание дедлайнов, распределение и выдача работы и общая помощь с ведением проекта и его социальных сетей! (๑¯◡¯๑)\n\n"
        "Требования к организатору:\n"
        "- Ответственность \n"
        "- Регулярная активность\n"
        "- Инициативность \n"
        "- Умение общаться с командой и решать возможные конфликты \n"
        "- Планирование\n"
        "- Умение распределять задачи \n"
        "- Базовое понимание разработки игр\n\n"
        "(P.S. В проекте имеется организатор, но в одиночку справиться бывает довольно трудно.. не находите?)"
    ),
    "writer": (
        "Scenarist.jpg",
        "˚₊‧✩ ˚₊‧꒰ა ʚიᵋº⁠⁠⁠⁠⁠⁠ᵌɞྀ ໒꒱ ‧₊˚ ✩‧₊˚\n"
        "Сценарист отвечает за написание основной сюжетной линии и прописание сценария! (⁎˃ᴗ˂⁎)  \n\n"
        "Требования к сценаристу: \n"
        "- Ответственность \n"
        "- Инициативность\n"
        "- Грамотность и владение русским языком \n"
        "- Креативность \n"
        "- Умение принимать правки\n\n"
        "(P.S. после того как Вы пройдете первый этап набора организатор выдаст Вам тестовое задание для определения Ваших навыков!)"
    ),
    "narrative": (
        "NarativnijDizajner.jpg",
        "˚₊‧✩ ˚₊‧꒰ა ʚიᵋº⁠⁠⁠⁠⁠⁠ᵌɞྀ ໒꒱ ‧₊˚ ✩‧₊˚\n"
        "Нарративный дизайнер отвечает за то, как история встроена в игру (๑¯◡¯๑)\n\n"
        "Требования:\n"
        "- Базовое понимание сторителлинга \n"
        "- Базовое понимание геймдизайна \n"
        "- Понимание основ повествования и драматургии"
    ),
    "dev": (
        "Programist.jpg",
        "˚₊‧✩ ˚₊‧꒰ა ʚიᵋº⁠⁠⁠⁠⁠⁠ᵌɞྀ ໒꒱ ‧₊˚ ✩‧₊˚\n"
        "Программист отвечает за написание кода и работу на движке Unity  (๑¯◡¯๑)\n\n"
        "Требования к программисту:\n"
        "- Базовое знание C#\n"
        "- Навыки работы на движке Unity \n"
        "- Умение работать с чужим кодом \n"
        "- Умение находить и исправлять ошибки в коде"
    ),
    "composer": (
        "Kompozitor.jpg",
        "˚₊‧✩ ˚₊‧꒰ა ʚიᵋº⁠⁠⁠⁠⁠⁠ᵌɞྀ ໒꒱ ‧₊˚ ✩‧₊˚\n"
        "Композитор отвечает за написание музыкального сопровождения игры. Также на композитора частично возлагается работа над саунд-дизайном  (⁎˃ᴗ˂⁎) \n\n"
        "Требования к композитору:\n"
        "- Базовые музыкальные знания\n"
        "- Умение писать музыку под настроение/сцены \n"
        "- Обязательное наличие портфолио"
    ),
    "artist": (
        "Hudojnik.jpg",
        "˚₊‧✩ ˚₊‧꒰ა ʚიᵋº⁠⁠⁠⁠⁠⁠ᵌɞྀ ໒꒱ ‧₊˚ ✩‧₊˚\n"
        "Художники отвечают за визуал предстоящей игры. Делятся на несколько должностей (๑¯◡¯๑) \n"
        "1) Художники-фоновики\n"
        "Отвечают за отрисовку фонову по заданному тз\n\n"
        "2) Художник по спрайтам \n"
        "Помощь с разработкой спрайтов в заданном стиле\n\n"
        "3) Художник по кат-сценам\n"
        "Прорисовка с разработкой кат-сцен в заданном стиле, отрисовка фонов для кат-сцен. \n\n"
        "4) Художники уровней \n"
        "Разработка визуала уровней. Работа с окружением в геймплейной части. \n\n"
        "ОБЩИЕ требования:\n"
        "- Базовые художественные навыки \n"
        "- Умение подстроиться под стиль игры \n"
        "- Умение работать по ТЗ\n"
        "- Умение работать с перспективой \n"
        "- Умение работать с детализацией окружения \n"
        "- Наличие портфолио"
    ),
    "gamedev": (
        "GameDizainer.jpg",
        "˚₊‧✩ ˚₊‧꒰ა ʚიᵋº⁠⁠⁠⁠⁠⁠ᵌɞྀ ໒꒱ ‧₊˚ ✩‧₊˚\n"
        "Геймдизайнер отвечает за разработку механик и геймплея, работа со структурой игры и взаимодействие с командой  (⁎˃ᴗ˂⁎) \n\n"
        "Требования к геймдизайнеру:\n"
        "- Креативность\n"
        "- Логическое мышление \n"
        "- Умение четко объяснять свои идеи"
    ),
}

# Постоянная панель внизу
def get_reply_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("Как оставить заявку?")]],
        resize_keyboard=True,
        one_time_keyboard=False
    )

# Главное меню (Inline)
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("О проекте", callback_data="about")],
        [InlineKeyboardButton("Организатор", callback_data="org"),
         InlineKeyboardButton("Сценарист", callback_data="writer")],
        [InlineKeyboardButton("Нарративный дизайнер", callback_data="narrative")],
        [InlineKeyboardButton("Программист", callback_data="dev"),
         InlineKeyboardButton("Композитор", callback_data="composer")],
        [InlineKeyboardButton("Художники", callback_data="artist"),
         InlineKeyboardButton("Геймдизайнер", callback_data="gamedev")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Кнопка назад
def get_back_keyboard():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("« Назад", callback_data="main_menu")]]
    )

async def delete_previous_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет все сообщения бота из списка."""
    if "msg_ids" in context.user_data:
        chat_id = update.effective_chat.id
        for msg_id in context.user_data["msg_ids"]:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
        context.user_data["msg_ids"] = []

async def send_main_menu(chat_id, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню: 1 сообщение с картинкой и текстом (inline-кнопки)."""
    new_ids = []
    try:
        msg = await context.bot.send_photo(
            chat_id=chat_id,
            photo=open(MAIN_PHOTO, "rb"),
            caption=WELCOME_TEXT,
            reply_markup=get_main_keyboard()
        )
        new_ids.append(msg.message_id)
    except FileNotFoundError:
        msg = await context.bot.send_message(
            chat_id=chat_id,
            text=WELCOME_TEXT,
            reply_markup=get_main_keyboard()
        )
        new_ids.append(msg.message_id)

    context.user_data["msg_ids"] = new_ids

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await delete_previous_messages(update, context)

    # Сразу включаем реплай-клавиатуру с кнопкой "Как оставить заявку?"
    await update.message.reply_text(
        "«The Universe Is Crying for Us»\n Это чисто информационный бот! Писать сюда ничего не нужно (сообщения не дойдут)",
        reply_markup=get_reply_keyboard()
    )

    # И отправляем главное меню (фото + текст + inline-кнопки)
    await send_main_menu(update.effective_chat.id, context)

async def apply_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопки из нижней панели - заявка в одном сообщении (картинка+текст)."""
    try:
        await update.message.delete()
    except:
        pass

    await delete_previous_messages(update, context)
    await asyncio.sleep(0.1)

    new_ids = []
    try:
        msg = await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open(ZAYAVKA_PHOTO, "rb"),
            caption=APPLY_TEXT,
            reply_markup=get_back_keyboard()
        )
        new_ids.append(msg.message_id)
    except FileNotFoundError:
        msg = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=APPLY_TEXT,
            reply_markup=get_back_keyboard()
        )
        new_ids.append(msg.message_id)

    context.user_data["msg_ids"] = new_ids

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await delete_previous_messages(update, context)
    await asyncio.sleep(0.2)

    chat_id = query.message.chat.id

    if query.data == "main_menu":
        await send_main_menu(chat_id, context)

    elif query.data == "about":
        # О ПРОЕКТЕ: отдельное сообщение-картинка, потом отдельное сообщение-текст
        new_ids = []

        # 1. Картинка
        try:
            msg_photo = await context.bot.send_photo(
                chat_id=chat_id,
                photo=open(ABOUT_PHOTO, "rb")
            )
            new_ids.append(msg_photo.message_id)
        except FileNotFoundError:
            # если нет картинки - просто пропускаем этот шаг
            pass

        # 2. Текст с кнопкой "Назад"
        msg_text = await context.bot.send_message(
            chat_id=chat_id,
            text=ABOUT_TEXT,
            reply_markup=get_back_keyboard()
        )
        new_ids.append(msg_text.message_id)

        context.user_data["msg_ids"] = new_ids

    elif query.data in BUTTON_DATA:
        photo_path, text = BUTTON_DATA[query.data]
        new_ids = []
        try:
            msg = await context.bot.send_photo(
                chat_id=chat_id,
                photo=open(photo_path, "rb"),
                caption=text,
                reply_markup=get_back_keyboard()
            )
            new_ids.append(msg.message_id)
        except FileNotFoundError:
            msg = await context.bot.send_message(
                chat_id=chat_id,
                text=f"[Файл не найден]\n\n{text}",
                reply_markup=get_back_keyboard()
            )
            new_ids.append(msg.message_id)
        context.user_data["msg_ids"] = new_ids

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, apply_info))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()