#!/usr/bin/python3
import json

groups = {}

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
    readJson()
    print("enter <group> <add/remove> <user>")
    command = input()[1:].split()



    if len(command) != 3 :
        if len(command) == 1 and command[0] in groups:
            for users in groups[command[0]]
                print(user)
            return
        print("Wrong syntacommand. Do this: <group> <add/remove> <user>")
        return
    if command[1] != "add" and  command[1] != "remove":
        print("Wrong syntacommand. Use add or remove")
        return
    if command[0] not in groups:
        print("Group not found")
        return


    if command[1] =="add":
        print("adding...")
        add(command[0], command[2])
    if command[1] =="remove":
        print("removing...")
        remove(command[0], command[2])

    #add(command[0],command[1])
    #print(groups)

    #remove(command[0],command[1])
    #print(groups)

main()
