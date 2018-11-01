#!/usr/bin/python3
import socket
import json
import getpass

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net" # Server
#channel = "#bot-test-bk" # Channel
channel = "#tihlde-drift" # Channel
botnick = "mentionbot" # Your bots nick
adminname = "bjornkpu" #Your IRC nickname
exitcode = "bye " + botnick

groups = {} # For managing users in groups

ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) #We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # assign the nick to the bot

def joinchan(chan): # join channel(s).
    pw = getpass.getpass("Password for " + chan + ": ")
    ircsock.send(bytes("JOIN "+ chan + " " + pw + "\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def ping(): # respond to server Pings.
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target=channel): # sends messages to the target.
    ircsock.send(bytes("NOTICE "+ target +" :"+ msg +"\n", "UTF-8"))

def readJson():
    with open("data_file.json", "r") as read_file:
        global groups
        groups = json.load(read_file)

def writeJson():
    with open("data_file.json", "w") as write_file:
        global groups
        json.dump(groups, write_file)

def add(group, users):
    for user in users:
        if user not in groups.get(group):
            groups.get(group).append(user)
    writeJson()

def remove(group, users):
    for user in users:
        while user in groups.get(group):
            groups.get(group).remove(user)
    writeJson()

def addGroup(groupList):
    for group in groupList:
        if group not in groups:
            groups[group] = []
    writeJson()

def removeGroup(groupList):
    for group in groupList:
        while group in groups:
            groups.pop(group)
    writeJson()

def main():
    joinchan(channel)
    readJson()
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if ircmsg.find('PING :') == -1: print(ircmsg)

        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
            target = ircmsg.split('PRIVMSG',1)[1].split(':',1)[0].strip()
            if target == botnick: target = name

            if len(name) < 17:

                # Hi answer
                if message.lower().find('hi ' + botnick.lower()) != -1:
                    sendmsg("Hello " + name + "!", target)

                # Group management
                if message.find('@') != -1:
                    group = message.split('@',1)[1].split(' ',1)[0].strip().lower()

                    # Help
                    if group == botnick:
                        sendmsg("@" + botnick + "         - Help.",target)
                        sendmsg("@groups          - List groups.",target)
                        sendmsg("@<group> <add/remove> <nick [nick2]...>  - Add/remove a given nicks.",target)
                        sendmsg("@group <add/remove> <groupname [groupname2]...>   - Add/remove given groups",target)
                        sendmsg("PS: I can be configured in private chat",target)

                    # List groups
                    if group == "groups": sendmsg(' '.join(groups),target)

                    # list nicks in group
                    elif group in groups:
                        if message.find('@' + group + ' add') == -1 and message.find('@' + group + ' remove') == -1:
                            sendmsg(' '.join(groups[group]), target)

                    # Add/remove nicks to/from group
                        if message.find('@' + group + ' add') != -1:
                            users = message.split('add',1)[1].strip().split(' ')
                            add(group, users)

                        if message.find('@' + group + ' remove') != -1:
                            users = message.split('remove',1)[1].strip().split(' ')
                            remove(group, users)

                    # Add/remove groups
                    if group == "group":
                        if message.find('@' + group + ' add') != -1:
                            groupList = message.split('add',1)[1].strip().split(' ')
                            addGroup(groupList)

                        if message.find('@' + group + ' remove') != -1:
                            groupList = message.split('remove',1)[1].strip().split(' ')
                            removeGroup(groupList)

                # Quit bot
                if name.lower() == adminname.lower() and message.rstrip() == exitcode:
                    sendmsg("oh...okay. :'(",target)
                    ircsock.send(bytes("QUIT \n", "UTF-8"))
                    return

        else:
            if ircmsg.find("PING :") != -1:
                ping()

main()
