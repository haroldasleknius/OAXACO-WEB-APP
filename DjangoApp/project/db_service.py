import psycopg2
from psycopg2 import Error
import os
from getpass import getpass
from .SaltHash import salting, hashingLocally

'''
Class is used to connect to the database and it provides a very simple location for 
the team to set up their database queries. The connection is established once a singleton 
instance of a class is created and it is shared throughout the whole program. Queries can 
be added to this class to easily query and return data from the database.
'''


class database:
    _instance = None
    connection = None

    def __new__(self):
        if self._instance is None:
            self._instance = super(database, self).__new__(self)
            self.connection = psycopg2.connect(
                user="group20",
                password="ahyieg",
                host="localhost",
                port=os.getenv('PORT'),
                database="CS2810/group20")
            self.server_information(self)
        return self._instance

    '''
    Print server information to ensure that the database connection has been established.
    '''

    def server_information(self):
        print(self.connection.get_dsn_parameters(), "\n")
        print("----- connection established -----")

    '''
    Close the database connection.
    '''

    def close_connection(self):
        print("----- database connection closed -----")
        self.connection.close()

    '''
    An example query for the team to use to learn the process of querying the database.
    '''
    def get_user_id(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = '{name}'".format(name=username))
        record = cursor.fetchall()
        cursor.close()
        return record
    
    def get_all_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        record = cursor.fetchall()
        cursor.close()
        return record

    #methods for 'tables'
    def get_assigned_tables(self, waiter):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT table_id, seats, clean, available, assistance, assigned FROM tables WHERE assigned='{waiter}' ORDER BY table_id ASC;")
        record = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return record
    
    def get_my_managed_tables(self, waiter):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT table_id, assigned FROM tables WHERE assigned='{waiter}';")
        record = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return record
    
    def get_unassigned_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT table_id, assigned FROM tables WHERE assigned IS NULL;")
        record = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return record
    
    def set_clean_table(self, waiter, table_num, status):
        with self.connection.cursor() as curs:
            curs.execute(f"UPDATE tables SET clean = '{status}' WHERE table_id = '{table_num}' AND assigned = '{waiter}';")
            self.connection.commit()
            curs.close()
    
    def set_available_table(self, waiter, table_num, status):    
        with self.connection.cursor() as curs:
            curs.execute(f"UPDATE tables SET available = '{status}' WHERE table_id = '{table_num}' AND assigned = '{waiter}';")
            self.connection.commit()
            curs.close()
    
    def set_assistance_table(self, waiter, table_num, status):
        with self.connection.cursor() as curs:
            curs.execute(f"UPDATE tables SET assistance = '{status}' WHERE table_id = '{table_num}' AND assigned = '{waiter}';")
            self.connection.commit()
            curs.close()
            
    def set_table_assignment(self, waiter, table_num, add_or_remove):
        with self.connection.cursor() as curs:
            if add_or_remove == "Add":
                curs.execute(f"UPDATE tables SET assigned = '{waiter}' WHERE table_id = '{table_num}' AND assigned IS NULL;")
            elif add_or_remove == "Remove":
                curs.execute(f"UPDATE tables SET assigned = NULL WHERE table_id = '{table_num}' AND assigned = '{waiter}';")
            self.connection.commit()
            curs.close()
    #end of 'tables' methods
    
    def get_login_users(self,username):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT password FROM users WHERE username = '{name}'".format(name=username))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record

    def add_new_menu_item(self, new):
        cursor = self.connection.cursor()
        sql = "INSERT INTO menu_items (item_name, price, description, allergies, calories, item_type, photo_name, stock) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (new.get_name(), new.get_price(), new.get_description(), new.get_allergies(), new.get_calories(), new.get_type(), new.get_photo(), 15)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.close()

    def get_menu_item_photo(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT photo_name FROM menu_items WHERE item_id = '" + id + "'")
        photo = []
        for row in cursor:
            for field in row:
                photo.append(field)
        self.connection.commit()
        cursor.close()
        return photo


    def get_menu_name(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT item_id, item_name  FROM menu_items")
        names = []
        for row in cursor:
            for field in row:
                names.append(field)
        self.connection.commit()
        cursor.close()
        return names

    def change_menu_item(self, id, name, thing):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE menu_items SET " + name + " = '" +
                       thing + "' WHERE item_id = '" + id + "'")
        self.connection.commit()
        cursor.close()

    def get_menu_item(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM menu_items WHERE item_id = '" + id + "'")
        item = []
        for row in cursor:
            for field in row:
                item.append(field)
        self.connection.commit()
        cursor.close()
        return item

    def delete_menu_item(self, id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM menu_items WHERE item_id = '" + id + "'")
        self.connection.commit()
        cursor.close()

    '''
    Send a new order to the database which a customer has payed for.
    '''

    def submit_order(self, basket,user_id):
        cursor = self.connection.cursor()
        sql = "INSERT INTO sales (user_id, total_expense, status) VALUES (%s, %s, %s)"
        val = (user_id, basket.get_basket_value(), 1)
        cursor.execute(sql, val)
        self.connection.commit()
        cursor.execute("SELECT * FROM sales")
        # Get the sale id so that we can add all the items within the order to the order table.
        sale_id = cursor.fetchall()[-1][0]
        sql = "INSERT INTO orders (sale_id, item_id, time_elapsed, quantity) VALUES (%s, %s, %s, %s)"
        basket = basket.get_basket()
        for item_id in basket:
            val = (sale_id, item_id, "08:00:00", basket[item_id].quantity)
            cursor.execute(sql, val)
            self.connection.commit()
        for item_id in basket:
            cursor.execute("UPDATE menu_items SET stock=stock-%s WHERE item_id=%s;", (basket[item_id].quantity, item_id))
        cursor.close()
        return sale_id

    '''
    Fetch all the menu items from the database so that they can be sent to the frontend.
    '''

    def get_all_menu_items(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM menu_items")
        record = cursor.fetchall()
        self.connection.commit()
        cursor.close()

    def get_all_menu_items(self, filter=None):
        """ Get all menu items depending on the filter.
        
        Fetch all the menu items from the database so that they can be sent to the frontend. 
        Check the filter and select the specific categories of items using an if statement.

        Args:
            filter: Determines the category of item that will be fetched from the database.
        
        Returns:
            A 2-dimensional array representing rows of data from the database.
        """
        with self.connection.cursor() as curs:
            if not(filter):
                sql = "SELECT * FROM menu_items ORDER BY item_id" # Return all items in the menu when no filter is applied.
            elif int(filter) == 1:
                sql = "SELECT * FROM menu_items WHERE item_type = 'starter' ORDER BY item_id" # Get all starters in the menu.
            elif int(filter) == 2:
                sql = "SELECT * FROM menu_items WHERE item_type = 'main' ORDER BY item_id" # Get all mains in the menu.
            elif int(filter) == 3:
                sql = "SELECT * FROM menu_items WHERE item_type = 'desert' ORDER BY item_id" # Get all drinks in the menu.
            else:
                sql = "SELECT * FROM menu_items WHERE item_type = 'drink' ORDER BY item_id" # Get all desserts in the menu.
            curs.execute(sql)
            record = curs.fetchall() # Get all records.
            self.connection.commit()
        return record

    '''
    Get item information from an id.
    '''

    def get_item_name_from_id(self, item_id):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT * FROM menu_items WHERE item_id = '{item_id}'".format(item_id=item_id))
            record = curs.fetchone()
            self.connection.commit()
            curs.close()
        return record

    '''
    Get all the orders within the database so that the kitchen can see them.
    '''

    def get_all_sales(self, filter=None):
        with self.connection.cursor() as curs:
            if not filter:
                sql = "SELECT * FROM sales INNER JOIN users ON sales.user_id=users.user_id ORDER BY sales.sale_id;"
                curs.execute(sql)
            else:
                sql = "SELECT * FROM sales INNER JOIN users ON sales.user_id=users.user_id WHERE sales.status = " + \
                    filter+" ORDER BY sales.sale_id;"
                curs.execute(sql)
            record = curs.fetchall()
            self.connection.commit()
            curs.close()
        return record

    '''
    Get all the information associated with a specific order id so that the 
    kitchen staff can see all the items and information associatd with a specific 
    order.
    '''

    def get_order_by_id(self, sale_id):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT * FROM order WHERE sale_id = '{sale_id}'".format(sale_id=sale_id))
            record = curs.fetchall()

    def get_user_role(self, username):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT role FROM users WHERE username = '{name}'".format(name=username))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record

    def get_salt(self, username):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT salt_value FROM users WHERE username = '{name}'".format(name=username))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record

    '''
    Given an ID of a status and the current status of that sale. Update the status by one.
    '''

    def update_sale_status_by_id(self, sale_id, current_status):
        with self.connection.cursor() as curs:
            sql = "UPDATE sales SET status = '" + \
                str(int(current_status)+1)+"' WHERE sale_id = '"+sale_id+"';"
            curs.execute(sql)
            self.connection.commit()
            curs.close()

    '''
    Get all the items associated with a specific sale and filtered by starter, main, dessert or drinks.
    '''

    def get_items_in_order_by_sale_id(self, sale_id, filter):
        with self.connection.cursor() as curs:
            sql = "SELECT * FROM orders INNER JOIN menu_items ON orders.item_id = menu_items.item_id WHERE item_type = '" + \
                filter+"' AND orders.sale_id = '"+sale_id+"';"
            curs.execute(sql)
            record = curs.fetchall()
            self.connection.commit()
            curs.close()
        return record

    '''
    A function that checks if a given username exists in the database, if it does it returns True otherwise False
    '''

    def check_username_exists(self, username):
        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT EXISTS (SELECT FROM users WHERE username='{username}');")
        result = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return result[0][0]

    '''
    A function that stores user registration details in the database
    '''

    def store_registration_details(self, form_data):
        cursor = self.connection.cursor()

        salt = salting()
        password = form_data['customer_password'] + salt
        hash = hashingLocally(password)

        cursor.execute(f"INSERT INTO users(first_name, last_name, role, username, password, salt_value) \
                         VALUES('{form_data['first_name']}','{form_data['last_name']}', 'Customer', '{form_data['customer_phone']}', \
                         '{hash}', '{salt}');")

        cursor.execute("SELECT * FROM users")
        self.connection.commit()
        cursor.close()
        return

    '''
    This method is used to upload a customers complaint to the database.
    '''

    def store_complaint(self, form_data):
        with self.connection.cursor() as curs:
            sql = "INSERT INTO complaints (first_name, last_name, phone_no, email, complaint_text) VALUES (%s, %s, %s, %s, %s)"
            val = (form_data.get('firstname'), form_data.get('lastname'), form_data.get(
                'phonenumber'), form_data.get('email'), form_data.get('message'))
            curs.execute(sql, val)
            self.connection.commit()
            curs.close()

    '''
    This method is used to get all customer complaints from the database.
    '''

    def get_all_complaints(self):
        with self.connection.cursor() as curs:
            curs.execute("SELECT * FROM complaints")
            record = curs.fetchall()
            self.connection.commit()
            curs.close()
        return record

    '''
    This function will retrieve order numbers, first and last names associated with an order,
    order status and various other order details.
    '''

    def get_orders(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT sales.sale_id, users.first_name, users.last_name, sales.status, sales.order_time, \
                        sales.order_date, sales.delivered FROM sales JOIN users ON sales.user_id=users.user_id \
                        ORDER BY sales.sale_id ASC;")
        result = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return result

    '''
    This function will be used to cancel an order based on its sale_id, the function
    will be used with the 'cancel_order' feature on the waiter view order page
    '''

    def delete_order(self, sale_id):
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM orders WHERE sale_id='{sale_id}';")
        cursor.execute(f"DELETE FROM sales WHERE sale_id='{sale_id}';")
        self.connection.commit()
        cursor.close()

    '''
    This function will be used for updating the delivery status of a order on the 
    waiter view order page, waiters will be able to click a button which will trigger
    this function and update the delivery status of the order.
    '''

    def update_delivery_status(self, sale_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT delivered FROM sales WHERE sale_id='{sale_id}'")
        result = cursor.fetchall()
 
        if (str(result[0][0]) == "False"):
            cursor.execute(f"UPDATE sales SET delivered=true where sale_id='{sale_id}'")
        elif (str(result[0][0]) == "True"):
            cursor.execute(f"UPDATE sales SET delivered=false where sale_id='{sale_id}'")

        self.connection.commit()
        cursor.close()

    def get_name(self, username):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT first_name FROM users WHERE username = '{name}'".format(name=username))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record
    
    def get_surname(self,username):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT last_name FROM users WHERE username = '{name}'".format(name=username))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record
    
    def get_status(self,sale_id):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT status FROM sales WHERE sale_id = '{sale}'".format(sale=sale_id))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record

    def get_user_id(self,username):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT user_id FROM users WHERE username = '{name}'".format(name=username))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record[0][0]

    def get_latest_sale_id(self,user_id):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT sale_id FROM sales WHERE user_id = '{user}'".format(user=user_id))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        sale_id = 0
        for r in record:
            if r[0] > sale_id:
                sale_id = r[0]
        return sale_id

    def get_item_id(self,sale_id):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT item_id FROM orders WHERE sale_id = '{sale}'".format(sale=sale_id))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record

    def get_quantity(self,item_id,sale_id):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT quantity FROM orders WHERE item_id = '{item}' AND sale_id = '{sale}'".format(item=item_id,sale=sale_id))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record

    def get_sale_id(self,user_id):
        with self.connection.cursor() as curs:
            curs.execute(
                "SELECT sale_id FROM sales WHERE user_id = '{user}'".format(user=user_id))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record

    def get_orders_by_user_id(self,user_id):
        with self.connection.cursor() as curs:
            curs.execute("SELECT sales.sale_id, users.first_name, users.last_name, sales.status, sales.order_time, \
                            sales.order_date, sales.delivered FROM sales JOIN users ON sales.user_id=users.user_id \
                             WHERE sales.user_id = '{sale_id}' ORDER BY sales.sale_id ASC;".format(sale_id=user_id))
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record
    
    '''
    Function that returns records needed for the manager page
    '''
    def get_manager_orders(self):
        with self.connection.cursor() as curs:
            curs.execute("SELECT * FROM orders INNER JOIN sales ON orders.sale_id=sales.sale_id ")
            record = curs.fetchall()
            self.connection.commit()
            curs.close()
        return record
    
    def increase_stock(self, item_id):
        with self.connection.cursor() as curs:
            curs.execute("UPDATE menu_items SET stock=stock+1 WHERE item_id=' {item}'".format(item=item_id))
            self.connection.commit()
            curs.close()

    def decrease_stock(self, item_id):
        with self.connection.cursor() as curs:
            curs.execute("UPDATE menu_items SET stock=stock-1 WHERE item_id=' {item}'".format(item=item_id))
            curs.close()
    def get_free_table(self):
        with self.connection.cursor() as curs:
            curs.execute("SELECT table_id FROM tables WHERE available = 't' ORDER BY table_id ASC LIMIT 1;")
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record

    def check_if_user_has_table(self,user_id):
        with self.connection.cursor() as curs:
            curs.execute(f"SELECT table_id FROM tables WHERE customer = '{user_id}'")
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record

    def assign_table(self,user_id,table_id):
        with self.connection.cursor() as curs:
            curs.execute(f"UPDATE tables SET available = 'f', customer = '{user_id}' WHERE table_id = '{table_id}' AND customer is NULL")
            self.connection.commit()
            curs.close()

    def notify_waiter(self,customer):
        with self.connection.cursor() as curs:
            curs.execute(f"SELECT assistance FROM tables WHERE customer = '{customer}'")
            record = curs.fetchall()
            if (str(record[0][0]) == "True"):
                curs.execute(f"UPDATE tables SET assistance = 'f' WHERE customer = '{customer}'")
            else:
                curs.execute(f"UPDATE tables SET assistance = 't' WHERE customer = '{customer}'")
            self.connection.commit()
            curs.close()

    def check_assistance(self,customer):
        with self.connection.cursor() as curs:
            curs.execute(f"SELECT assistance FROM tables WHERE customer = '{customer}'")
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
        return record[0][0]
    
    def notify_waiter_false(self,customer):
        with self.connection.cursor() as curs:
            curs.execute(f"UPDATE tables SET assistance = 'f' WHERE customer = '{customer}'")
            self.connection.commit()
            curs.close()

    def check_if_delivered(self,sale_id):
        with self.connection.cursor() as curs:
            curs.execute(f"SELECT delivered FROM sales WHERE sale_id = '{sale_id}'")
            record = curs.fetchall()
            print(record)
            self.connection.commit()
            curs.close()
            if record == []:
                record = True
                return record
            else:
                return record[0][0]
    
    def delete_table(self,user_id):
        with self.connection.cursor() as curs:
            curs.execute(f"UPDATE tables SET available = 't',assistance = 'f', customer = NULL, clean = 'f' WHERE customer = '{user_id}'")
            self.connection.commit()
            curs.close()

    def get_user_id_from_sales(self,sale_id):
        with self.connection.cursor() as curs:
            curs.execute(f"SELECT user_id FROM sales WHERE sale_id = '{sale_id}'")
            record = curs.fetchall()
            self.connection.commit()
            curs.close()
        return record[0][0]
