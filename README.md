# tivix-demo
 a demo application for tivix.
 
 A postman-collection file is also attached to the files, which might be helpfull while testing
 
after clone of this project, use the following steps to get it working with docker:
 1. docker build <name> .   (or) docker build.
 2.docker-compose up -d --build

 
note: the manage.py is located in the top most root folder
For setting it up with a virtual environment, here are the steps required:

 1.clone the proect to any folder.
 
2.setup a python virtual enviroment: python -m venv env
 
3.pip install -r requirements.txt
 
4.setup postgresql via the env file in the root dir
 
5.make migrations via: python manage.py makemigrations , python manage.py migrate
 
6.run via: python manage.py runserver
 
