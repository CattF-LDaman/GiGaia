
from GiGaia.GiCore.Game.inventory import Inventory, Item

class PlayerInventory(Inventory):

    def __init__(self, player):
        super().__init__(player.game.assets)

        self.player = player
        self.updates = {"add_item":[], "add_container":[]}

    def add_item(self, container, item_id, amount=1, data=None):
        if not data:
            data = {}
        super().add_item(container, item_id, amount, data)
        self.updates["add_item"].append((container, item_id, amount, data))

    def add_container(self, container):
        super().add_container(container)
        self.updates["add_container"].append(container)

    def update(self):

        while self.updates["add_container"]:
            container = self.updates["add_container"].pop()
            self.player.h.send("SC_ADD_CONTAINER",{"container":container})

        while self.updates["add_item"]:
            container, item_id, amount, data = self.updates["add_item"].pop()
            idata = Item.get_datastruc(self, item_id, data)
            self.player.h.send("SC_ADD_ITEM",{"container":container,"item_id":item_id,"amount":amount, "data":idata})


