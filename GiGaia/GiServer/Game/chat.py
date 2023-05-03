
class Chat:

    def __init__(self, game):
        
        self.game = game
        self.traffic = game.traffic

    def handle_chat(self, player, chat):  # When a chat is received

        if chat.content.startswith("/"):
            self.game.server.terminal.parse(chat.content[1:], player)
        else:
            self.traffic.broadcast("SC_CHAT", {'user':player.name, 'content':chat.content})
            self.game.log(f"CHAT <{player.name}> {chat.content}")