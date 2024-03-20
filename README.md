## E-Commerce System

This Django project implements a simple e-commerce system with the following functionalities:

**Models:**

* **Customer:** Represents a customer with a one-to-one relationship to the Django User model.  
  * Attributes: name, email.
* **Product:** Represents a product with attributes like name, price, and an optional image.
  * Includes a property `imageURL` to retrieve the product image URL.
* **Order:** Represents an order placed by a customer with details such as customer, date, completeness status, and transaction ID.  
  * Includes methods to calculate total prices and check if shipping is required.
* **OrderItem:** Represents an item within an order with references to the product, quantity, and date added.  
  * Includes a method to calculate the total price of the order item.
* **ShippingAddress:** Represents the shipping address associated with an order.
  * Attributes: customer, order, address, city, state, zipcode, date added.

**Functionality Overview:**

* **Customers:** Manage customer accounts with names and emails.
* **Products:** Add, edit, and manage product details including names, prices, and images.
* **Orders:** Track orders placed by customers, their status, and transaction details.
* **Order Items:**  Manage individual items within orders with quantities and total prices.
* **Shipping Addresses:** Store shipping details for orders.

**Models' Functionality:**

* **Calculations:**
  * The `Order` model calculates the total price of all items in the order.
  * The `OrderItem` model calculates the total price of a specific item.
* **Shipping:**
  * The `Order` model checks if shipping is required based on the products in the order.

**Usage:**

* Create customers, products, and orders through the Django admin interface.
* Associate customers with orders and products with order items.
* View and manage orders, order items, and shipping addresses.


