# pull official base image
FROM python:3.7.2-stretch

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy run.sh
#COPY ./run.sh .
# copy project
#COPY . .

## run entrypoint.sh
#ENTRYPOINT ["/usr/src/app/run.sh"]
EXPOSE 8000
