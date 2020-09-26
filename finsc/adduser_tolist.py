import sys
import json
from pprint import pprint

FINDATA = None


def hasDup(st, ty):
    isDup = False
    if len(FINDATA["accounts"]) > 0:
        for i in FINDATA["accounts"]:
            if i[ty] == st:
                isDup = False
            else:
                isDup = True
    else:
        isDup = True
    return isDup


if __name__ == "__main__":
    with open("conf.json") as f:
        data = json.load(f)
        FINDATA = data

    phone = input("[+] Enter the phone number: ")
    api_id = int(input("[+] Enter API ID: "))
    api_hash = str(input("[+] Enter API hash: "))

    if not hasDup(phone, "phone"):
        print("phone number is already registerd please try again: ")
        sys.exit(0)
    elif not hasDup(api_id, "api_id"):
        print("api_id is already registerd please try again: ")
        sys.exit(0)
    elif not hasDup(api_hash, "api_hash"):
        print("api_hash is already registerd please try again: ")
        sys.exit(0)
    else:
        FINDATA["accounts"].append(
            {
                "phone": phone,
                "api_id": api_id,
                "api_hash": api_hash,
                "use": True,
            },
        )

        # pprint(FINDATA)
        with open("conf.json", "w") as f:
            json.dump(FINDATA, f)
