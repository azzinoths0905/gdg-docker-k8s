FROM python:3.7-slim

WORKDIR /app

COPY . /app

COPY sources.list /etc/apt/
RUN apt update && apt install -y curl
RUN pip install flask -i https://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com 
EXPOSE 5000
ENV NAME World

HEALTHCHECK --interval=5s --timeout=3s CMD curl --fail http://localhost:5000/ || exit 1

CMD ["python", "app.py"]