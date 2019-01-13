# BareboneShop
Shopify Developer Intern Challenge Implementation

# Endpoints

| Endpoint        | Description           | Method Allowed  |
| :------------- |:-------------| -----:|
| /      | Return link to products & cart endpoints | GET |
| /products/      | Returns all products & Create new products | GET, POST |
| /products/{id}/      | Returns single product. id parameter will be 1,2,3..      |   GET |
| /products/{id}/avl/ | Returns all products with non zero inventory      |    GET |
| /products/{id}/purchase/ | Endpoint to purchase product. It will decrease the product's inventory by 1. Products with zero inventory will throw 404 error "Not found"     |    POST |
| /product/{id}/addcart/ | Endpoint to add product to Cart      |    POST |
| /cart/ | Returns Cart details. Contains products, quantity and total amount of cart      |    GET |
| /cart/checkout/ | Complete Cart purchase. Inventory of all products in cart will be reduced.      |    POST |

/product/id/addcart/ - POST product json {"product": "Amazon Echo","price": 29,"product_cnt": 1,"checked_out": false,"owner": 1} to addcart

# Securing the end points
Restricted HTTP methods
Input validation-malformed url prevented
