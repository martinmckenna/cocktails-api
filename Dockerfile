FROM python:3.6-alpine

# create a new user named marty
RUN adduser -D marty

# current directory where the app will be installed
WORKDIR /home/marty

# copy file from the machine to the container file system
COPY app app
COPY requirements.txt requirements.txt

# run a virtual env and install requirements
RUN python3 -m venv venv
CMD source ./venv/bin/activate
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev openssl-dev
RUN pip install -r requirements.txt


# The EXPOSE instruction indicates the ports on which a container # # will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Run app.py when the container launches
CMD python app/app.py