# Nuveo Backend Test

Workflow's REST API developed as a backend test for Nuveo

#### Requirements
- [Docker](https://www.docker.com/get-started)
- [Python](https://www.python.org/downloads/)

#### To run the application

**Before initializing the process, make sure that there is no Postgresql instance running on its default port.**
Clone this repository, go to the project root, and run:
```
./run_application.sh
```
Wait for the dependencies installation, docker images download, and builds. At the first time, maybe take some minutes.
After the script finish, the application is ready at `http://localhost:5000/`. If necessary, run the command above again.

#### To stop the application enter:
```
./manage.py compose down
```

#### [See the endpoints](https://documenter.getpostman.com/view/13814016/TVmV4ssW)

### Considerations
- I chose RabbitMQ after searching for the most practical tool, since I had no much time available and there were technologies that I was not used to. So, to not complicate at all, I picked up that I found most pratical.
- I apologize for delivery too close to the limit. It was a full week.
- I appreciated the challenge, thank you. It was a learning expirience.

