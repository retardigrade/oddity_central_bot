FROM python:3.9-alpine

WORKDIR /bot_code

RUN apk --no-cache add gcc musl-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]