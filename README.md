
## Simple Messenger


#### Prerequisites

- docker - https://www.docker.com/
- docker-compose - https://docs.docker.com/compose/

#### To Run

You must have docker compose installed on the system. Cd to the directory  and run
```
docker-compose up
```
If you dont have docker installed then run this as a flask web application. 


#### Code Structure

The project contains three source files:
1. **app.py** -- Flask web app

2. **helper.py** -- all helper functions

3. **requirements.txt** -- requirement file for building the virtual env.

4. **settings.py** - configurations for the web app

5. **test_app.py** - unite tests for the app

6. **db_init.sql** - sql script to initialize the SQLite database and create the required table

7. **static** - contains css file for styling

8. **templates** - contains Jinja templates for the pages


#### Project Notes

I am using a python-based Flask web application with a sqlite database back-end to develop my messaging service.
In addition to flask request routing, I am also using socketio to broadcast messages. This is done to maintain multi-way
channel between different participants in the app. So when one user sends a message, it should propagate to all the
other users currently logged in. In addition to all the basic requirements, I have also completed the bonus tasks. 
- I have included a unit test file that has only one test but includes the set up and tear down as well as mocking the data
for session and database.
- The data is persisted on to the sqlite database in a file called main.db As long as the docker container is up the 
data will persist. If you need to persist it beyond that then container needs to be started with a volume mount but I
have skipped that for simplicity's sake
- I like minimal styling so have not strayed much beyond bootstrap's default but did add a few touches. The app best 
runs on Chrome

#### Walkaround

The application will start on http://127.0.0.1:8000/ and ask for a username and password. **Enter any name and `123`
for password** (This can be changed in settings.py). The application will then redirect to the chatroom where you will
see all the messages in the database and a form to send messages. Multiple people can log onto the app and send messages
which will then show up on all the pages in real-time due to the use of sockets. Please use incognito windows to start
up different sessions. In order to logout simply close the browser or hit refresh. The server clears up the session when
a socket disconnects