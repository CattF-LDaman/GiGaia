
from GiGaia.GiCore.Game.inventory import Inventory

class PlayerInventory(Inventory):

    def __init__(self, state):
        super().__init__(state.game.assets)

        self.state = state
        self.p = state.p

        self.p.subscribe("SC_ADD_CONTAINER", self.handle_add_container_packet)
        self.p.subscribe("SC_ADD_ITEM", self.handle_add_item_packet)
    
    def handle_add_container_packet(self, acp):

        self.add_container(acp.container)

    def handle_add_item_packet(self, aip):

        self.add_item(aip.container, aip.item_id, aip.amount, aip.data)
