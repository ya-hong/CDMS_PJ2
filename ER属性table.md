| 所属实体 | 属性           | 类型                      | 注释                            |
| -------- | -------------- | ------------------------- | ------------------------------- |
| 用户     | uid            | varchar(255), primary key |                                 |
|          | pwd            | text, not null            |                                 |
|          | shop_id        | varchar(255), foreign key |                                 |
|          | balance        | float                     | 账户余额                        |
|          | token          | text                      |                                 |
|          | terminal       | text                      |                                 |
| 商铺     | shop_id        | varchar(255), primary key |                                 |
|          | uid            | varchar(255), foreign key |                                 |
|          | ranking        | integer                   | 排名？不知道要不要实现          |
| 书籍     | book_id        | text, primary key         |                                 |
|          | title          | text                      |                                 |
|          | author         | text                      |                                 |
|          | publisher      | text                      |                                 |
|          | original_title | text                      |                                 |
|          | translator     | text                      |                                 |
|          | pub_year       | text                      |                                 |
|          | pages          | integer                   |                                 |
|          | price          | integer                   |                                 |
|          | currency_unit  | text                      |                                 |
|          | binding        | text                      |                                 |
|          | isbn           | text                      |                                 |
|          | author_intro   | text                      |                                 |
|          | book_intro     | text                      |                                 |
|          | content        | text                      |                                 |
|          | tags           | text                      |                                 |
|          | picture        | blob                      |                                 |
|          | quantity       | integer                   | 库存                            |
|          | uid            | varchar(255), foreign key | 店主id                          |
|          | shop_id        | varchar(255), foreign key | 店铺id                          |
| 订单     | order_id       | text, primary key         |                                 |
|          | uid            | varchar(255), foreign key |                                 |
|          | shop_id        | varchar(255), foreign key |                                 |
|          | book_id        | text, foreign key         |                                 |
|          | order_time     | text                      | 下单时间，超时未付款取消，，，  |
|          | order_quantity | integer                   | 购买数量                        |
|          | current_state  | integer / char            | 状态：未付款，已付款未发货，... |
|          |                |                           |                                 |
|          |                |                           |                                 |
|          |                |                           |                                 |
|          |                |                           |                                 |
|          |                |                           |                                 |





