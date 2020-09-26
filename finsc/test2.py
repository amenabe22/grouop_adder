from pprint import pprint
from telethon import TelegramClient, sync
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import pandas as pd

api_id = "1928810"
api_hash = "41b4612d22c94ceb1a844376eee8b3a0"
phone = "+251942762357"
# api_id = "1027637"
# api_hash = "da1df5c8b2e03ec778c97f7f74fc9649"
# phone = "+251911359586"

# Group name can be found in group link (Example group link : https://t.me/c0ban_global, group name = 'c0ban_global')
group_username = "GET_COIN_Ethiopia"
client = TelegramClient("session_name", api_id, api_hash).start()
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input("Enter the code"))

chats = []
groups = []
last_date = None
chunk_size = 200

result = client(
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
for x in groups:
    # if x.title == "Python ኢትዮጵያ":
    print("#" * 100)
    print(x.title, "==>", x.id, "===>", x.access_hash)
    # pprint(x.__dict__)
    print("#" * 100)
