# syntax=docker/dockerfile:1

FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

# ENTRYPOINT ["python3"]

##-Staging Env
CMD ["/bin/bash", "-c", "/app/docker-entrypoint2.sh"]

##-Production Env
# CMD ["/bin/bash", "-c", "/app/docker-entrypoint.sh"]
