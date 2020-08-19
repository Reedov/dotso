FROM python:3.8.3

COPY ./requirements.txt /tmp/requirements.txt
COPY ./run_wsgi.sh /run_wsgi.sh

RUN eval `apt-get update $2>/dev/null` && eval `apt-get install -y $2>/dev/null` && pip3 install -r /tmp/requirements.txt

COPY /imager /imager
WORKDIR /imager

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


