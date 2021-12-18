## 搜索

#### URL
POST http://[address]/extra/search

#### Request

##### Body

```json
{
    "title": [[]],
    "tags": [[]],
    "content": [[]],
    "shop_id": "shop_id",
    "page_num": "page_num"
}
```

##### 属性说明


变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
title | array | 标题搜索条件 | Y
tags | array | 标签搜索条件 | Y
content | array | 内容搜索条件 | Y
shop_id | string | 检索特定的商店 | Y
page_name | int | 需要得到检索结果的第几页 | N

对于title, tags, content的检索条件，在同一个子array中的关系为AND，在不同子array中的关系为OR

#### Response


Status Code:

码 | 描述
--- | ---
200 | 检索成功
5XX | 参数错误

##### Body:

```json
{
  "books": [{"book_id": "id", "shop_id": "id"}]
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
books | array | 检索到的书籍列表，只有返回200时才有效 | N

## 物流状态

### 发货（卖家）

#### URL：

POST http://$address$​/seller/delivery

#### Request


##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N


##### Body:

```json
{
    "user_id": "$seller_id$",
    "shop_id": "$shop_id$",
    "order_id": "$order_id$"
}
```

| 变量名   | 类型   | 描述   | 是否可为空 |
| -------- | ------ | ------ | ---------- |
| user_id | string | 卖家id | N           |
| shop_id | string | 商店id | N           |
| order_id | string | 订单号 | N          |

#### Response

Status Code:

| 码   | 描述                     |
| ---- | ------------------------ |
| 200  | 成功发货                 |
| 506  | 参数错误（订单号不存在或商店id错误） |
| 401  | 无相应权限（卖家id有误） |

##### Body:

```json
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| message | string | 返回错误消息，成功时为"ok" | N          |



### 收货（买家）

#### URL：

POST http://$address$​/buyer/delivery

#### Request

##### Body：

```json
{
    "user_id": "$buyer_id$",
    "order_id": "$order_id$",
    "password": "$password$"
}
```

##### 属性说明：

| 变量名   | 类型   | 描述         | 是否可为空 |
| -------- | ------ | ------------ | ---------- |
| user_id  | string | 买家用户ID   | N          |
| order_id | string | 订单ID       | N          |
| password | string | 买家用户密码 | N          |

#### Response

Status Code:

| 码   | 描述                     |
| ---- | ------------------------ |
| 200  | 成功收货                 |
| 506  | 参数错误（订单号不存在） |
| 401  | 授权失败（密码有误）     |

##### Body：

```json
{
    "message": "$error message$"
}
```

##### 属性说明：

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| message | string | 返回错误消息，成功时为"ok" | N          |



## 订单查询

#### URL：

POST http://$address$/buyer/history

#### Request

##### Body:

```json
{
    "user_id": "$buyer_id$"
}
```

##### 属性说明：

| 变量名  | 类型   | 描述       | 是否可为空 |
| ------- | ------ | ---------- | ---------- |
| user_id | string | 买家用户ID | N          |

#### Response

Status Code:

| 码   | 描述                   |
| ---- | ---------------------- |
| 200  | 成功发货               |
| 401  | 授权失败（用户不存在） |

##### Body:

```json
{
    "orders": [
        {
            "order_id": "$order_id$",
            "shop_id": "$shop_id$",
            "order_time": "$order_time$",
            "order_state": "$order_state$"
        },
        ...
    ]
}
```

##### 属性说明:

| 变量名 | 类型  | 描述                 | 是否可为空 |
| ------ | ----- | -------------------- | ---------- |
| orders | class | 该用户的历史订单列表 | N          |

orders数组：

| 变量名      | 类型   | 描述     | 是否可为空 |
| ----------- | ------ | -------- | ---------- |
| order_id    | string | 订单id   | N          |
| shop_id     | string | 商店id   | N          |
| order_time  | string | 下单时间 | N          |
| order_state | string | 订单状态 | N          |

订单状态分为：超时未付款、买家取消、未发货、已发货、已签收



## 取消订单

#### URL：

POST http://$address$​/extra/cancel_order

#### Request

##### Body:

```json
{
    "user_id": "$buyer_id$",
    "order_id": "$order_id$",
    "password": "$password$"
}
```

##### 属性说明:

| 变量名   | 类型   | 描述         | 是否可为空 |
| -------- | ------ | ------------ | ---------- |
| user_id  | string | 买家id       | N          |
| order_id | string | 订单号       | N          |
| password | string | 买家账户密码 | N          |

#### Response

Status Code:

| 码   | 描述                             |
| ---- | -------------------------------- |
| 200  | 成功取消订单                     |
| 401  | 授权失败（用户不存在或密码有误） |
| 5XX | 无此订单 |
| 5XX | 无法取消 (已发货或已取消) | 

##### Body:

```json
{
    "message": "$error_message$"
}
```

##### 属性说明:

| 变量名  | 类型   | 描述                           | 是否可为空 |
| ------- | ------ | ------------------------------ | ---------- |
| message | string | 错误信息，成功取消订单则返回ok | N          |


## 查看历史订单

#### URL

POST http://[address]/extra/history


#### Request

Headers:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

Body:

```json
{
  "user_id": "$buyer id$",
}
```

key | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N


#### Response

Status Code:

码 | 描述
--- | ---
200 | 登出成功
401 | 用户名或token错误

Body:

```
{
    "orders": [
        {
            "order_id": "id",
            "state": "订单状态",
        }
    ]
}
```

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
orders | string | 返回历史订单id以及状态 | N
