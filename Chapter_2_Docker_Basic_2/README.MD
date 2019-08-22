# 新的篇章：Swarm与Docker的整合——Swarm mode

## 和集群相关的对象

### SWARM

和前面的swarm直接对应，但是不同的是旧版的swarm会独立启动一个容器来运行swarm组件。而于docker整合后的swarm则是用户无感知的。

```shell
$ docker swarm --help

Usage:    docker swarm COMMAND

Manage Swarm

Commands:
  ca          Display and rotate the root CA
  init        Initialize a swarm
  join        Join a swarm as a node and/or manager
  join-token  Manage join tokens
  leave       Leave the swarm
  unlock      Unlock swarm
  unlock-key  Manage the unlock key
  update      Update the swarm

Run 'docker swarm COMMAND --help' for more information on a command.
```

创建swarm集群并启动manager：

```shell
docker swarm init --listen-addr 192.168.99.200:2377 --advertise-addr 192.168.99.200
```

此时会输出加入swarm集群的方式：

```shell
docker swarm join --token SWMTKN-1-0nbwp5l3wsrtvf1hhrzf7dxbabpvitzo2ssyjqhnymg7d2ypzr-b1v1t5lnabvr4ojw9xe7eugkk 192.168.99.200:2377
```

如果没有记住的话：

```shell
docker swarm join-token worker
```

依旧会输出：
```shell
docker swarm join --token SWMTKN-1-0nbwp5l3wsrtvf1hhrzf7dxbabpvitzo2ssyjqhnymg7d2ypzr-b1v1t5lnabvr4ojw9xe7eugkk 192.168.99.200:2377
```

在另一台节点上执行
```shell
docker swarm join --token SWMTKN-1-0nbwp5l3wsrtvf1hhrzf7dxbabpvitzo2ssyjqhnymg7d2ypzr-b1v1t5lnabvr4ojw9xe7eugkk 192.168.99.200:2377
```

### NODE

运行`Docker`的主机可以主动初始化一个`Swarm`集群或者加入一个已存在的`Swarm`集群，这样这个运行`Docker`的主机就成为一个`Swarm`集群的节点 (`node`) 。

```shell
$ docker node --help

Usage:    docker node COMMAND

Manage Swarm nodes

Commands:
  demote      Demote one or more nodes from manager in the swarm
  inspect     Display detailed information on one or more nodes
  ls          List nodes in the swarm
  promote     Promote one or more nodes to manager in the swarm
  ps          List tasks running on one or more nodes, defaults to current node
  rm          Remove one or more nodes from the swarm
  update      Update a node

Run 'docker node COMMAND --help' for more information on a command.
```

使用ls命令查看节点信息：

```shell
$ docker node ls

ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS      ENGINE VERSION
v1oo73vt40hnjivnhnw78po4u *   dameng-00           Ready               Active              Leader              18.09.8-ce
yrz7drszt4hq5j8c8rbhoexqc     dameng-01           Ready               Active                                  18.09.8-ce
```

### STACK

Stack可以说是升级版的Compose：

```shell
$ docker stack --help

Usage:    docker stack [OPTIONS] COMMAND

Manage Docker stacks

Options:
      --kubeconfig string     Kubernetes config file
      --orchestrator string   Orchestrator to use (swarm|kubernetes|all)

Commands:
  deploy      Deploy a new stack or update an existing stack
  ls          List stacks
  ps          List the tasks in the stack
  rm          Remove one or more stacks
  services    List the services in the stack
```

部署：

```shell
# compose:

$ docker-compose -f CONFIG-YAML up

# stack:

$ docker stack deploy -c CONFIG-YAML STACK-NAME
```

查看：

```shell
# compose:

$ docker-compose ps
$ docker ps

# stack:

$ docker node ls
$ docker stack ls
$ docker service ls
```

终止：

```shell
# compose:

$ docker-compose -f CONFIG-YAML down

# stack:

$ docker stack rm STACK-NAME
```

网络：

单机 vs 跨节点
> 注意: docker stack 默认使用的是swarm，但也是可以对接k8s的

### SERVICE

```shell
$ docker service --help

Usage:    docker service COMMAND

Manage services

Commands:
  create      Create a new service
  inspect     Display detailed information on one or more services
  logs        Fetch the logs of a service or task
  ls          List services
  ps          List the tasks of one or more services
  rm          Remove one or more services
  rollback    Revert changes to a service's configuration
  scale       Scale one or multiple replicated services
  update      Update a service

Run 'docker service COMMAND --help' for more information on a command.
```

查看：

```shell
$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
oyiesfc3biiq        myapp_myapp         replicated          1/1                 friendlyhello:v3    *:5000->5000/tcp
xrk7kska1z76        myapp_redis         replicated          1/1                 redis:latest
```

扩容：

```shell
$ docker service scale myapp_myapp=2

ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
oyiesfc3biiq        myapp_myapp         replicated          2/2                 friendlyhello:v3    *:5000->5000/tcp
xrk7kska1z76        myapp_redis         replicated          1/1                 redis:latest
```

## TRY IT OUT (4)

这次我们要用`Swarm`集群来部署前面做过的`friendlyhello`。

在前面，我们了解到可以用`Docker Machine `很快地创建一个虚拟的Docker主机，接下来我们来创建2个新的Docker主机，并加入到集群中。

### STEP 1: 创建Swarm集群——管理节点

首先是一个管理节点，创建并通过ssh连接：
```shell
$ docker-machine create -d virtualbox manager
$ docker-machine ssh manager
```

我们可以看到：

![Screen Shot 2019-08-19 at 3.17.14 PM.png](https://i.loli.net/2019/08/19/7T4DsYz9agXWBwn.png)

然后，我们用`docker swarm init`从这个节点初始化一个`Swarm`集群，如果这个Docker主机有多个IP（多个网卡），就要用`--advertise-addr`指定一个:

```shell
$ docker swarm init --advertise-addr 192.168.99.107
```

我们可以看到：

![Screen Shot 2019-08-19 at 3.27.10 PM.png](https://i.loli.net/2019/08/19/t5yxPIdX2i4ra7R.png)

现在我们的`Manager`节点就是刚刚创建的集群的管理节点了，

记得复制一下它输出的添加工作节点的那句命令。

### STEP 2: 添加项目文件

接下来我们`Manager`节点的`~/try-it-out-4`里添加几个文件:

- app.py
- Dockerfile
- docker-stack.yaml

```shell
$ mkdir try-it-out-4
$ cd try-it-out-4
$ vi app.py
$ vi Dockerfile
$ vi docker-stack.yaml

$ docker build -t friendlyhello .
```

![Screen Shot 2019-08-19 at 3.21.41 PM.png](https://i.loli.net/2019/08/19/TnFMQsCtm1DBIcS.png)

#### app.py

```python
from flask import Flask
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

#### Dockerfile

```Dockerfile
FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN pip install flask redis -i https://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com 
EXPOSE 5000
ENV NAME World

CMD ["python", "app.py"]
```

#### docker-stack.yaml

```yaml
version: "3"

services:
  myapp:
    image: friendlyhello
    container_name: myapp
    ports:
      - 5000:5000
    environment:
      NAME: World

  redis:
    image: redis
    container_name: web
```


### STEP 3: 创建Swarm集群——工作节点

继续，我们来创建一个工作节点：

首先回到主机：

```shell
$ exit 
```

接着创建一个新的虚拟机`worker`，并通过上面复制的那句命令加入到集群里:

```shell
$ docker-machine create -d virtualbox worker
$ docker-machine ssh worker

$ docker swarm join --token SWMTKN-1-3wd0vdozskitmpw5vofkjc9ie6251wuno21dmbugqk56pd97iv-eu9w5gkkmy7chvgcwt7j71iu4 192.168.99.107:2377
```

我们可以看到：

![Screen Shot 2019-08-19 at 3.25.26 PM.png](https://i.loli.net/2019/08/19/THRZgC2B4iIjeKd.png)

### STEP 4: 使用Stack部署服务

我们先回到`manager`节点：

```shell
$ exit

$ docker-machine ssh manager
```

然后使用`docker stack deploy`部署服务，其中`-c`参数指定`docker-stack.yaml`文件：

```shell
$ docker stack deploy -c ~/try-it-out/docker-stack.yaml friendlyhello
```

![Screen Shot 2019-08-19 at 3.27.10 PM.png](https://i.loli.net/2019/08/19/t5yxPIdX2i4ra7R.png)

部署完毕。

### STEP 5: 访问friendlyhello

现在就可以通过集群中的任意一个节点的IP访问到这个`flask`项目了：

![Screen Shot 2019-08-19 at 4.41.31 PM.png](https://i.loli.net/2019/08/19/ajdG5vKYcbS6mfF.png)

## TRY IT OUT (5)

我们继续用前一个Case的集群。

进入`manager`节点，在`try-it-out-5`里新建一个`docker-stack.yaml`：

```shell
$ docker-machine ssh manager

$ mkdir try-it-out-5
$ vi docker-stack.yaml
```

#### docker-stack.yaml

```yaml
version: '3.1'

services:

  db:
    image: postgres
    command: postgres -c 'shared_buffers=512MB' -c 'max_connections=2000'
    restart: always
    environment:
      POSTGRES_USER: dameng
      POSTGRES_PASSWORD: pythonic
    ports:
      - 5432:5432
    volumes:
      - pgdata:/var/lib/postgresql/data


  adminer:
    image: adminer
    restart: always
    ports:
      - 8998:8080

volumes:
  pgdata:
```

然后部署：

```shell
$ docker stack deploy -c docker-stack.yaml postgresql
```

接着就可以从`8998端口`访问GUI了：

![Screen Shot 2019-08-19 at 5.17.16 PM.png](https://i.loli.net/2019/08/19/IOakg98EdLFuwAC.png)