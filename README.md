# BareboneShop
Shopify Developer Intern Challenge Implementation

# Endpoints

| Endpoint        | Description           | Method Allowed  |
| :------------- |:-------------| :-----|
| /      | Return link to products & cart endpoints | GET |
| /products/      | Returns all products & Create new products | GET, POST |
| /products/{id}/      | Returns single product. id parameter will be 1,2,3..      |   GET |
| /products/{id}/avl/ | Returns all products with non zero inventory      |    GET |
| /products/{id}/purchase/ | Endpoint to purchase product. It will decrease the product's inventory by 1. Products with zero inventory will throw 404 error "Not found"     |    POST |
| /product/{id}/addcart/ | Endpoint to add product to Cart      |    POST |
| /cart/ | Returns Cart details. Contains products, quantity and total amount of cart      |    GET |
| /cart/checkout/ | Complete Cart purchase. Inventory of all products in cart will be reduced.      |    POST |

/product/id/addcart/ - POST product json {"product": "Amazon Echo","price": 29,"product_cnt": 1,"checked_out": false,"owner": 1} to addcart

# Sample Requests & Response
#### Endpoint /products/
* Request  

`  
GET /products/ HTTP/1.1  
Host: 127.0.0.1:8000  
Connection: keep-alive  
Cache-Control: max-age=0  
Upgrade-Insecure-Requests: 1  
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36  
DNT: 1  
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8  
Accept-Encoding: gzip, deflate, br  
Accept-Language: en-US,en;q=0.9  
Cookie: csrftoken=VHcNRPaoYtUPQ8QliFJGJQZgBbV3vSGBPUEUpjitzd32T129nXqpEJgDFPV1LrVm; sessionid=3kieqota42sr0ujfxeegajgfk3asts6l;  tabstyle=html-tab  
`  
* Response  

`  
{  
  "count": 3,  
  "next": null,  
  "previous": null,  
  "results": [  
    {  
      "id": 1,  
      "title": "Iphone 6",  
      "price": 350,  
      "inventory_count": 17  
    },  
    {  
      "id": 2,  
      "title": "Amazon Echo",  
      "price": 29,  
      "inventory_count": 42  
    },  
    {  
      "id": 3,  
      "title": "Oneplus 6t",  
      "price": 650,  
      "inventory_count": 0  
    }  
  ]  
}  
`  

# Securing the end points
Restricted HTTP methods
Input validation-malformed url prevented
