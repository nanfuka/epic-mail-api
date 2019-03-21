[![Build Status](https://travis-ci.org/nanfuka/epic-mail-api.svg?branch=integrations)](https://travis-ci.org/nanfuka/epic-mail-api)
## Epic-Mail

# Description

The internet is increasingly becoming an integral part of lives. Ever since the invention of electronic mail by Ray Tomlinson, emails have grown to become the primary medium of exchanging information over the internet between two or more people, until the advent of Instant Messaging (IM) Apps. Despite thE growing need, people have not been adquately empowered to adapt to this change.

In order to close this gap, Epic-Mail application has been developed to facilitate the exchange messages/information over the internet.

Getting Started
Follow these instructions to get a copy of the API to run on your machine.

Prerequisites
Install the following programs before using the API:

1. Python version 3.7.1
2. Postman
Instructions for set up
Clone into this repo using:
Clone into this repo using:
git clone 
Set up a virtual environment for python in the project directory
Inorder to set up the virtual environment, you need to install the python package called virtualenv using pip. Run the command below to install it.

pip install virtualenv to install virtualenv
virtualenv virtual to create a virtual environment named virtual
virtual/Scripts/activate to activate your virtual environment.


After setting up and activating your virtual environment, install all the packages required by the project by running the code below.

pip install -r requirements.txt
Running the tests
Use the following command to run the tests in your virtual environment:

pytest -v
pytest --cov to see coverage
Running the application
Use the following command in the project folder to run the app:

python run.py
#API End points for the application
|HTTP method|	End point|	Functionality|
|GET|	/|	A welcome route to the application or index|
|GET|	/api/v1/messages|	Return all recieved messages|
|GET|	/api/v1/messages/unread	|Return all recieved but unread messages|
|GET|	/api/v1/messages/sent|	Return all sent messages|
|GET|	/api/v1/messages/int:message_id|	Get a specific email-record|
|POST|	/api/v1/messages|	Create a new message|
|POST|	/api/v1/auth/signup|	Register a new user|
|POST|	/api/v1/auth/signin|	Login a user |
|DELETE|	/api/v1/messages/int:message_id|	Delete specific email-record |

#Sample Data to use in postman
Registering a user.
{
	"firstname": "deb",
	"lastname": "kalungi",	
	"email": "kals@gmail.com",
	"password": "Password"
}

User Log In.
{
	"email": "kals@gmail.com",
	"password": "Password",
}

Creating a message
{
	"comment": "New comment about corruption",
	"_type": "red-flag",
	"images": "image.jpg",
	"location": "Lat 11231 Long 14224",
	"videos": "vid.mp4"
}
Sample output after user signup
{
    "data": [
        {
            "email": "kalgs@gm.com",
            "firstname": "deb",
            "id": 1,
            "lastname": "Nsubs"
        }
    ],
    "message": "thanks for registering with Epic mail",
    "status": 201
}

Sample output after user sign in
{
    "data": [
        {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTUzMTU3NDE0fQ.qnGlk2NiD4gDaryar1G-HWr19Ioy2skV5i51ytftQQA"
        }
    ],
    "message": "you have successfully logged in as a user"
}
Posting a message
{"subject": "bnbjhb",
    "message":"1",
    "parentMessageId":1,
    "status":"sent",
    "sender_id":1,
    "reciever_id":1
    }
Sample output after creating a message
{
    "data": [
        {
            "createdOn": "Thu, 21 Mar 2019 11:08:06 GMT",
            "id": 1,
            "message": "1",
            "parentMessageId": 1,
            "status": "sent",
            "subject": "bnbjhb"
        }
    ],
    "status": 201
}
# Adding Token to headers using Postman
- In Postman, select an API method.
- Click the Authorization tab.
- Choose OAuth 2.0 or Bearer Token.
- Copy the token above and paste it in the edit text box provided on the right hand side.
- Built with
- Flask - Micro web framework for Python
- PIP - A python package installer

#Tools Used
- Pivotal Tracker used to write user stories for this project
- Visual Studio acting as an editor for the project files
- Github
- Postman used to test the api end points

#Deployment
- The link to Heroku where the api is deployed can be found [here](https://epicd.herokuapp.com/)

- To access other routes append the api end points stated above to the home route.

# Authors
Deborah Kalungi
