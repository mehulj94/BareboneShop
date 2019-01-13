# BareboneShop
Shopify Developer Intern Challenge Implementation

# Securing the end points
Restricted HTTP methods
Input validation-malformed url prevented

# Libraries
Django Rest Framework

# Endpoints

| Endpoint        | Description           | Method Allowed  |
| :------------- |:-------------:| -----:|
| /      | Root | GET |
| /products/      | Lists all products, Enter new products | GET, POST |
| /products/{id}/      | Browse products one by one. id parameter will be 1,2,3..      |   GET |
| /products/{id}/avl/ | List products with non zero inventory      |    GET |
| /products/{id}/purchase/ | Buy product. Will decrease inventory by 1. Products with zero inventory will throw 404 error "Not found"     |    POST |
| /product/{id}/addcart/ | Add product to Cart      |    POST |
| /cart/ | Cart details. Contains products, quantity and total amount      |    GET |
| /cart/checkout/ | Complete Cart purchase      |    POST |

###/product/id/addcart/ - POST product json {"product": "Amazon Echo","price": 29,"product_cnt": 1,"checked_out": false,"owner": 1} to addcart
