from pymongo import MongoClient
from telethon import TelegramClient, events, functions
from os import getenv
import asyncio
from dotenv import load_dotenv



load_dotenv()

api_id = getenv('API_ID')
api_hash = getenv('API_HASH')
token = getenv('BOT_TOKEN')
url = getenv('MONGO_URI')

bot = TelegramClient("asst", api_id, api_hash).start(bot_token=token)
cli = MongoClient(url, tls=True, tlsAllowInvalidCertificates=True)
db = cli["cloud"]
client = db.chats
devs = 2107137268


def get_chat(chat_id: int):
    return client.find_one({"chat_id": chat_id})


def add_chat(chat_id: int, msg_id: int, link: str, backup_link: str, backup_chat_id: int, id: int):
    if get_chat(chat_id):
        return False
    client.insert_one({
        "id": id,
        "chat_id": chat_id,
        "msg_id": msg_id,
        "link": link,
        "backup_link": backup_link,
        "backup_chat_id": backup_chat_id
    })

def remove_chat(chat_id: int):
    client.delete_one({"chat_id": chat_id})

def get_link(chat_id: int):
    return get_chat(chat_id)["link"]

@bot.on(events.NewMessage(pattern="/add", from_users=devs))
async def add_(e):
    try:
        chat_id = e.chat_id
        msg_id = e.id
        backup_chat_id = e.raw_text.split(" ")[1]
        id = e.chat.title.split(" ")[-1]
        link = (await bot(functions.messages.ExportChatInviteRequest(int(chat_id)))).link
        backup_link = (await bot(functions.messages.ExportChatInviteRequest(int(backup_chat_id)))).link
        add_chat(chat_id, msg_id, link, backup_link, backup_chat_id, id)
        await e.reply("Added chat\nchat id : {}\nlink : {}\nbackup chat id : {}\nbackup link : {}\nid : {}".format(chat_id, link, backup_chat_id, backup_link, id))
    except Exception as a:
        await e.reply("Error : {}".format(a))
        

@bot.on(events.NewMessage(pattern="/remove", from_users=devs))
async def rm_chat(e):
    try:
        chat_id = e.chat_id
        remove_chat(chat_id)
        await e.reply("Removed")
    except Exception as e:
        await e.reply("Error : {}".format(e))

@bot.on(events.NewMessage(pattern="/link", from_users=devs))
async def get_link(e):
    try:
        chat_id = e.chat_id
        await e.reply(get_link(chat_id))
    except Exception as e:
        await e.reply("Error : {}".format(e))


@bot.on(events.NewMessage(pattern="/start"))
async def start(e):
    await e.reply("Hello")
    

async def start():
    await bot.send_message("tamilvip007", "Bot started")

print("Bot started")
asyncio.get_event_loop().run_until_complete(start())
bot.run_until_disconnected()
