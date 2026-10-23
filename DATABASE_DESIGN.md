# JZL Electronics database design

The supplied ER diagram has four main entities: User, Component, Order, and Inventory. This starter implements them as Django models.

- **User**: Django's built-in user model stores username and a securely hashed password. `first_name` is used as the display name. `is_staff` controls product management.
- **Component**: ID, name, quantity, price, description, optional image, created timestamp.
- **Order**: ID, user (FK), component (FK), quantity, unit price snapshot, status, created timestamp.
- **Inventory**: ID, component (FK), quantity change, date added, note, optional user who recorded the change.

Relationships:
- One User can create many Orders.
- One Component can appear in many Orders.
- One Component can have many Inventory records.

The supplied ER diagram shows `Order.User.id` and `Order.Component.id` as foreign keys. `Inventory.Component.id` is also a foreign key. Django's `ForeignKey` fields implement these links.

For class explanation: an order stores the price at the time of purchase so the historical order total will not change if the product price changes later.
