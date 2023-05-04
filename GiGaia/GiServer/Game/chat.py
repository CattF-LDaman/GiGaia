
class Chat:

    def __init__(self, game):
        
        self.game = game
        self.traffic = game.traffic

    def broadcast_chat(self, username, chat_msg):

        self.traffic.broadcast("SC_CHAT", {'user':username, 'content':chat_msg})
        self.game.log(f"CHAT <{username}> {chat_msg}")

    def handle_chat(self, player, chat):  # When a chat is received

        if chat.content.startswith("/"):
            self.game.server.terminal.parse(chat.content[1:], player)
        else:
            self.broadcast_chat(player.name, chat.content)