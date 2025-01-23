from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import complaintform
from .forms import paymentForm
from .forms import customer_register
from .basket import item
from .basket import basket
from .basket import basket as tempbasket
from django.shortcuts import redirect
from .db_service import database
from .forms import LoginForm
from .forms import changeform
from .forms import addform 
from .SaltHash import salting,hashingLocally,hashingFromDatabase,authenticate,authenticateRole
from .menu_item import menu_item
from .forms import select_change_form
from .models import addModle
import os
from django.conf import settings
from django.contrib.auth import login,logout
from .login import userlogin

userlogin = userlogin()
basket = basket()
database = database()
tempbasket = tempbasket()
id = None

def index(request):
    context = {}

    return render(request, 'index.html', context)

def error(request):
    context = {}

    return render(request, 'error-page.html', context)

def FAQ(request):
    context = {}

    return render(request, 'FAQ-page.html', context)

def about(request):
    if userlogin.status:
        html = "loginNav.html"
    else:
        html = "navigation.html"
    context = {
        "html": html
    }

    return render(request, 'about-us.html', context)

def change(request):
    if userlogin.status == False or userlogin.role != 'Kitchen':
        return redirect('error')
    if id == None:
        return redirect('/project/select-change')
    item = database.get_menu_item(id)
    if request.method == 'GET':
        form = changeform()
        form.fields['name'].initial = item[1]
        form.fields['description'].initial = item[3]
        form.fields['price'].initial = item[2]
        form.fields['allergies'].initial = item[4]
        form.fields['calories'].initial = item[5]
    elif request.method == 'POST':
        form = changeform(request.POST)
        if form.is_valid():
            form_data = request.POST
            name = form_data.get('name')
            description = form_data.get('description')
            price = form_data.get('price')
            allergies = form_data.get('allergies')
            calories = form_data.get("calories")
            if form_data.get('name') is not "":
                database.change_menu_item(id, "item_name", name)
            if form_data.get('description') is not "":
                database.change_menu_item(id, "description", description)
            if form_data.get('price') is not "":
                database.change_menu_item(id, "price", price)
            if form_data.get('allergies') is not "":
                database.change_menu_item(id, "allergies", allergies)
            if form_data.get('calories') is not "":
                database.change_menu_item(id, "calories", calories) 
            return redirect('/project/kitchen-dashboard/-1')
    return render(request, 'Change-menu.html', {'form': form})

def select_change(request):
    if userlogin.status == False or userlogin.role != 'Kitchen':
        return redirect('error')
    db = database.get_menu_name()
    names = []
    for x in range(len(db)//2):
        names.append([])
        names[x].append(db[2 * x])
        names[x].append(db[(2 * x) + 1])

    if request.method == 'GET':
        form = select_change_form()
        form.fields['change'].choices = names
    elif request.method == 'POST':
        if 'next' in request.POST:
            form = select_change_form(request.POST)
            form_data = request.POST
            global id
            id = form_data.get("change")
            return redirect('/project/Change-menu')
        elif 'add' in request.POST:
            return redirect('/project/Add-to-menu')
        elif 'delete' in request.POST:
            form = select_change_form(request.POST)
            form_data = request.POST
            delete_id = form_data.get("change")
            photo_name = database.get_menu_item_photo(delete_id)
            print(photo_name[0])
            file_path = os.path.join(settings.STATICFILES_DIRS[0], photo_name[0])
            os.remove(file_path)
            database.delete_menu_item(delete_id)
            return redirect('/project/kitchen-dashboard/-1')   
    return render(request, 'select-change.html', {'form': form})

def waiter_orders(request):
    if userlogin.status == False or userlogin.role != 'Waiter':
        return redirect('error')
    context = {
        'sales': database.get_orders()
    }
    print("Waiter orders page requested")
    return render(request, 'waiter-orders.html', context)


def add(request):
    if userlogin.status == False or userlogin.role != 'Kitchen':
        return redirect('error')
    context = {'form': addform()}

    if request.method == 'POST':
        form = addform(request.POST, request.FILES)
        if form.is_valid():
            form_data = request.POST
            name = form_data.get('name')
            description = form_data.get('description')
            price = form_data.get('price')
            allergies = form_data.get('allergies')
            item_type = form_data.get('type')
            calories = form_data.get("calories")
            image_file = form.cleaned_data['photo']
            file_name = image_file.name
            file_path = os.path.join(settings.STATICFILES_DIRS[0], file_name)
            with open(file_path, 'wb') as f:
                f.write(image_file.read())
            new = menu_item(name, price, description, allergies, calories, item_type, file_name)
            database.add_new_menu_item(new)
            return redirect('/project/kitchen-dashboard/-1')
        else:
             context = {'form': form, 'error_message': 'Invalid photo file: ' + str(form.errors['photo'][0])}
    return render(request, 'Add-to-menu.html', context)

def menu(request, filter):
    """ Returns the menu frontend with menu items from database.

    The menu view takes in a "filter" as a parameter and determins if it is in 
    a valid range. If its in a valid range the database will be queried with the 
    specified filter parameter. These records will then be returned and passed to 
    the frontend via context.

    Args:
        filter: Used to determine which catagory of items to fetch from the 
        database.
    
    Returns:
        menu.html with conext containing database data.
    """
    if int(filter) < 0 or int(filter) > 4: 
        filter = None # ensure no invalid url parameters are entered by the user.
    b = basket.get_basket()
    if userlogin.status:
        html = "loginNav.html"
    else:
        html = "navigation.html"
    print(basket.get_basket())
    print(basket.get_basket_value())
    context = {
        "menu_items": database.get_all_menu_items(filter), # Call the database function to get all items in the menu based on the specified filter.
        "filter": filter if filter else -1,
        "basket": b,
        "basket_value": basket.get_basket_value(),
        "number_of_items": len(b),
        "login": userlogin.status,
        "html": html
    } 
    return render(request, "menu.html", context)

def register(request):
    context = {}

    return render(request, 'customer-register.html', context)


def terms_of_service(request):
    context = {}

    return render(request, 'terms-of-service.html', context)

'''
Complaint form can be used by users to submit complaints directly 
to the restraunt.
'''
@csrf_exempt
def complaintForm(request):
    # Send the form to the fronted via context
    if userlogin.status:
        html = "loginNav.html"
    else:
        html = "navigation.html"
    context = {
        'form': complaintform(),
        'invalidData': None,
        'html': html
    } 
    if request.method == 'POST': # Check the request type.
        form = complaintform(request.POST)
        if form.is_valid():
            form_data = request.POST # Extract form data from POST request
            database.store_complaint(form_data)
            context['invalidData'] = "false"
            return redirect('/project/customer-landing')
        else:
            context['invalidData'] = "true"
    return render(request, 'complaint.html', context)

#views for waiters
def tables(request):
    if userlogin.status == False or userlogin.role != 'Waiter':
        return redirect('error')
    
    uid = database.get_user_id(userlogin.username)
    context = { 'assigned_tables': database.get_assigned_tables(uid)
               }
    print("My table view requested")
    return render(request, 'waiter-my-tables.html', context)

def manageTables(request):
    if userlogin.status == False or userlogin.role != 'Waiter':
        return redirect('error')
    
    uid = database.get_user_id(userlogin.username)
    context = {'assigned_to_me': database.get_my_managed_tables(uid),
               'unassigned_tables': database.get_unassigned_tables(),
               'waiter': uid
               }
    print("Manage table view requested")
    return render(request, 'waiter-manage-tables.html', context)

def waiterLanding(request):
    if userlogin.status == False or userlogin.role != 'Waiter':
        return redirect('error')
        
    context = {'user': request.session.get('username')
               }
    return render(request, 'waiter-landing.html', context)

def change_table_clean_status(request, waiter, table_num, current_status):
    database.set_clean_table(waiter,  table_num, current_status)
    print(table_num, current_status)
    return redirect('/project/my-tables')

def change_table_available_status(request,  waiter, table_num, current_status):
    database.set_available_table(waiter, table_num, current_status)
    print(table_num, current_status)
    return redirect('/project/my-tables')

def change_table_assistance_status(request,  waiter, table_num, current_status):
    database.set_assistance_table(waiter, table_num, current_status)
    print(table_num, current_status)
    return redirect('/project/my-tables')

def add_table_assignment(request, waiter, table_num, current_status):
    database.set_table_assignment(waiter, table_num, current_status)
    return redirect('/project/manage-tables')

def remove_table_assignment(request, waiter, table_num, current_status):
    database.set_table_assignment(waiter, table_num, current_status)
    return redirect('/project/manage-tables')
#views for waiter ends    


def customerLanding(request):
    if userlogin.status == False or userlogin.role != 'Customer':
        return redirect('error')

    user_id = database.get_user_id(userlogin.username)
    user_has_table = database.check_if_user_has_table(user_id)
    print(f"user_id: {user_id}, user_has_table: {user_has_table}")

    if user_has_table:
        userlogin.assistance = database.check_assistance(user_id)
        print(f"userlogin.assistance: {userlogin.assistance}")

    context = {
        "name": userlogin.name,
        "assistance": userlogin.assistance
    }
    sale_id = database.get_latest_sale_id(user_id)
    status = database.get_status(sale_id)

    if status and not database.check_if_delivered(sale_id):
        context["order"] = status[0][0]

    print("Customer landing page requested")
    return render(request, 'Customer-landing.html', context)

@csrf_exempt
def payment_form_view(request):
    context = {
        'form': paymentForm(),
        'basket': basket.get_basket(),
        'basket_value': basket.get_basket_value()
    } 
    if request.method == 'POST':
        form = paymentForm(request.POST)
        

        database.submit_order(basket,database.get_user_id(userlogin.username))
        basket.clear_basket()
        user_id = database.get_user_id(userlogin.username)
        if database.check_if_user_has_table(user_id) == []:
            table_id = database.get_free_table()[0][0]
            database.assign_table(user_id,table_id)

        return redirect('customer-landing')
        if form.is_valid():
            form_data = request.POST
    return render(request, 'payment.html', context)

def view_complaints(request):
    context = {
        'complaints': database.get_all_complaints()
    }
    print("Page for staff to view complaints requested")
    return render(request, 'view-complaints.html', context)

def LogoutView(request):
    userlogin.logout()
    return redirect('login')

def loginForm(request):
    context = {
        'form': LoginForm(),
        'login': None
    } 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = request.POST
            username = form_data.get('username')
            password = form_data.get('password')
            salt = database.get_salt(username)
            password = hashingFromDatabase(salt,password)

            if (authenticate(password,database.get_login_users(username))):
                fname = database.get_name(username)[0][0]
                sname = database.get_surname(username)[0][0]
                if(authenticateRole(database.get_user_role(username)) == 'Waiter'):
                    userlogin.set_details(username,password,'Waiter',fname,sname)
                    userlogin.login()
                    context['login'] = "false"
                    request.session['username'] = username
                    request.session['user_id'] = database.get_user_id(username)
                    return redirect('welcome')
                elif(authenticateRole(database.get_user_role(username)) == 'Kitchen'):
                    userlogin.set_details(username,password,'Kitchen',fname,sname)
                    userlogin.login()
                    context['login'] = "false"
                    return redirect('/project/kitchen-dashboard/-1')
                else:
                    userlogin.set_details(username,password,'Customer',fname,sname)
                    userlogin.login()
                    context['login'] = "false"


                    return redirect('/project/menu/-1')
            else:
                context['login'] = "true"
    return render(request, 'login-page.html', context)

def view_basket(request):
    if userlogin.status:
        html = "loginNav.html"
    else:
        html = "navigation.html"
    context = {
        'html': html,
        "login": userlogin.status,
        'basket': basket.get_basket(),
        'basket_value': basket.get_basket_value()
    }

    return render(request, 'view-basket.html', context)

def increment_item_basket_quantity(request, item_name, page_name, filter):
    """ Increments the quantity of an item.

    Take in a page name and filter and redirect the user to the page with 
    the filter applied. Increment the quantity of a specific item.

    Args:
        item_name: Item we want to increment in our basket.
        page_name: Page the user is sending the request from.
        filter: The filter applied to the menu page that the 
            user sent a request from.
    
    Returns:
        Redirect depending on which page the user sends a request from.
    """
    print(item_name)
    basket.add_to_basket(item_name)    
    if page_name == "menu":
        return redirect('/project/menu/'+filter)

    return redirect('view_basket')

def decrement_item_basket_quantity(request, item_name, page_name, filter):
    """ Decrements the quantity of an item.

    Take in a page name and filter and redirect the user to the page with 
    the filter applied. Decrement the quantity of a specific item.

    Args:
        item_name: Item we want to increment in our basket.
        page_name: Page the user is sending the request from.
        filter: The filter applied to the menu page that the 
            user sent a request from.
    
    Returns:
        Redirect depending on which page the user sends a request from.
    """
    basket.remove_from_basket(item_name)
    if page_name == "menu":
        return redirect('/project/menu/'+filter)
    return redirect('view_basket')

def check_name_contains_nums(name):
    return any(letter.isdigit() for letter in name)

@csrf_exempt
def register(request):
    context = {
        'form': customer_register(),
        'usernameError': False,
        'passwordError': False,
        'nameError': False
    } 
    if request.method == 'POST':
        form = customer_register(request.POST)
        if form.is_valid():
            form_data = request.POST
            if (database.check_username_exists(form_data['customer_phone']) is True):
                context['usernameError'] = "True"
            elif (form_data['customer_password'] != form_data['password_repeat']):
                context['passwordError'] = "True"
            elif (check_name_contains_nums(form_data['first_name']) is True or check_name_contains_nums(form_data['last_name']) is True):
                context['nameError'] = "True"
            else:
                database.store_registration_details(form_data)
                context['usernameError'] = "False"
                context['passwordError'] = "False"
                context['nameError'] = "False"

    return render(request, 'customer-register.html', context)

'''
This page is used to get all the orders currently in the system. A range of filters can be 
applied which sort the orders into different categories such as pending, accepted, cooking 
and completed.
'''
def kitchen_dashboard(request, filter):
    if userlogin.status == False or userlogin.role != 'Kitchen':
        return redirect('error')
    if int(filter) < 0 or int(filter) > 4: # ensure no invalid url parameters are entered by the user.
        filter = None
    context = {
        "sales": database.get_all_sales(filter), # get all the sales with a specific filter applied.
        "number_of_orders": len(database.get_all_sales()), # no id is the parameter for all orders.
        "number_of_pending_orders": len(database.get_all_sales("1")), # 1 is the id for pending orders.
        "number_of_completed_orders": len(database.get_all_sales("4")), # 4 is the id for completed orders.
    } 
    return render(request, 'kitchen-dashboard.html', context)

'''
This method is used to retrieve all items associated with a specific sale. Each category of item is 
queried and placed within the context map and sent to the frontend.
'''

def view_order(request, sale_id, user_redirect):
    if userlogin.status == False:
        return redirect('error')
    context = {
        "mains":database.get_items_in_order_by_sale_id(sale_id, "main"), # query mains
        "desserts":database.get_items_in_order_by_sale_id(sale_id, "desert"), # query desserts
        "starters":database.get_items_in_order_by_sale_id(sale_id, "starter"), # query starters
        "drinks":database.get_items_in_order_by_sale_id(sale_id, "drink"), # querr drinks
        "sale_id":sale_id,
        "user": str(user_redirect),
    } 
    return render(request, 'view-order.html', context)

'''
This method is used to update the status of a specific order. It is used by the kitchen dashboard page.
'''
def update_sale_status(request, sale_id, current_status):
    database.update_sale_status_by_id(sale_id, current_status)
    return redirect('/project/kitchen-dashboard/-1') # redirect to the dashboard showing all items

def cancel_order(request, sale_id):
    if userlogin.status == False or userlogin.role != 'Waiter':
        return redirect('error')
    context = {}
    print(f"Cancelling order with sale_id: {sale_id}")
    user_id = database.get_user_id_from_sales(sale_id)
    user_has_table = database.check_if_user_has_table(user_id)
    if user_has_table:
        database.delete_table(user_id)
    print(database.delete_order(sale_id))
    return redirect('/project/waiter-orders')

def update_delivery_status(request, sale_id):
    if userlogin.status == False or userlogin.role != 'Waiter':
        return redirect('error')
    context = {}
    user_id = database.get_user_id_from_sales(sale_id)
    user_has_table = database.check_if_user_has_table(user_id)
    print(f"Changing order delivery status of order with sale_id {sale_id}")
    database.update_delivery_status(sale_id)
    if database.check_if_delivered(sale_id) and user_has_table:
        database.delete_table(user_id)

    return redirect('/project/waiter-orders')

def notify_waiter(request):
    if userlogin.status == False or userlogin.role != 'Customer':
        return redirect('error')

    user_id = database.get_user_id(userlogin.username)
    user_has_table = database.check_if_user_has_table(user_id)

    if not user_has_table:
        userlogin.assistance = not userlogin.assistance
    else:
        database.notify_waiter(user_id)

    return redirect('/project/customer-landing')

def view_bill(request):
    if userlogin.status == False or userlogin.role != 'Customer':
        return redirect('error')
    sale_id = database.get_latest_sale_id(database.get_user_id(userlogin.name))
    tempbasket.clear_basket()
    for item in database.get_item_id(sale_id):
        for item_id in item:
            for x in range(database.get_quantity(item_id,sale_id)[0][0]):
                tempbasket.add_to_basket(int(item_id))
    context = {
        'basket': tempbasket.get_basket(),
        'basket_value': tempbasket.get_basket_value()
    } 
    return render(request, 'Bill.html',context)


def view_order_history(request):
    if userlogin.status == False or userlogin.role != 'Customer':
        return redirect('error')
    context = {
        'sales': database.get_orders_by_user_id(database.get_user_id(userlogin.username))
    }
    return render(request, 'customer-order.html',context)

def customer_view_order(request,sale_id):
    if userlogin.status == False or userlogin.role != 'Customer':
        return redirect('error')

    context = {
        "mains":database.get_items_in_order_by_sale_id(sale_id, "main"), # query mains
        "desserts":database.get_items_in_order_by_sale_id(sale_id, "desert"), # query desserts
        "starters":database.get_items_in_order_by_sale_id(sale_id, "starter"), # query starters
        "drinks":database.get_items_in_order_by_sale_id(sale_id, "drink"), # querr drinks
        "sale_id":sale_id,

    } 
    return render(request, 'customer-view-order.html',context)

def manager(request):
    context = {
        'stock': database.get_all_menu_items(),
        'orders': database.get_manager_orders()
    }
    print("Manager page requested")
    return render(request, 'manager.html', context)

def add_stock(request, item_id):
    database.increase_stock(item_id)
    return redirect('manager')

def reduce_stock(request, item_id):
    database.decrease_stock(item_id)
    return redirect('manager')
