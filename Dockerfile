# syntax=docker/dockerfile:1

FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends wkhtmltopdf

RUN echo "Africa/Nairobi" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

# ENTRYPOINT ["python3"]

##-Staging Env
CMD ["/bin/bash", "-c", "/app/docker-entrypoint.sh"]
