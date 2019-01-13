# BareboneShop
Shopify Developer Intern Challenge Implementation

# Securing the end points
Restricted HTTP methods
Input validation-malformed url prevented

# Libraries
Django Rest Framework

# Endpoints
/products/ -  will list all the products. methods allowed GET, POST
/products/id/ - To view products one by one by id in detail. Methods allowed GET
/products/id/purchase - POST method on this endpoint will reduce the inventory count of id product. Products with zero inventory will throw 404 error "Not found"
/product/id/addcart/ - POST product json {"product": "Amazon Echo","price": 29,"product_cnt": 1,"checked_out": false,"owner": 1} to addcart

| Endpoint        | Description           | Method Allowed  |
| ------------- |:-------------:| -----:|
| /      | root | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |
