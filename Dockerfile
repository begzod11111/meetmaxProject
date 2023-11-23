FROM python:3.9

EXPOSE 8000

WORKDIR /usr/src/meetmax

COPY . /usr/src/meetmax

COPY requirements.txt /usr/src/requirements.txt

RUN pip install -r /usr/src/requirements.txt

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000