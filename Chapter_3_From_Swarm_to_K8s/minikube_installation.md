# Kubernetes初体验

本文会指引读者完成`minikube`及其相关工具的安装，通过一个单节点的`kubernetes`集群来进行学习和体验。

## STEP 1: 安装 kubectl 

> 本文仅演示macOS上通过`Homebrew`安装`kubectl`的过程，windows和linux用户请移步[官方文档](https://kubernetes.io/docs/tasks/tools/install-kubectl/)寻找最方便的安装方法：

通过`Homebrew`安装`kubectl`的过程非常简单：

```shell
$ brew install kubernetes-cli
```

安装完成后，查看版本信息以确认安装成功：

```shell
$ kubectl version
```

## STEP 2: 安装 minikube

`minikube`可以让我们很方便的体验Kubernetes，不过由于一些众所周知的原因，我们在大陆使用起来会有些麻烦，所以我们这次采用[阿里云社区里提供的版本](https://yq.aliyun.com/articles/221687)。

**在开始前，请确保本机装了对应的驱动，我的是VirtualBox，没有的话请先安装一个**

`minikube`在MacOS, Windows和Linux上的安装方法：

- MacOS:

  ```shell
  $ curl -Lo minikube http://kubernetes.oss-cn-hangzhou.aliyuncs.com/minikube/releases/v1.3.1/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
  ```

- Linux:

  ```shell
  $ curl -Lo minikube http://kubernetes.oss-cn-hangzhou.aliyuncs.com/minikube/releases/v1.3.1/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
  ```

- Windows:

  下载 [minikube-windows-amd64.exe](https://yq.aliyun.com/go/articleRenderRedirect?spm=a2c4e.11153940.0.0.7dd54cecRWi6W7&url=http%3A%2F%2Fkubernetes.oss-cn-hangzhou.aliyuncs.com%2Fminikube%2Freleases%2Fv1.2.0%2Fminikube-windows-amd64.exe) 文件，并重命名为 `minikube.exe`

## STEP 3: 初始化环境（可选）

如果在之前有安装过官方的`minikube`，在启动前需要先清除之前的配置：

删除旧集群：

```shell
$ minikube delete
```

删除配置文件：

```shell
$ rm -rf ~/.minikube
```

## STEP 4: 启动 minikube 并打开 dashboard

我们需要通过`minikube start`来创建本地Kubernetes环境，如果不指定驱动，则默认是`Virtualbox`，我们也可以加上`--registry-mirror`来提高速度：

```shell
$ minikube start --registry-mirror=https://docker.mirrors.ustc.edu.cn
```

![step_4_1.png](https://i.loli.net/2019/09/07/vrklOnRjWPg6Jz2.png)

成功以后，我们可以查看集群状态：

```shell
$ minikube status
```

![step_4_2.png](https://i.loli.net/2019/09/07/aCvf5cyM13ER4Gu.png)

最后，我们打开dashboard：

```shell
$ minikube dashboard
```

![step_4_3.png](https://i.loli.net/2019/09/07/tfOCwNg9dqorUai.png)

![step_4_4.png](https://i.loli.net/2019/09/07/lSydEYxOKIDj7ca.png)

> 如果这一步出现了大量`503`，请做一下 STEP 3 里的步骤