class Item:
    def __init__(self,
                 itemCooldown : int,
                 itemID : int,
                 itemStacks : int) -> None:
        self.itemCooldown = itemCooldown
        self.itemID = itemID
        self.itemStacks = itemStacks