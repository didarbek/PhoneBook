# pulling official python image
FROM python:3.9.5-slim-buster

# setting our work directory
WORKDIR /usr/src/app

# setting all environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# installing system dependencies
RUN apt-get update && apt-get install -y netcat

# installing all dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copying local project to container
COPY . /usr/src/app/

# running entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]