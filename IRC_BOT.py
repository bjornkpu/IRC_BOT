#!/usr/bin/python3
import socket
import json

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net" # Server
channel = "#bot-test-bk" # Channel
botnick = "huleBOT" # Your bots nick
adminname = "bjornkpu" #Your IRC nickname
exitcode = "bye " + botnick

groups = {} # For managing users in groups

ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) #We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # assign the nick to the bot

def joinchan(chan): # join channel(s).
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def ping(): # respond to server Pings.
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target=channel): # sends messages to the target.
    ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

def readJson():
    with open("data_file.json", "r") as read_file:
        global groups
        groups = json.load(read_file)

def writeJson():
    with open("data_file.json", "w") as write_file:
        global groups
        json.dump(groups, write_file)

def add(group, user):
    groups.get(group).append(user)
    writeJson()

def remove(group, user):
    while user in groups.get(group):
        groups.get(group).remove(user)
        writeJson()

def main():
    joinchan(channel)
    readJson()
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]

            if len(name) < 17:

                # Hi answer
                if message.lower().find('hi ' + botnick.lower()) != -1:
                    sendmsg("Hello " + name + "!")

                # Send message for me
                if message[:5].find('.tell') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in the format of '.tell [target] [message]' to work properly."
                    sendmsg(message, target)

                # Group management
                #if message[:5].find('@groups') != -1:
                    #grouplist = ""
                    #for group in groups:

                if message[:5].find('@') != -1:
                    command = message.split(' ')
                    if len(command) == 1:
                        group = message[1:].split(' ',3)[0]
                        if group in groups:
                            userlist = ""
                            for user in groups[group]:
                                userlist += user + ":"
                            print(userlist)

                    if len(command) == 3 and message[1:].split(' ',3)[0] in groups:
                        if message.split(' ',3)[1].lower() == "add":
                            add(message[1:].split(' ',3)[0], message.split(' ',3)[2])

                        if message.split(' ',3)[1].lower() == "remove":
                            remove(message[1:].split(' ',3)[0], message.split(' ',3)[2])

                # Quit bot
                if name.lower() == adminname.lower() and message.rstrip() == exitcode:
                    sendmsg("oh...okay. :'(")
                    ircsock.send(bytes("QUIT \n", "UTF-8"))
                    return




        else:
            if ircmsg.find("PING :") != -1:
                ping()

main()
