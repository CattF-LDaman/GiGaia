
class Inventory:

    def __init__(self, assets):
        
        self.assets = assets
        self.items_data = self.assets.Items.__dict__
        self.containers_data = self.assets.Containers.__dict__

        self.containers = {}
        self.contents = {}

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
        return self.container_size(container)+add_amount < self.containers[container].capacity
        
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

    def __init__(self, inventory, itemid, amount=1, data=None):

        if not data:
            data = {}

        self.item_data = inventory.items_data[itemid]

        self.inventory = self.inv = inventory
        self.amount = amount

        self.data = {**self.item_data["data"], **data}

        self.ID = itemid
        self.STACK_SIZE = self.item_data["stack_size"]
        self.DESCRIPTION = self.item_data["description"]
        self.RARITY = self.RARITIES[self.item_data["rarity"]]

    def add_amount(self, amount):
        left = 0
        if self.amount+amount > self.STACK_SIZE:
            left = amount - (self.STACK_SIZE - self.amount)
            self.amount = self.STACK_SIZE
        return left

    def match(self, item_id, data=None):
        idata = {**self.items_data[item_id]["data"], **(data if data else {})}
        if self.ID == item_id and self.data == idata:
                return True
        return False
