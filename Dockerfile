FROM python:latest

WORKDIR /usr/bot
COPY . /usr/bot/.

RUN pip install -r requirenments.txt

CMD ["python", "main.py"]
