FROM python:3.6.5

WORKDIR /home/


ENV FLASK_APP = app.py

COPY requirements.txt .
COPY pip.conf /home/parallels/Desktop/project/pip.conf

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
EXPOSE 8010

CMD ["python","app.py"]
