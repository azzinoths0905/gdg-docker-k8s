FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN pip install flask -i https://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com 

EXPOSE 80

ENV NAME World

CMD ["python", "app.py"]