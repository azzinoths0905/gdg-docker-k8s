FROM python:3.7-slim

WORKDIR /app

COPY . /app

# COPY sources.list /etc/apt/
RUN pip install flask redis -i https://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com 
EXPOSE 5000
ENV NAME World

CMD ["python", "app.py"]