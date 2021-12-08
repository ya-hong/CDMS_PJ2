## PostgreSQL数据库连接

### Install
使用psycopg2进行连接，使用前需要安装
```shell
pip install psycopg2
```

### Config
```be/model/```目录下的database.ini文件是连接数据库所需的配置参数，内容如下：
```editorconfig
[postgresql]
host=localhost
database=$database$
user=postgres
password=$password$
```
- host即为数据库的host，默认为localhost
- database为数据库的名称 ，使用前需要在postgre中创建并修改
- user为用户名，默认为postgres
- password为连接时所用密码

数据库有所修改时，记得修改该config文件中的参数。

### Connect
```be/model/```下的db_handler.py文件实现了简单连接数据库的功能，依赖于上述的config文件建立连接，连接失败时将会报错。
