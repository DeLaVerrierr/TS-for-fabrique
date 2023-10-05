FROM python:3.10

WORKDIR /fabric

COPY requirements.txt /fabric/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /fabric/


RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
