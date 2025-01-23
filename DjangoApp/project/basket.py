from .db_service import database

class item:
    """ Class represents items stored within a basket.

    Attributes:
        name (str): Name of item being added to the basket.
        cost (float): Cost of each item.
        quantity (int): Quantity of the item in the basket.
    """
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.quantity = 1

class basket:
    """ Class represents the basket structure used to store items in the users basket.

    Attributes:
        database (con): Database connection.
        basket (hashmap): Used to store item objects.
    """
    def __init__(self):
        self.database = database()
        self.basket = {}

    def add_to_basket(self, item_id):
        """ Add to basket is used to add specific items to the basket.

        Args:
            item_id: Id of the item, used to get information about a specific item.
        """
        if item_id in self.basket:
            self.basket[item_id].quantity += 1
        else:
            item_information = self.database.get_item_name_from_id(item_id)
            self.basket[item_id] = item(item_information[1], item_information[2])

    def remove_from_basket(self, item_id):
        """ Add to basket is used to add specific items to the basket.

        Args:
            item_id: Id of the item, used to update the quantity of each item.
        """
        if self.basket[item_id].quantity == 1:
            del self.basket[item_id]
        else:
            self.basket[item_id].quantity -= 1
            
    def get_basket(self):
        """ Gets the entire hashmap containing all the items.

        Returns:
            The basket hashmap.
        """
        return self.basket

    def get_basket_value(self):
        """ Calculates the total value of all items within the hashmap.

        Returns:
            The value of all items in the basket with 2 decimal places.
        """
        total = 0
        for name in self.basket:
            item = self.basket[name]
            total += (item.cost*item.quantity)
        return "{0:.2f}".format(total)
    
    def clear_basket(self):
        self.basket = {}