if u want to bring any machine learning model in front of world so we should prepare 
api's. 
An API stands for Application Programming Interface.
It’s like a bridge that allows two different software applications to communicate with each other.

api is ntg but a connector btw 2 pieces of software 
customer order dish --> made in kitchen --> brought to table 
customer (FE) --> kitchen (BE) 
waiter is api , since he is the component , he is connecting to kitchen to customer 


fast api is a modern , high performace web frame work for building apis with py
fast api is made upon 2 famous libraries , starlette and pydantic

the http req that is receving by fast api it is through starlette and sends back res
it manages how ur api receive req and sends back res 

pydantic is data validation library 
pydantic is used to check if data coming into your api is correct and in the 
right format  

res time of other api's are too slow 
back frame works are having more boyler plate code and lengthy unncessary code 
fast to run --> fast api 
fast to code --> fast api 


🔹 WSGI vs ASGI vs SGI
Think of SGI (Server Gateway Interface) as the agreement or translator between your Python app and a web server.
WSGI (Web Server Gateway Interface)
The old standard.
Only handles synchronous requests (one at a time per worker).
Works well for traditional apps (Flask, Django classic).
Example: If a request is waiting for a database response, the worker is blocked until it finishes.
ASGI (Asynchronous Server Gateway Interface)
The modern standard.
Supports both sync and async code.
Allows handling many requests at once without blocking.
Used by FastAPI, Django Channels, Starlette.
Needed for things like WebSockets, real-time chat, background tasks.
SGI (general idea)
Just a contract between app & server.
Web server says: “Here’s a request, do your thing.”
App says: “Here’s the response.”
How they talk depends on which SGI standard (WSGI or ASGI).


Gunicorn & Uvicorn
These are application servers that sit between your code and the outside world.
Gunicorn
Stands for Green Unicorn.
A WSGI server → works with Flask, Django (traditional).
Handles multiple workers (processes), load balancing.
Good for synchronous apps.
Uvicorn
A ASGI server → works with FastAPI, Starlette.
Super-fast, built on uvloop (high-performance event loop).
Handles async requests, WebSockets, background tasks.
👉 Sometimes people combine them:
Gunicorn (process manager) + Uvicorn workers (async server) = scalable FastAPI deployment.


SGI for a 1-year-old (super-simple story 🍼)
Imagine this like ordering food at a restaurant:
The Web Server (Waiter) = takes your order (HTTP request).
The SGI (Translator) = makes sure the waiter and the chef understand each other.
The Python App (Chef) = cooks your meal (response).
The Customer (User/Browser) = eats the food.
Now:
In WSGI world:
The chef can only cook one dish at a time. If one order takes too long, other customers must wait.
In ASGI world:
The chef is smart and can start cooking multiple dishes at once. If one dish is waiting (say pasta boiling), the chef works on another dish meanwhile.
Gunicorn/Uvicorn:
Think of them as the kitchen managers who hire multiple chefs (workers) so many customers can be served at once.

