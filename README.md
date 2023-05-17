# CookShare

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

**P.S.**

请在提交PR之前先同步远程仓库的代码

commit格式为`[feat]: xxx`，比如`[feat]: add user model`，如果是修复bug，commit格式为`[fix]: xxx`，比如`[fix]: fix user model`
