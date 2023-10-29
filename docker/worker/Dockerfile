FROM python:3.10-slim
# pull official base image
LABEL maintainer="rudotcom@githubm.com"
LABEL description="Celery worker image for DASHA"
LABEL version="1.0"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./backend /app/backend
COPY ./requirements.txt /app
COPY ./docker/worker/worker-entrypoint.sh /app

# Install pip requirements
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt


RUN chmod +x /app/worker-entrypoint.sh
ENTRYPOINT ["/app/worker-entrypoint.sh"]
