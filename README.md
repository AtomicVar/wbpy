# wbpy - 命令行版微博客户端

使用 `requests` 模拟登录账号的命令行微博，支持记住账号免登陆，基于 Python 3。支持 Windows/Linux/macOS。

目前仅支持发单行文字微博，适合在脚本中使用管道和文件重定向。

## 应用场景

- 不愿打开浏览器或手机的懒人，想直接在命令行发微博
- 在无图形界面的服务器上发微博
- 自动脚本化发微博，应用于各种毕设、爬虫数据定时展示

## 使用实例

第一次登录，使用`-l`(login)参数：
```
$ wb -l
Username> msn1998@sina.com
Password>
登陆成功！
（已保存登录信息至 /home/geniusguo/wblogin.data）
```

发送单条微博：
```
$ wb
我的第一条微博 ... [Enter]
微博发送成功

$ echo 我的第二条微博 | wb
微博发送成功

$ wb < data.txt
微博发送成功
```

发送多条微博，使用`-i`(interactive)参数：
```
$ wb -i
发微博>我的第四条微博。[Enter]
微博发送成功
发微博> ...
```

## 安装

### 从源码安装

1. 安装依赖：

```
$ pip install --user requests rsa
```

2. 克隆代码

```
$ git clone https://github.com/ZJUGuoShuai/wbpy.git
```

3. 运行

Linux/macOS:

```
$ ./install   # 安装到 /usr/local/bin
$ wb          # 运行

$ ./uninstall # 卸载
```

Windows:

```
C:\> wb      # Windows CMD
PS> .\wb     # Windows PowerShell
```

### 从 PIP 安装

...

### 使用 Docker 镜像

...

## TODO

- [x] 保存账号信息（免登陆）
- [ ] 显示用户昵称
- [x] 显示帮助速度更快
- [x] 实现管道
- [x] 实现文件重定向
- [ ] 支持多行微博
- [ ] 处理验证码
- [ ] 实现从 pip 安装
- [ ] 打包成 Docker
- [ ] 代码结构清晰化，脚本通用性