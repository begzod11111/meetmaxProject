FROM python:3.9

EXPOSE 8000
COPY ../meetmax .
WORKDIR .


COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["py", "manage.py", "runserver"]