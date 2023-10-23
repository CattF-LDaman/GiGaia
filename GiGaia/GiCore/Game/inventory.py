from GiGaia.GiCore.Data.datatypes import DATATYPE_NAMETYPES

class Inventory:

    def __init__(self, assets):
        
        self.assets = assets
        self.items_data = self.assets.data.Items.__dict__
        self.containers_data = self.assets.data.Containers.__dict__

        self.containers = {}
        self.contents = {}

    def add_dict(self, d):
        for container, items in d.items():
            self.add_container(container)
            for item in items:
                self.add_item(container, item['item_id'], item['amount'], item['data'][1] if type(item['data']) == tuple else item['data'])

    def as_dict(self):
        inv_dict = {}
        for container, items in self.contents.items():
            inv_dict[container] = []
            for item in items:
                inv_dict[container].append(item.as_dict())
        return inv_dict

    def add_container(self, container):
        if container not in self.containers_data:
            raise ValueError(f"Container '{container} doesn't exist")
        if container not in self.containers:
            self.contents[container] = []
        self.containers[container] = self.containers_data[container]

    def container_size(self, container):
        return sum(i.amount for i in self.contents[container])

    def has_space(self, container, add_amount=0):
        if container not in self.containers:
            return False
        return self.container_size(container)+add_amount < self.containers[container]["capacity"]
        
    def item_exists(self, container, item_id, data=None, not_full=False, ignores=()):
        for i in self.contents[container]:
            if i not in ignores and i.match(item_id, data):
                if not_full and i.amount == i.STACK_SIZE:
                    continue
                return i
        return False

    def get_item(self, container, item_id, data=None, not_full=False, raise_error=True, ignores=()):
        
        if not (found_item:= self.item_exists(container, item_id, data, not_full, ignores)):
            if raise_error:
                raise ValueError(f"{container.capitalize()} doesn't have any '{item_id}'")

        return found_item

    def get_all_of(self, item_id, data=None):

        found = []
        for container in self.contents.values():
            for item in container:
                if item.match(item_id, data):
                    found.append(item)
        return found

    def get_amount_of(self, item_id, data=None):

        return sum(item.amount for item in self.get_all_of(item_id, data))

    def create_item(self, container, item_id, amount=1, data=None):

        self.contents[container].append((item_instance := Item(self, item_id, amount, data)))
        return item_instance

    def has_item(self, item_id, data=None, amount=1):
        
        return self.get_amount_of(item_id, data) > amount

    def add_item(self, container, item_id, amount=1, data=None):

        if not self.has_space(container):
            raise ValueError(f"Not enough space to store {amount} more item(s)")
        
        if not self.item_exists(container, item_id, data):
            self.create_item(container, item_id, amount, data)
            return
        
        left = amount

        while left:
            item_instance = self.get_item(container, item_id, data, not_full=True, raise_error=False)
            if not item_instance:
                item_instance = self.create_item(container, item_id, amount=0, data=data)
            left = item_instance.add_amount(left)

class Item:

    RARITIES = ["Trash", "Common", "Rare", "Epic", "Legendary", "Godlike"]
    RARITY_COLORS = [(198, 140, 83), (171, 171, 171), (71, 117, 209), (0, 255, 204), (255, 153, 0), (255, 51, 0)]
    DEFAULT = {
        "name": "Air",
        "description": "?",
        "type": "generic", # Determines behaviour,
        "rarity": 1,
        "data": {},
        "datatypes": {}
    }

    def __init__(self, inventory, item_id, amount=1, data=None):

        if not data:
            data = {}

        self.item_data = {**Item.DEFAULT, **inventory.items_data[item_id]}
        if not self.item_data["data"]:
            self.item_data["data"] = {}
        if not self.item_data["datatypes"]:
            self.item_data["datatypes"] = {}

        self.inventory = self.inv = inventory
        self.amount = amount

        # self.data = {**self.item_data["data"], **data}
        # self.DATATYPES = {k:DATATYPE_NAMETYPES[v] for k,v in self.item_data["datatypes"].items()}

        self.DATATYPES, self.data = Item.get_datastruc(inventory, item_id, data)

        self.ID = item_id
        self.NAME = self.item_data["name"]
        self.STACK_SIZE = self.item_data["stack_size"]
        self.DESCRIPTION = self.item_data["description"]
        self.RARITY = self.RARITIES[self.item_data["rarity"]]
        self.RARITY_COLOR = self.RARITY_COLORS[self.item_data["rarity"]]

    def as_dict(self):
        return {'item_id':self.ID, 'amount':self.amount, 'data':(self.DATATYPES, self.data)}

    @staticmethod
    def get_datastruc(inventory, item_id, data):
        item_data = {**Item.DEFAULT, **inventory.items_data[item_id]}

        data = {**item_data["data"], **data}
        datatypes = {k:DATATYPE_NAMETYPES[v] for k,v in item_data["datatypes"].items()}
        datastruc = tuple((dataname, datatype, 8) for dataname, datatype in datatypes.items())

        return datastruc, data

    def add_amount(self, amount):
        left = 0
        if self.amount+amount > self.STACK_SIZE:
            left = amount - (self.STACK_SIZE - self.amount)
            self.amount = self.STACK_SIZE
        else:
            self.amount += amount
        return left

    def match(self, item_id, data=None):
        idata = {**self.item_data["data"], **(data if data else {})}
        if self.ID == item_id and self.data == idata:
                return True
        return False
