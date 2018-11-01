ircmsg = ":bjornkpu!~weechat@blue.nerdvana.tihlde.org PRIVMSG #bot-test-bk :asd"
name = ircmsg.split('!',1)[0][1:]
message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
target = ircmsg.split('PRIVMSG',1)[1].split(':',1)[0].strip()
stop = "|"
print(name+stop)
print(message+stop)
print(target+stop)
