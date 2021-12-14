# 搜索

## URL
POST http://[address]/extra/search

## Request

### Body

```json
{
    "title": [[]],
    "tags": [[]],
    "content": [[]],
    "shop_id": "shop_id",
    "page_num": "page_num",
}
```

### 属性说明


变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
title | array | 标题搜索条件 | Y
tags | array | 标签搜索条件 | Y
content | array | 内容搜索条件 | Y
shop_id | string | 检索特定的商店 | Y
page_name | int | 需要得到检索结果的第几页 | N

对于title, tags, content的检索条件，在同一个子array中的关系为AND，在不同子array中的关系为OR

## Response


Status Code:

码 | 描述
--- | ---
200 | 检索成功
5XX | 参数错误

### Body:

```json
{
  "books": [{"book_id": "id", "shop_id": "id"}]
}
```

### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
books | array | 检索到的书籍列表，只有返回200时才有效 | N
