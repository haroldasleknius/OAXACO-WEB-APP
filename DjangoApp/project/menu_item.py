class menu_item:
    def __init__(self, item_name, price, description, alleriges, calories, item_type, photo):
        self.item_name = item_name
        self.price = price
        self.description = description
        self.allergies = alleriges
        self.calories = calories
        self.item_type = item_type
        self.photo = photo
    
    def get_name(self):
        return self.item_name

    def get_price(self):
        return self.price

    def get_description(self):
        return self.description
    
    def get_allergies(self):
        return self.allergies

    def get_calories(self):
        return self.calories
    
    def get_type(self):
        return self.item_type
    
    def get_photo(self):
        return self.photo