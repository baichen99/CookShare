## 搭建环境

### MongoDB

1. 使用docker启动MongoDB，通过环境变量指定用户名和密码

    ```bash
    docker run -d -p 27017:27017 --name mongodb \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=password \
    mongo
    ```

    或者使用docker-compose

    ```bash
    docker-compose up mongodb -d
    ```

2. 安装mongoshell

    [官方网站](https://www.mongodb.com/docs/mongodb-shell/connect/)

3. 连接MongoDB

    ```bash
    mongosh "mongodb://admin:password@localhost:27017"
    ```

4. 创建数据库

    ```bash
    use tutor_db
    db.createUser({user: "tutor_user", pwd: "tutor_password", roles: [{role: "readWrite", db: "tutor_db"}]})
    ```

#### 其他mongo命令

1. 查看所有数据库

    ```bash
    show dbs
    ```
2. 查看当前数据库

    ```bash
    db
    ```

3. 删除数据库

    ```bash
    db.dropDatabase()
    ```

4. 查看当前数据库下的所有集合

    ```bash
    show collections
    ```

5. 删除集合

    ```bash
    db.collection.drop()
    ```

### 安装依赖

```bash
pip install fastapi beanie
```

## 贡献代码流程

1. fork项目到自己的仓库
2. clone项目到本地
3. 创建分支
  
   ```bash
    git checkout -b feature/xxx
    ```

4. 提交代码

   ```bash
    git add .
    git commit -m "xxx"
    git push origin feature/xxx
    ```

5. 提交PR

**P.S. **

请在提交PR之前先同步远程仓库的代码

commit格式为`[feat]: xxx`，比如`[feat]: add user model`，如果是修复bug，commit格式为`[fix]: xxx`，比如`[fix]: fix user model`

## 项目结构

```bash
LICENSE：项目的开源许可证文件。
README.md：项目的说明文档，一般用markdown格式编写。
pycache：Python解释器自动生成的目录，用于缓存编译后的Python代码。一般不需要手动管理。
app.py：FastAPI应用程序的入口文件。
auth：存放JWT授权相关的代码。
jwt_bearer.py：实现JWT的Bearer认证。
jwt_handler.py：实现JWT的生成和解析。
config：存放应用程序配置相关的代码。
config.py：存放应用程序的配置参数。
data：存放MongoDB数据库文件。
db：MongoDB的数据文件目录。
docker-compose.yml：Docker Compose的配置文件。
gitignore：git的忽略文件列表，列出了应该被忽略的文件和目录。
main.py：应用程序的主要逻辑代码。
models：存放应用程序的数据模型。
admin.py：存放管理员数据模型。
routes：存放应用程序的路由和API。
admin.py：实现管理员相关的路由和API。
services：存放应用程序的业务逻辑。
admin.py：实现管理员相关的业务逻辑。
```

