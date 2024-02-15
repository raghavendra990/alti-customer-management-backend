
## Software and Version
Python 3.10<br />
Django 4.2.9<br />
Postgres 12.10<br />
React 18.2 <br />
Docker version 24.0.2


<b>React Frontend Repo </b>: [https://github.com/raghavendra990/alti-customer-management-frontend](https://github.com/raghavendra990/alti-customer-management-frontend)

# Project Structure:
<pre> 
.
├── Dockerfile 			# DockerFile for the backend
├── README.md
├── backend
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py  		# URL root
│   └── wsgi.py
├── db.sqlite3
├── docker-compose.yml  	# Docker YML contains backend and postgres conf
├── manage.py
├── requirements.txt # requirement txt
└── userauth    		# app to store user data, add user, login, Logout
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── authentication.py  	# custom jwt authentication
    ├── jwt.py
    ├── log.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py 		# DB models
    ├── serializers.py # serializers for views 
    ├── tests.py
    ├── urls.py 		# url routing for userauth
    └── views.py  		# views for userauth
</pre>

## Installation
## clone the backend project
	git clone https://github.com/raghavendra990/demo-docker-backend.git
	cd demo-docker-backend
 	
 ### build docker image
	docker-compose build
 ### Run Docker image
 	docker-compose up

## Backend structure: 
![Architecture](/architecture.png)

Backend is built using django rest framework and Postgres as backend DB. 

It majorly contain two apps details below:
	
<b>userauth</b>: It is used for authentication for the user with apis like Login, Register, Logout. I have used JWT custom authentication, code present at demo-backend/userauth/authentication.py .

<b>For Logout</b>, the frontend application will just delete the jwt token from storage, but there is still a chance that token remains valid and the fraudster can miss use it. That is Why we have created a Table BlackListedToken where we will store the blacklisted tokens and we have created Custom Permission Class IsTokenValid present in authentication.py file in userauth app.


