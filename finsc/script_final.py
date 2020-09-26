import os
import sys
import csv
import time
import json
import traceback
import logging
from telethon.client import users
from telethon import TelegramClient, sync, events, connection
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, InputUser
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import FloodWaitError, PeerFloodError, UserPrivacyRestrictedError

# 1250391816
os.system("clear")
message = """
    ###################################################################################################
    # ############################################################################################### #
    # ################################ TELEGRAM GROUP ADDER ######################################### #
    # #################################################################################################
    # #################################################################################################
    """

print(message)
print()
print("Initiating group ADD")
print()
fialConf = open("conf.json", "r")
_fc = json.load(fialConf)

GRP_ID = _fc["group"]["group_id"]
GRP_ACCESS_HASH = int(_fc["group"]["group_hash"])
# -1046133482585014127
# GRP_ACCESS_HASH = 4964886362779661294
INPUT_FILE = "scraped_data/" + input("[+] Enter input csv filename: ")
# extract CSV file and return users data


def cleanCSVData(input_f):
    users = []
    with open(input_f, encoding="UTF-8") as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user["username"] = row[0]
            user["id"] = int(row[1])
            user["access_hash"] = row[2]
            user["name"] = row[3]
            users.append(user)

    return users


def setup_client(session_name, api_id, api_hash, phone):
    client = TelegramClient(session_name, api_id, api_hash).start()
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        return (client, False)
    with open("handled_sessions.json", "w") as f:
        json.dump({"session_name": session_name}, f)
    return (client, True)


def add_to_grp(client, mode="uname", data=None, uname=None, grid=None, grhash=None):
    try:
        if (uname is not None) and (mode == "uname"):
            user_to_add = client.get_input_entity(uname)
        # get user_to_add with hash not username
        elif (data is not None) and (mode == "hash"):
            user_to_add = InputPeerUser(data["uid"], int(data["uhash"]))

        target_group_entity = InputPeerChannel(grid, int(grhash))
        target_grp_ent = InputPeerChannel(grid, int(grhash))
        client(InviteToChannelRequest(target_grp_ent, [user_to_add]))
        return {"added": True}

    except PeerFloodError as e:
        print("Error Fooling cmnr")
        print("remove client: ")
        client.disconnect()
        # filter_clients.remove(current_client)
        return {"added": False}

    except UserPrivacyRestrictedError:
        print("Error Privacy")
    except Exception as e:
        print(e)
        return {"added": False}
        # print("Error other")
        # traceback.print_exc()
        # break

    # except Exception as e:
    #     print(e)


def initializeAdd(api_id, api_hash, phone, count):
    # TODO make sth unique as a session name everytime to persist data
    allsess = os.listdir("/home/anonny/scrapers/grpadder/sessions")
    session_name = "demesession"
    csvUsrs = cleanCSVData(INPUT_FILE)
    emptyUnames = []
    nonEmptyUnames = []
    initData = {}
    # slice only 10 for now
    for usrs in csvUsrs[: int(count)]:
        usrHashData = {"uid": usrs["id"], "uhash": usrs["access_hash"]}
        if usrs["username"] == "":
            usrHashData = {"uid": usrs["id"], "uhash": usrs["access_hash"]}
            emptyUnames.append(usrHashData)
        else:
            nonEmptyUnames.append(usrs["username"])
    initData["emptyunames"] = len(emptyUnames)
    initData["fullunames"] = len(nonEmptyUnames)
    usrAddedAlready = "This user was kicked from this supergroup/channel (caused by InviteToChannelRequest)"
    client, _ = setup_client(session_name, api_id, api_hash, phone)
    if _:
        if not (len(nonEmptyUnames) == 0):
            for un in nonEmptyUnames:
                gr = add_to_grp(
                    client,
                    mode="uname",
                    data=None,
                    uname=un,
                    grid=GRP_ID,
                    grhash=GRP_ACCESS_HASH,
                )
                if gr == usrAddedAlready:
                    print("User is already a member")
                else:
                    print(gr, "WITH USERNAME")
        if not (len(nonEmptyUnames) == 0):
            for hs in emptyUnames:
                gr = add_to_grp(
                    client,
                    mode="hash",
                    data=hs,
                    uname=None,
                    grid=GRP_ID,
                    grhash=GRP_ACCESS_HASH,
                )
                if gr == usrAddedAlready:
                    print("User is already a member")
                else:
                    print(gr, "WITH HASH")
        initData["err"] = False
        print("Empty usernames: {}".format(len(emptyUnames)))
        print("With usernames: {}".format(len(nonEmptyUnames)))
        print()

    elif not _:  # means that client is not authorized
        print("user authentication error")

        initData["err"] = True

    return initData


def add_group(client, count):
    print(client)
    csvUsrs = cleanCSVData(INPUT_FILE)
    emptyUnames = []
    nonEmptyUnames = []
    initData = {}
    # slice only 10 for now
    for usrs in csvUsrs[: int(count)]:
        usrHashData = {"uid": usrs["id"], "uhash": usrs["access_hash"]}
        if usrs["username"] == "":
            usrHashData = {"uid": usrs["id"], "uhash": usrs["access_hash"]}
            emptyUnames.append(usrHashData)
        else:
            nonEmptyUnames.append(usrs["username"])
    initData["emptyunames"] = len(emptyUnames)
    initData["fullunames"] = len(nonEmptyUnames)
    usrAddedAlready = "This user was kicked from this supergroup/channel (caused by InviteToChannelRequest)"
    # start adding users
    if not (len(nonEmptyUnames) == 0):
        for un in nonEmptyUnames:
            gr = add_to_grp(
                client,
                mode="uname",
                data=None,
                uname=un,
                grid=GRP_ID,
                grhash=GRP_ACCESS_HASH,
            )
            if gr == usrAddedAlready:
                print("User is already a member")
            else:
                print(gr, "WITH USERNAME")
    if not (len(nonEmptyUnames) == 0):
        for hs in emptyUnames:
            gr = add_to_grp(
                client,
                mode="hash",
                data=hs,
                uname=None,
                grid=GRP_ID,
                grhash=GRP_ACCESS_HASH,
            )
            if gr == usrAddedAlready:
                print("User is already a member")
            else:
                print(gr, "WITH HASH")


if __name__ == "__main__":
    with open("conf.json", "r") as f:
        config = json.loads(f.read())

        logging.basicConfig(level=logging.WARNING)

        accounts = config["accounts"]

        folder_session = "session/"

        for account in accounts:
            api_id = account["api_id"]
            api_hash = account["api_hash"]
            phone = account["phone"]
            if account["use"] == True:
                client = TelegramClient(folder_session + phone, api_id, api_hash)
                client.start()
                client.connect()
                if client.is_user_authorized():
                    print("Login success")
                else:
                    print("Login fail")
                client.disconnect()

    conf = open("conf.json", "r")
    _j = json.load(conf)

    for acc in _j["accounts"]:
        api_hash = acc["api_hash"]
        api_id = acc["api_id"]
        phone = acc["phone"]
        print(api_hash, api_id, phone)
        session_path = (
            "/home/anonny/scrapers/grpadder/finsc/session/" + phone + ".session"
        )
        client = TelegramClient(folder_session + phone, api_id, api_hash)
        client.connect()
        add_group(client, 10)
        # initializeAdd(api_id, api_hash, phone, 10)
