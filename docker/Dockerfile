FROM python:3.10-slim
# Identify the maintainer of an image
LABEL maintainer="arkhbum@githubm.com"
LABEL description="Django image for polynex.arkhbum.local"
LABEL version="1.0"

EXPOSE 4004

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

#ENV SECRET_KEY=${SECRET_KEY}
#ENV POLYNEX_POSTGRES_DB=${POLYNEX_POSTGRES_DB}
#ENV POLYNEX_POSTGRES_USER=${POLYNEX_POSTGRES_USER}
#ENV POLYNEX_POSTGRES_PASSWORD=${POLYNEX_POSTGRES_PASSWORD}

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


COPY ./backend /app/backend
COPY ./requirements.txt /app

# Install pip requirements
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /app/requirements.txt

WORKDIR /app/backend

CMD ["gunicorn", "--bind", "0.0.0.0:4004", "backend.wsgi"]
