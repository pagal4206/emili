import os
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from bson.objectid import ObjectId
from Emilia import custom_filter, BOT_NAME, TOKEN, SUPPORT_CHAT, UPDATE_CHANNEL, START_PIC
from Emilia.anime.bot import get_anime, get_recommendations, auth_link_cmd, logout_cmd, get_additional_info, code_cmd, help_
from Emilia.pyro.connection.connect import connectRedirect
from Emilia.pyro.greetings.captcha.button_captcha import buttonCaptchaRedirect
from Emilia.pyro.greetings.captcha.text_captcha import textCaptchaRedirect
from Emilia.pyro.notes.private_notes import note_redirect
from Emilia.pyro.rules.rules import rulesRedirect
from Emilia.utils.decorators import leavemute, rate_limit, RATE_LIMIT_GENERAL
from Emilia.utils.helper import AUTH_USERS, get_btns
from Emilia.mongo.users_mongo import add_user, add_chat

START_TEXT = """
Welcome to [{} :3]({})

This bot give varieties of features such as
➩ Group Management
➩ Spammer Protection
➩ Fun like chatbot
➩ Ranking, AI System
➩ Anime Loaded Modules
➩ Inline Games

Use the buttons below or /help to checkout even more!
"""

async def handle_private_start(client, message: Message):
    start_pic_url = START_PIC
    buttons = [
        [InlineKeyboardButton("Help", callback_data="help_back")],
        [
            InlineKeyboardButton("Support", url=f"https://t.me/{SUPPORT_CHAT}"),
            InlineKeyboardButton("News", url=f"https://t.me/{UPDATE_CHANNEL}"),
        ],
    ]
    await message.reply_text(
        START_TEXT.format(BOT_NAME, start_pic_url),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=False,
    )

async def handle_group_start(client, message: Message):
    await message.reply("Hey there, ping me in my PM to get help!")

async def handle_deep_link(client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        payload = message.text.split(maxsplit=1)[1]
    except IndexError:
        return
    args = payload.split("_")
    query = args[0]
    if query == "captcha":
        await buttonCaptchaRedirect(client, message)
        await textCaptchaRedirect(client, message)
    elif query == "note":
        await note_redirect(client, message)
    elif query == "connect":
        await connectRedirect(client, message)
    elif query == "rules":
        await rulesRedirect(message, client)
    elif query == "anihelp":
        await help_(client, message)
    elif query == "auth":
        await auth_link_cmd(client, message)
    elif query == "logout":
        await logout_cmd(client, message)
    elif query == "code":
        if not os.environ.get("ANILIST_REDIRECT_URL"):
            return
        try:
            token_id = payload.split("_", 1)[1]
            k = await AUTH_USERS.find_one({"_id": ObjectId(token_id)})
            if k:
                await code_cmd(k["code"], message)
        except (IndexError, KeyError):
            pass
    elif query == "des":
        if len(args) >= 3:
            req = args[3] if len(args) > 3 else "desc"
            anime_id = args[2]
            name = args[1]
            pic, result = await get_additional_info(anime_id, name, req)
            await client.send_photo(chat_id, pic)
            clean_result = result.replace("~!", "").replace("!~", "") if result else "No description available!!!"
            try:
                await client.send_message(chat_id, clean_result)
            except Exception:
                await client.send_message(chat_id, "No description available!!!")
    elif query == "anime":
        if len(args) >= 2:
            anime_id = int(args[1])
            auth = bool(await AUTH_USERS.find_one({"id": user_id}))
            result = await get_anime({"id": anime_id}, user=user_id, auth=auth)
            pic, msg = result[0], result[1]
            buttons = get_btns("ANIME", result=result, user=user_id, auth=auth)
            await client.send_photo(chat_id, pic, caption=msg, reply_markup=buttons)
    elif query == "anirec":
        if len(args) >= 2:
            result = await get_recommendations(args[1])
            await client.send_message(user_id, result, disable_web_page_preview=True)

@Client.on_message(custom_filter.command(commands="start"))
@leavemute
@rate_limit(RATE_LIMIT_GENERAL)
async def start_command(client, message: Message):
    if len(message.text.split()) > 1:
        await handle_deep_link(client, message)
    else:
        if message.chat.type == ChatType.PRIVATE:
            await handle_private_start(client, message)
        else:
            await handle_group_start(client, message)
