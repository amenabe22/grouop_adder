import csv
import json
import sys
from telethon import TelegramClient, sync
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from pprint import pprint
import pandas as pd

folder_session = "session/"
_accounts = json.load(open("conf.json"))["accounts"]

ACCINDEX = 0
for acc in range(len(_accounts)):
    phone = _accounts[acc]["phone"]
    api_id = _accounts[acc]["api_id"]
    api_hash = _accounts[acc]["api_hash"]
    print("=" * 100)
    print("[{}] Phone => {}".format(acc, phone))
    print("=" * 100)

accIndex = int(input("Choose an account: "))
print(accIndex)
try:
    account = _accounts[accIndex]

    client = TelegramClient(
        folder_session + account["phone"], account["api_id"], account["api_hash"]
    ).start()
    client.connect()

    chats = []
    last_date = None
    chunk_size = 200
    groups = []

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
        groups.append(chat)
    par = []
    print("\nChoose a group you wanna scrape from: ")
    for p in range(len(groups)):
        print("[{}] {}".format(p, groups[p].title))
        # if p.title == "Freelance Ethiopia Group":
        #     par.append(p)
        #     print(p.access_hash)
        #     print(p.title, "==>", p)
    try:
        grp_idx = int(input("[+] Choose the group you want: "))
        print(grp_idx)
        # print(client.get_participants(groups[grp_idx]))
        all_p = client.get_participants(groups[grp_idx])
        # print(all_p)
        with open(
            "scraped_data/{}.csv".format(groups[grp_idx].title), "w", encoding="UTF-8"
        ) as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(
                ["username", "user_id", "access_hash", "name", "group", "group_id"]
            )
            print("+" * 200)
            print(len(all_p))
            for x in all_p:
                if x.username:
                    username = x.username
                else:
                    username = ""
                if x.first_name:
                    first_name = x.first_name
                else:
                    first_name = ""
                if x.last_name:
                    last_name = x.last_name
                else:
                    last_name = ""
                name = (first_name + " " + last_name).strip()
                writer.writerow(
                    [
                        username,
                        x.id,
                        x.access_hash,
                        name,
                        groups[grp_idx].title,
                        groups[grp_idx].id,
                    ]
                )
        print("Members scraped successfully.")
    except Exception as e:
        print(e, "!" * 20)

except Exception as e:
    print(e, "#" * 20)
    print("account not found")
    sys.exit(0)

client = TelegramClient(folder_session + phone, api_id, api_hash).start()
