from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import itchat
import json

app = Flask(__name__)
api = Api(app)


class TFRobot(Resource):
    def __init__(self):
        self.login()
        self.friend_list = itchat.get_friends()

    def login(self):
        itchat.auto_login(hotReload=True, enableCmdQR=2)

    def _get_username_by_NickName(self, name):
        for friend in self.friend_list:
            if friend['NickName'] == name:
                return friend['UserName']
        return None

    def _send_msg(self, msg, username):
        ret = itchat.send(msg, toUserName=username)
        return ret

    def send_msg_to_nickname(self, nickname, msg):
        userid = self._get_username_by_NickName(name=nickname)
        ret = self._send_msg(msg=msg, username=userid)
        return ret

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('msg', type=str)
        parser.add_argument('token', type=str)
        args = parser.parse_args()
        if args['token'] != 'tensorflow':
            abort(404, message="require token")
        else:
            print('Receiving message!')
            req = self.send_msg_to_nickname(nickname=args['name'], msg=args['msg'])
            print('Done!')
            return req 

api.add_resource(TFRobot, '/log')

if __name__ == '__main__':
    app.run('0.0.0.0', port=80)
