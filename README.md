## Video for the Code as the server is associated to my student login: **https://www.youtube.com/watch?v=Kh-TE_jPE1Q**
Team 20 Oaxaca Restaurant Web Application
===============================================

This is the source code for Team 20's Oaxaca web application. The aim of this project was to create a web application for the Oaxaca restaurant group, which streamlines the restaurant's operations and improves its overall efficiency. 

Key Features
============

The Oaxaca restaurant management web app includes the following key features:

Menu and Menu Management
-------------------------

This feature allows customers to seemlessly interact with the menu, place orders, edit orders and pay for their orders. We have also created various features to allow staff (waiters and kitchen staff) to manage the menu in various ways including editing menu item information, descriptions, images, price etc.


Secure Account Registration and Login
--------------------------------------

The account registration feature allows new customers to create Oaxaca accounts. The registration page utilises secure hashed and salted password storage to protect user data. Once registered, customers can log in to the Oaxaca web application using their username and password, making it easy to access their order history, make a complaint, view order status etc.

Waiter Table Management
------------------------

The waiter table management feature allows waiters to easily manage tables in various ways including, assigning tables to waiters, being able to view free tables, marking tables as cleaned and available and allowing waiters to see if a specific table requires assistance.

Kitchen and Waiter Orders Management
------------------------------------

The kitchen and waiter order management features allow the kitchen staff and waiter staff to view and manage orders in various ways. Both dashboards allow staff members to view order details such as order IDs, date and times the orders were placed, the customers name, order status and delivery status (only waiter dashboard). The waiter dashboard provides waiters with multiple order management options such as viewing additional information about an order, marking an order as delivered and cancelling an order. The kitchen dashboard provides kitchen staff with options to change the status of an order (accept, start cooking, finish cooking, complete) and to also view additional information about each order.


Staff Web Application Navigation
---------------------------------

A key feature of the web application is the staff side site navigation bar and footer, which provide staff with easy access to various parts of the site such as kitchen and order dashboards, view complaints, homepage, menu page and about us page. Both features are crucial elements of a web application and enhance the user experience and make it easy for staff members to find the information they need. By providing easy navigation and important links, these elements contribute to the usability, functionality, and accessibility of the web application.


Installation
============

In order to use this site you can follow the following steps:

1) Clone the git repository, you can use the following command to do so
```
git clone https://gitlab.cim.rhul.ac.uk/TeamProject20/PROJECT/
```
You will then be prompted to give a username and password, which you need to provide
```
Cloning into 'PROJECT'...
Username for 'https://gitlab.cim.rhul.ac.uk': myUsername
Password for 'https://myUsername@gitlab.cim.rhul.ac.uk': 
```

2) After cloning the repository change you current working directory to the ```PROJECT``` directory:
```
cd PROJECT
```

3) Lastly, you need to install the various packages and libraries used throughout the project:
```
pip install -r requirements.txt
```

Usage
=====

To start the project you need to do the following:

1) Start the Django web application
```
python DjangoApp/manage.py runserver
```
You will be prompted for a username and password, this should be your RHUL username and password, this is used to establish an SSH connection with the PostgreSQL database server hosted by the university. 
```
Username: ZCAP214
Password: 
```

If the connection is successful you should see something like this appear on your terminal:
```
----- tunnel opened -----
{'user': 'group20', 'channel_binding': 'prefer', 'dbname': 'CS2810/group20', 'host': 'localhost', 'port': '42165',
 'options': '', 'sslmode': 'prefer', 'sslcompression': '0', 'sslsni': '1', 'ssl_min_protocol_version': 'TLSv1.2',
 'gssencmode': 'prefer', 'krbsrvname': 'postgres', 'target_session_attrs': 'any'} 

----- connection established -----
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 14, 2023 - 12:22:51
Django version 4.1.5, using settings 'team20app.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

2) The final step is to open a browser (chrome or firefox is recommended) and type the following into the search bar:
```
http://127.0.0.1:8000/project/
```
This will direct you to the homepage where you can view and interact with the site.

Supported Operating Systems
============================

The Oaxaca web application has been tested on the following operating systems:

- Microsoft Windows 10 22H2 - Project has full functionality and works as it should
- Ubuntu 20.04.5 LTS - Project has full functionality and works as it should
- macOS Monterey Version 12.2 - Project has full functionality and works as it should

Contributors
=============

- Qasim Ijaz
- Alex Fuller
- Harvey Saunders
- Yasmin Shahid
- Hassan Imran
- Haroldas Leknius
- Joseph Salter
