# Product Recommend

## Input Data

``<User Id>,<Product Id>``

|User ID | Product ID |
|-|-|
| 421d2709e1c2138a756c223d824c316e | 8026 | 2015/06/20T10:00:00 | Click |
| 5c2ebc17052b076fd036fb61e989c0b9 | 2173 | 2015/06/28T11:00:00 | Click |
| b4bab661ff821f52d3b5091bfb41ece3 | 3321 | 2015/08/28T11:01:00 | Click |
| d31f22cfa0ef210194ab076146199ff3 | 3532 | 2015/08/28T12:00:01 | Purchase |



## Collaborative Filtering

One row per user and one column per product. It's will be 1 if the user have viewed the product, otherwise will be 0.  

|| Product 1 | Product 2 | Product 3 | Product 4 | Product 5 |
|-|:-:|:-:|:-:|:-:|:-:|
| **User 1** | 0 | 1 | 1 | 0 | 0 |
| **User 2** | 0 | 1 | 1 | 0 | 1 |
| **User 3** | 0 | 0 | 1 | 0 | 0 |
| **User 4** | 1 | 0 | 0 | 0 | 1 |
| **User 5** | 0 | 0 | 0 | 0 | 1 |


Use the cosine theorem to calculate any two column data, and the distance of two vectors will be the similarity.

(Product 1, Product 2) similarity
``a = (0,0,0,1,0)``
``b = (1,1,0,0,0)``
``similarity =  1 - spatial.distance.cosine(a, b)``

|| Product 1 | Product 2 | Product 3 | Product 4 | Product 5 |
|-|:-:|:-:|:-:|:-:|:-:|
| **Product 1** | 1 | 0 | 0 | 0 | 0.577350 |
| **Product 2** | 0 | 1 | 0.816496 | 0 | 0.408248 |
| **Product 3** | 0 | 0.816496 | 1 | 0 | 0.333333 |
| **Product 4** | 0 | 0 | 0 | 1 | 0 |
| **Product 5** | 0.577350 | 0.408248 | 0.333333 | 0 | 1 |











