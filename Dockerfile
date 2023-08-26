FROM python:bullseye
MAINTAINER Gleb Felyust 'felyust@list.ru'

# copy and install all dependencies
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# copy project files
COPY . /app
WORKDIR /app

# run api
CMD ["/bin/sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8001"]
