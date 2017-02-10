# mongodb 初始化配置，包括安全性和备份

 0. 菜鸟教程的MongoDB资料, http://www.runoob.com/mongodb/mongodb-tutorial.html

 1. 安装mongodb 
    
    ``` shell
        # MAC
        $ brew install mongodb
        
        # MAC with openssl 
        $ brew install mongodb --with-openssl
        
        # install with manual
        $ curl https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-3.4.2.tgz
        $ tar -zxvf mongodb-linux-x86_64-3.4.2.tgz
        $ mv mongodb-linux-x86_64-3.4.2/  /usr/local/mongodb
        $ export PATH=/usr/local/mongodb/bin:$PATH 
    ```


 2. 配置mongodb 
    
    ``` shell
        $ vi /usr/local/etc/mongod.conf
        
        systemLog:
          destination: file
          path: /usr/local/var/log/mongodb/mongo.log
          logAppend: true
        storage:
          dbPath: /usr/local/var/mongodb
        net:
          bindIp: 127.0.0.1
          port: 27017
    ```
 
 
 3. mongodb 连接
    
    ```
    mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
    ```


 4. 数据备份 mongodump --help

    ``` shell
        # 备份所有数据 （默认备份到当前目录的 dump/ 目录下）
        $ mongodump --host 127.0.0.1 --port 27017 
        
        # 备份数据库实例
        $ mongodump -h 127.0.0.1:27017 -d dbname -o /data/bak/mongodb
        
        # 备份指定数据库实例的集合
        $ mongodump --collection mycol --db dbname -o ./mycol.bak
    ```
 
 
 5.  一些命令
  
    ``` shell

        
        # 启动mongo
        mongod --dbpath /Users/nico/data
        # mongod --dbpath /Users/nico/data --sslOnNormalPorts
        # BadValue: need sslPEMKeyFile when SSL is enabled
        
        # 显示数据库实例和集合
        show dbs
        show collections
        
        # 创建实例和集合
        use dbname
        
        # 创建用户和密码
        db.createUser(
          {
            user: "reportsUser",
            pwd: "12345678",
            roles: [
               { role: "read", db: "reporting" },
               { role: "read", db: "products" },
               { role: "read", db: "sales" },
               { role: "readWrite", db: "accounts" }
            ]
          }
        )
        db.getSiblingDB("products").runCommand({createUser:"ADMIN", pwd: "password", customerData:<doc>, roles:[]})
        
        # 插入文档
        db.colum.insert({name:"mongo"})
        db.colum.insert(doc)
        
        # 更新或替换
        ## db.colum.update(<query>, <update>, { upsert:<boolean>, multi:<boolean>, writeConcern:<document> } )
        db.colum.update(({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}})
        # 输出信息: WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
        
        ## save , 替换, _id = ObjectId("xxx")
        db.colum.save(<document>, {writeConcern:<document>})
        
        # 查找数据
        ## limit, skip, sort(1升-1降)
        db.colum.find(<query>).pretty()
        db.colum.find().limit(2).skip(10).sort({KEY:1})
        
        # 创建索引 
        ## 1 升 -1 降 , <options>, background, unique, name, dropDups, expireAfterSeconds, weights 
        db.colum.ensureIndex({KEY:1}, <options> )
        
        # 聚合统计
        db.colum.aggregate()
        db.colum.aggregate([{ $group: {_id: "$DUPKEY", count: {$sum:"$NUMKEY"} } }])
        
        
        # 删除数据文档
        db.colum.remove(<query>, { justOne: <boolean>, writeConcern: <document> })
        
        # 删除集合
        db.colum.drop()
        
        # 删除数据库实例
        db.dropDatabase()
        
        
    ```


 6. 安全性: 指定端口, 要求密钥
    
    ``` shell
    # https://docs.mongodb.com/manual/administration/security-checklist/
    # https://www.digitalocean.com/community/tutorials/how-to-securely-configure-a-production-mongodb-server
    # http://security.stackexchange.com/questions/7610/how-to-secure-a-mongodb-instance/7655#7655
    
    通过一个SSH通道连接到你的Mongo虚拟专用服务器，你可以避免很多潜在的安全问题。
    警告：你的VPS一定要完全锁定，不能对其他端口开放。建议SSH配置为只有秘钥或秘钥加密码。
    举例: 设置服务器server_host对外网开放8080端口, mongo_host 只能通过server_host 连接。
    
    然后，运行以下命令来初始化连接：
    ssh \
    -L 8080:mongo_host:27017 \
    -i ~/.ssh/my_secure_key \
    [user@]server_host
    
    我们一步一步来看：
    
    1  -L, 远程调试时,先登录到server_host, 再通过server_host的8080端口跳转到 mongo_host的27017端口。
    
    2  -i 选项只是表示将上面的连接到一个SSH秘钥，而不是一个密码。
    
    3  [user@]server_host , ssh登录的是server_host。
    
    ```
