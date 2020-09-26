import os, sys, csv, time, traceback, json
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest


USEALL = True
chats = []
last_date = None
chunk_size = 200
groups = []
os.system("clear")
# api_id = 1928810
# api_hash = "41b4612d22c94ceb1a844376eee8b3a0"
# phone = "+251942762357"


def initGrpAdd(client, input_file, phone):
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input("Enter the code: "))

    users = []
    with open("scraped_data/" + input_file, encoding="UTF-8") as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user["username"] = row[0]
            user["id"] = int(row[1])
            user["access_hash"] = int(row[2])
            user["name"] = row[3]
            users.append(user)

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

    print("Choose a group to add members:")
    i = 0
    for group in groups:
        print(str(i) + "- " + group.title)
        i += 1
    print("\nChoose a group to add members \n")
    g_index = input("Enter a Number: ")
    target_group = groups[int(g_index)]

    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

    # mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

    print(len(users), "$" * 20)
    for user in users:
        try:
            # print("Adding {}".format(user["id"]))
            # if mode == 1:
            if user["username"] == "":
                # continue
                user_to_add = client.get_input_entity(user["username"])
            else:
                user_to_add = InputPeerUser(user["id"], user["access_hash"])
                # sys.exit("Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print("Waiting 10 Seconds...")
            time.sleep(10)
            print("Testing => %s <=" % str(user["username"]))
        except PeerFloodError:
            print(
                "Getting Flood Error from telegram. Script is stopping now. Please try again after some time."
            )
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
        except Exception as e:
            print(e)
            print("Error ADDING USER ")
            continue


def main():
    folder_session = "session/"
    scraped_users = os.listdir("scraped_data/")

    if len(scraped_users) <= 0:
        print(
            "you don't have any data scraped yet please run python3 accounts_scraper.py and scrape data: "
        )
    else:
        print("\nChoose a file from your scaped data: \n")
        for sc in range(len(scraped_users)):
            print("[{}] {}".format(sc, scraped_users[sc]))
        print()
        sc_idx = int(input())
        print("[*] SELECTED CSV FILE {}".format(scraped_users[sc_idx]))
        _accounts = json.load(open("conf.json"))["accounts"]

        for acc in range(len(_accounts)):
            phone = _accounts[acc]["phone"]
            api_id = _accounts[acc]["api_id"]
            api_hash = _accounts[acc]["api_hash"]
            print("=" * 100)
            print("[{}] Phone => {}".format(acc, phone))
            print("=" * 100)

        accIndex = input(
            "\nChoose an account: !!! ENTER ALL TO LOOP EVERY ACCOUNT !!! "
        )
        if accIndex.lower() == "all":
            USEALL = True
            print("USING ALL ACCOUNTS ......")
            for acc in range(len(_accounts)):
                phone = _accounts[acc]["phone"]
                api_id = _accounts[acc]["api_id"]
                api_hash = _accounts[acc]["api_hash"]
                client = TelegramClient(
                    folder_session + phone, api_id, api_hash
                ).start()
                client.connect()
                initGrpAdd(client, scraped_users[sc_idx], phone)
        else:
            try:
                accIndex = int(accIndex)
                print("[*] SELECTED ACCOUNT {}".format(_accounts[accIndex]))
                selected_account = _accounts[accIndex]
                client = TelegramClient(
                    folder_session + selected_account["phone"],
                    selected_account["api_id"],
                    selected_account["api_hash"],
                ).start()
                client.connect()
                initGrpAdd(client, scraped_users[sc_idx], selected_account["phone"])
            except Exception as e:
                print(e)
                print("please enter a correct number or enter ALL")
                sys.exit()


if __name__ == "__main__":
    main()