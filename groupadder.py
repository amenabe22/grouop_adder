"""
Author: Amen Abe
Title: Group Adder Bot
Date: Sunday, Sep 26/ 2020
Desription: bot to add random users to a group

HELp: Use /startinvite to get started
"""

import csv
import time
import logging
from aiogram import Bot, Dispatcher, executor, types
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest

API_TOKEN = ""

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

USEALL = True
chats = []
last_date = None
chunk_size = 200
groups = []
users = []


@dp.message_handler(commands=["startinvite"])
async def send_welcome(message: types.Message):
    api_id = ""  # your api id
    api_hash = ""  # your api hash
    phone = ""  # your phone

    client = TelegramClient("session_name", api_id, api_hash)
    await client.connect()
    with open("scraped_data/GetCoin.csv", encoding="UTF-8") as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user["username"] = row[0]
            user["id"] = int(row[1])
            user["access_hash"] = int(row[2])
            user["name"] = row[3]
            users.append(user)

    result = await client(
        GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0,
        )
    )
    chats.extend(result.chats)
    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    tgid = 0000  # your group ID
    tghash = 4123123871932  # your group hash
    target_group_entity = InputPeerChannel(tgid, tghash)
    max_usrs = 200  # max users you wanna add
    for user in users[:max_usrs]:
        try:
            if user["username"] == "":
                user_to_add = await client.get_input_entity(user["username"])
            else:
                user_to_add = InputPeerUser(user["id"], user["access_hash"])
                # sys.exit("Invalid Mode Selected. Please Try Again.")
            await client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print("Waiting 10 Seconds...")
            time.sleep(5)
            print("Testing => %s <=" % str(user["username"]))
        except PeerFloodError:
            print(
                "Getting Flood Error from telegram. Script is stopping now. Please try again after some time."
            )
            await message.reply("🌊 Getting Flood ERR Wait 🌊")
        except UserPrivacyRestrictedError:
            print(" The user's privacy settings do not allow you to do this. Skipping.")
            await message.reply(
                "🚫 The user's privacy settings do not allow you to do this. Skipping. 🚫"
            )
        except Exception as e:
            await message.reply(str(e))
            print(e)
            print("Error ADDING USER ")

    await message.reply("✅✅ FINISHED ADDING USERS TO GROUP ✅✅")


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    WElcome message handler
    """
    await message.reply(
        "Hi!\nI'm Group Adder use /startinvite to start adding users !\nPowered by aiogram."
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)