#/usr/bin/env python3
import sys
import requests
import json

server = "http://localhost:8888"
user = "<username_for_logging>"


def help():
    print("Daddy Tops Command Line Tool")
    print()
    print("Current Configuration")
    print("Server: " + server)
    print("User: " + user)
    print()
    print("OPTIONS:")
    print("NEW ACTION:              action: <target_hostname>: <mode>: <arguments>")
    print("NEW GROUP ACTION:        gaction: <target_groupname>: <mode>: <arguments>")
    print("SHOW ACTION RESULT:      show: result: <actionid>")
    print("SHOW TABLE INFO:         show: <table>")
    print("                           -table options: 'bots', 'hosts', 'actions', 'groups', 'db'")
    return

def newAction(args):
    try:
        args = args.split(":", 4)
        target = args[1].strip()
        mode = args[2].strip()
        argum = args[3].strip()
    except:
        print("Invalid syntax...")
        help()
        return
    opt = ""
    header = {'Content-type': 'application/json'}
    data = {"hostname": target, "mode": mode, "arguments": argum, "options": opt, "dtuser": user}
    request = requests.post(server + "/add/command/single", headers=header, data=json.dumps(data))
    if request.text == "success":
        print("SUCCESS! " + mode + " action queued for host: " + target)
    else:
        print(request.text)
    return

def newGroupAction(args):
    try:
        args = args.split(":", 4)
        target = args[1].strip()
        mode = args[2].strip()
        argum = args[3].strip()
    except:
        print("Invalid syntax...")
        help()
        return
    opt = ""
    header = {'Content-type': 'application/json'}
    data = {"groupname": target, "mode": mode, "arguments": argum, "options": opt, "dtuser": user}
    request = requests.post(server + "/add/command/group", headers=header, data=json.dumps(data))
    if request.text == "success":
        print("SUCCESS! " + mode + " action queued for group: " + target)
    else:
        print(request.text)
    return


def listObj(args):
    try:
        args = args.split(":", 3)
        obj = args[1].strip()
    except:
        print("Invalid syntax...")
        help()
        return
    if obj.lower() not in ["bots", "hosts", "actions", "groups", "db", "database", "result"]:
        print("Unknown object: " + obj + "...")
        print("Options are (not case-sens): bots, hosts, actions, groups, db, result")
        help()
        return
    if "result" not in obj:
        url = server + "/list/" + obj
        request = requests.get(url)
        print(request.text)
        return
    else:
        try:
            aid = args[2].strip()
        except:
            print("show: result requires actionid...")
            print("EXAMPLE: `show: result: 45`")
            return
        header = {'Content-type': 'application/json'}
        data = {"actionid": aid}
        request = requests.post(server + "/get/actionresult", headers=header, data=json.dumps(data))
        print(request.text)
        return


if __name__ == "__main__":
    # Show the help if we need
    if len(sys.argv) < 2:
        help()
    else:
        args = " ".join(sys.argv[1:])
        if args.startswith("action:"):
            newAction(args)
        elif args.startswith("gaction:"):
            newGroupAction(args)
        elif args.startswith("show:"):
            listObj(args)
        else:
            help()