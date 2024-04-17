# syntax=docker/dockerfile:1

FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

# Install wkhtmltopdf and other necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/local/bin/ ; ln -s /usr/bin/wkhtmltopdf /usr/local/bin/

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
