class Adventurer:
    """
    Class for representing an adventurer.
    
    Attributes:
        name: (str) the name of the adventurer
        bag: (Bag) the adventuer's bag
        cash: (int) the amount of cash the adventurer is 
            carrying
    """

    def __init__(self, name, bag, cash):
        self.name = name
        self.bag = bag
        self.cash = cash


class Bag:
    """
    Class for representing an adventurer's bag.
    
    Attributes:
        material: (str) the material the bag is made from
        price: (int) the price of the bag
    
    Methods:
        add_item(item):
            adds an item to the bag
        get_visible_items(): list of Item
            returns the visible items in the bag
        get_total_value(): integer
            computes the total value of the items in the bag
    """
    
    def __init__(self, material, price):
        self.material = material
        self.price = price
        self.__items = []
    
    def add_item(self, item):
        """
        Adds an item to the bag.
        
        Input:
            item: an Item object
        
        Returns: nothing
        """

        self.__items.append(item)

    def get_visible_items(self):
        """
        Returns the sublist of items that are visible.

        Inputs: none

        Returns: list of Item objects
        """

        return [item for item in self.__items if item.is_visible]

    def get_total_value(self):
        """
        Computes the total value of the bag and its contents,
        including the price of the bag, and the price of all
        items in the bag (even invisible items).

        Inputs: none

        Returns: integer
        """

        return self.price + sum([item.price for item in self.__items])


class Item:
    """
    Class for representing an item an adventurer can own.
    
    Attributes:
        name: (str) the name of the item
        price: (int) the price of the item
        is_visible: (bool) whether the item is visible
    """

    def __init__(self, name, price, is_visible):
        self.name = name
        self.price = price
        self.is_visible = is_visible

def stop_at_customs(adventurers, max_value, banned):
    """
    Given a list of customers, return the sublist of the
    adventurers who are stopped for failing the customs check.
    To pass the customs check, an adventurer must not be
    carrying more than max_value in value (including cash and 
    the value of their bag, counting the price of the bag
    itself and all the items in it, even invisible items), and
    none of the *visible* items in their bag can be in the set
    of banned items.

    Inputs:
        adventurers: list of Adventurer objects
        max_value: (int) maximum allowed value of goods
        banned: (set of strings) the names of the banned items
    
    Returns: list of Adventurer objects
    """
  
    stopped = []

    for adventurer in adventurers:
        item_bag_value = adventurer.bag.get_total_value()
        cash = adventurer.cash
        total_value = item_bag_value + cash

        if total_value >= max_value:
            stopped.append(adventurer)

        visible_items = adventurer.bag.get_visible_items()
        for item in visible_items:
            if item in banned:
                stopped.append(adventurer)
    
    return stopped
        


