# 文件结构

```
.
├── __init__.py
│
├── model                                       连接数据库，实际的功能实现
│
├── bp                                          蓝图（子路由）
│   ├── __init__.py
│   ├── auth.py
│   ├── buyer.py
│   └── seller.py
├── readme.md
└── serve.py                                    启动或关闭服务器
```