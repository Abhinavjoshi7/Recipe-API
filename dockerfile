FROM python:3.9-alpine3.13
LABEL maintainer="Abhinav Joshi"

ENV PYTHONUNBUFFERED 1

# Copy the requirements file into the docker image  
# Copy the APP directory that contains the Django app
# Workdir is the working default directory , from where the comands will be runned 
# Expose the port from the container to our machine

COPY ./requirements.txt /tmp/requirements.txt 
COPY ./requirements.dev.txt /tmp/requirements.dev.txt 
COPY ./app /app
WORKDIR /app
EXPOSE 8000

#Default dev value to false, this can be overwritten through docker-compose.yml
ARG DEV=false
# This command will be runned on the alpine linux image
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip &&\
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV ="true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user
