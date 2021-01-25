# coding=utf-8
import json
import time

PLUGIN_METADATA = {
    'id': 'authme',
    'version': '0.0.1',
    'name': 'authme',  
    'author': 'otae',
        'dependencies': {
        'mcdreforged': '<1.0.0',
    }
}


json_filename = "config/authme_list.json"

Game_account = {

}

Login_queue = []



def on_player_joined(server, player):
    server.execute("effect give {} minecraft:slowness 1000000 255".format(player))
    server.execute("effect give {} minecraft:mining_fatigue 1000000 255".format(player))
    server.execute("effect give {} minecraft:blindness 1000000 255".format(player))
    if player in Game_account:
        server.tell(player,'输入"!!log [密码]"来登录')
        Login_queue.append(player)
    else:
        server.tell(player,'输入"!!reg [密码] [重复密码]"来注册')

        

def on_info(server,info):
    if info.content.startswith('!!log'):
        if info.player in Login_queue:
            password = info.content.split(" ")
            if len(password) == 2:
                if password[1] == Game_account[info.player]:
                    server.execute("effect clear {} minecraft:slowness".format(info.player))
                    server.execute("effect clear {} minecraft:mining_fatigue".format(info.player))
                    server.execute("effect clear {} minecraft:blindness".format(info.player))
                    server.tell(info.player,"登录成功")
                    password = ('')
                    Login_queue.remove(info.player)
                else:
                    server.tell(info.player,"密码错误")
            else:
                server.tell(info.player,"格式错误")
        else:
            server.tell(info.player,"你已经登陆过了")
    if info.content.startswith("!!reg"):
        if info.player in Game_account:
            server.tell(info.player,"你已经注册过了")
        else:
            args = info.content.split(' ')
            if len(args) == 3:
                if args[1] == args[2]:
                    Game_account[info.player] = args[2]
                    saveJson()
                    server.execute("effect clear {} minecraft:slowness".format(info.player))
                    server.execute("effect clear {} minecraft:mining_fatigue".format(info.player))
                    server.execute("effect clear {} minecraft:blindness".format(info.player))
                    server.tell(info.player,"注册成功，已自动登录")
                else:
                    server.tell(info.player,"请输入相同的密码")
            else:
                server.tell(info.player,"格式错误")



def on_load(server, old):
    global Game_account
    try:
        with open(json_filename) as f:
            Game_account = json.load(f, encoding='utf8')
    except:
        saveJson()


def on_unload(server):
    saveJson()

#保存json
def saveJson():
    with open(json_filename, 'w') as f:
        json.dump(Game_account, f, indent=4)
