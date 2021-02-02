# basicbrixapp
Coding Exam
============

I do develop different features to fullfill all the needed requirements in the cart API
- Registration feature of User
- Login and Logout features with the use of JWT Authentication
- Only the Admin account can add products to the product list
- User can only access the List API w/ search filter and sorting filet and the Cart API for adding and removing items
- Added fields in the List API like the total quantity per product and total price per product per transaction.

Installation
============

Install requirements.txt in a virtual environment


API
======

Registration API using JWT Authentication 
=========================================
-for the user account so they can't easily add products and access the Add Products API

link for POST request:

http://127.0.0.1:8000/cart/register

needed parameters:

{
    "user": {
        "username": "user",
        "password": "user"
    },
    "name": "basicbrix",
    "email": "manila"
}

Login API using JWT Authentication
==================================
link for POST request:

http://127.0.0.1:8000/api/token/

-this api will give access token and refresh token

Logout API
=============
link for POST request:

http://127.0.0.1:8000/cart/logout_all/

-this will put the access token to the blacklisttoken in db


List Products API for User w/ Pagination, Search and Sort Algorithm
=====================================================================

link for GET request:

-need to pass the access token in the request

http://127.0.0.1:8000/cart/store/



List Products API for Admin w/ Pagination, Search and Sort Algorithm
=====================================================================

link for GET request:

-need to pass the access token in the request

http://127.0.0.1:8000/cart/admin_store/

link for Search and Sort Algorithm
http://127.0.0.1:8000/cart/admin_store/?search=keyboard

-search is the parameter key then add the product name or price to be search or sorted


Add Products API for Admin Only
================================
link for POST request:

-need to pass the access token in the request

http://127.0.0.1:8000/cart/admin_store/

needed parameters in form-data:

    "name": "keyboard",
    "price": 10,
    "quantity": 20
    
    
Edit Products API for Admin Only
==================================
link for PUT request:

-need to pass the access token in request

http://127.0.0.1:8000/cart/admin_store/$/
- $ is the product id

needed parameters in form-data:

    "name": "keyboard",
    "price": 5,
    "quantity": 20
    
Delete Products API for Admin Only
===================================
link for DELTE request:

-need to pass the access token in request

http://127.0.0.1:8000/cart/admin_store/$/
- $ is the product id


List Items to the Cart
======================
link for GET request:

-need to pass the access token in request

http://127.0.0.1:8000/cart/order_list



Adding and Removing Items in the Cart
=========================
link for POST request:

-need to pass the access token in request

http://127.0.0.1:8000/cart/update_list/

needed parameters in form-data:

-product id and the action of request (add for adding to cart and remove for removing to the cart)

-every request is an increment or decrement of 1 in the total items in the cart

    "productId": "1",
    "action": "add",
    
    

    "productId": "1",
    "action": "remove",
    
    
- Automatically adjust the total price, total cart items, price per product, quantity per product etc.
  




