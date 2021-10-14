#!/usr/bin/env python3
from pathlib import Path
import json
import irc.bot
import irc.strings
import requests
import urllib.parse
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

config = None

# a simple struct like object
# just holds some variables
class Config:
    def __init__(self):
        self.port = 8089
        self.server = ''
        self.username = ''
        self.password = ''
        self.channel = ''
        self.admins = []
        self.sudoku_base = ''


class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, config):
        self.admins = config.admins
        irc.bot.SingleServerIRCBot.__init__(self, [(config.server, config.port, config.password)], config.username, config.username)
        self.channel = config.channel
        self.config = config

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        print("Joining", self.channel)
        c.join(self.channel)

    def on_privmsg(self, c, e):
        a = e.arguments[0].split(" ")
        print("Message", a)
        self.do_command(e, a[0].strip(), a[1:])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(" ")
        print("Message", a)
        self.do_command(e, a[0].strip(), a[1:])
        return

    def is_admin(self, nick):
        return nick in self.admins

    def match_y(self, y):
        mapper = {'a': '0', 'b': '1', 'c': '2', 'd': '3', 'e': '4', 'f': '5', 'g': '6', 'h': '7', 'i': '8'}
        if y.lower() in mapper:
            return mapper[y.lower()]
        else:
            return y

    def match_x(self, x):
        if ord(x) >= ord('1') and ord(x) <= ord('9'):
            return chr(ord(x)-1)
        else:
            return x

    def do_command(self, e, cmd, args=[]):
        nick = e.source.nick
        c = self.connection

        if cmd == "!disconnect" and self.is_admin(nick):
            self.disconnect()
        elif cmd == "!die" and self.is_admin(nick):
            self.die()
        elif cmd == "!stats" and self.is_admin(nick):
            for chname, chobj in self.channels.items():
                c.privmsg(self.channel, "--- Channel statistics ---")
                c.privmsg(self.channel, "Channel: " + chname)
                users = sorted(chobj.users())
                c.privmsg(self.channel, "Users: " + ", ".join(users))
                opers = sorted(chobj.opers())
                c.privmsg(self.channel, "Opers: " + ", ".join(opers))
                voiced = sorted(chobj.voiced())
                c.privmsg(self.channel, "Voiced: " + ", ".join(voiced))
        elif cmd == "!help":
            c.privmsg(self.channel, "Valid commands are: !put <1-9> <A-I> <1-9>, !next, !help")
        elif cmd == "!put":
            if len(args) < 3:
                c.privmsg(self.channel, "Usage: !put <1-9> <A-I> <1-9>")
            else:
                res = requests.get(self.config.sudoku_base
                + '/put?x=' + urllib.parse.quote(self.match_x(args[0]))
                + '&y=' + urllib.parse.quote(self.match_y(args[1]))
                + '&n=' + urllib.parse.quote(args[2]))
                parsed = res.json()
                if parsed == 'bad_request':
                    c.privmsg(self.channel, "Usage: !put <1-9> <A-I> <1-9>")
                elif parsed == 'bad_input':
                    c.privmsg(self.channel, ":(")
                else:
                    c.privmsg(self.channel, ":)")
        elif cmd == "!reset" and self.is_admin(nick):
            requests.get(self.config.sudoku_base + '/next')
            c.privmsg(self.channel, "Generating...")

def init():
    config = Config()
    read_cfg(config)
    return config

def read_cfg(config):
    # create config path
    Path('./config/').mkdir(parents=True, exist_ok=True)
    config_path = Path('./config/bot.json')
    if not Path.exists(config_path):
        return

    contents = Path(config_path).read_text()
    parsed = json.loads(contents)
    config.port = parsed['port']
    config.server = parsed['server']
    config.username = parsed['username']
    config.password = parsed['password']
    config.channel = parsed['channel']
    config.admins = parsed['admins']
    config.sudoku_base = parsed['sudoku_base']

def main():
    global config
    config = init()
    bot = Bot(config)
    bot.start()


if __name__ == '__main__':
    main()

