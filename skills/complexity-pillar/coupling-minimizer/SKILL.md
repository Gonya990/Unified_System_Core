---
name: coupling-minimizer
description: Reduces coupling to effective minimum while understanding coupling types - tight coupling OK within modules, loose coupling between modules; use when designing module interactions or managing dependencies.
---

# Coupling Minimizer

Activate when managing dependencies between modules, designing APIs, or when changes ripple across the system.

## Core Insight

**"Coupling is not inherently bad - context matters."**

Tight coupling WITHIN cohesive modules is fine. Loose coupling BETWEEN modules is essential.

## Coupling Types

### 1. Content Coupling (Worst)
One module modifies another's internal state directly.

```python
# ❌ CONTENT COUPLING
class OrderService:
    def finalize_order(self, order):
        # Reaching into Customer internals!
        order.customer._credit_used += order.total  # BAD!
        order.customer._save()  # Modifying internal state!
```

### 2. Common Coupling (Bad)
Modules share global state.

```python
# ❌ COMMON COUPLING
GLOBAL_ORDER_STATUS = {}  # Shared mutable state

class OrderService:
    def create_order(self, data):
        order_id = generate_id()
        GLOBAL_ORDER_STATUS[order_id] = "pending"  # Shared state!

class PaymentService:
    def process(self, order_id):
        if GLOBAL_ORDER_STATUS[order_id] == "pending":  # Coupled via global!
            ...
```

### 3. Control Coupling (Bad)
One module controls another's behavior via flags.

```python
# ❌ CONTROL COUPLING
def process_order(order, use_new_algorithm=False):
    if use_new_algorithm:
        # Caller controlling internal logic
        new_algorithm(order)
    else:
        old_algorithm(order)
```

### 4. Data Coupling (Good)
Modules share only necessary data via parameters.

```python
# ✅ DATA COUPLING
def calculate_total(items: list[OrderItem]) -> Decimal:
    # Only receives data it needs
    return sum(item.price * item.quantity for item in items)
```

## DRY Is Too Simplistic

**From the book**: "DRY Is too Simplistic" - Section title

**Don't Repeat Yourself (DRY)** is good advice but can cause inappropriate coupling.

### The Problem

```python
# Two pieces of code that LOOK similar but are CONCEPTUALLY different:

# Order domain
def calculate_order_total(items: list[OrderItem]) -> Decimal:
    return sum(item.price * item.quantity for item in items)

# Invoice domain  
def calculate_invoice_total(line_items: list[LineItem]) -> Decimal:
    return sum(item.unit_price * item.quantity for item in line_items)

# DRY says: "These are the same! Extract!"

# ❌ WRONG - Now coupled through shared code
def calculate_total(items: list[Any]) -> Decimal:
    return sum(item.price * item.quantity for item in items)
    # Order and Invoice now coupled!
    # Change for one affects the other
```

**Quote**: "DRY is too simplistic. Don't couple unrelated code just because it looks similar."

### The Fix: Bounded Context Duplication

```python
# ✅ RIGHT - Similar code but SEPARATE concerns
# Order bounded context
@dataclass
class OrderItem:
    price: Decimal
    quantity: int
    
    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity

def order_total(items: list[OrderItem]) -> Decimal:
    return sum(item.subtotal for item in items)


# Invoice bounded context
@dataclass  
class InvoiceLineItem:
    unit_price: Decimal
    quantity: int
    tax_rate: Decimal
    
    @property
    def line_total(self) -> Decimal:
        return self.unit_price * self.quantity * (1 + self.tax_rate)

def invoice_total(items: list[InvoiceLineItem]) -> Decimal:
    return sum(item.line_total for item in items)


# DUPLICATION IS OK - These are different concepts!
# If invoice rules change, order unaffected.
# If order rules change, invoice unaffected.
```

## Loose Coupling Isn't the Only Kind That Matters

**From the book**: "Loose Coupling Isn't the Only Kind That Matters" - Section title

**Key insight**: Within a cohesive module, tight coupling is fine!

```python
# ✅ TIGHT COUPLING - Within Order domain (GOOD)
@dataclass
class Order:
    id: str
    items: list[OrderItem]  # Tightly coupled to OrderItem
    customer: Customer  # Tightly coupled to Customer
    
    def total(self) -> Decimal:
        # Tightly coupled to items - THIS IS GOOD!
        return sum(item.subtotal for item in self.items)
    
    def can_ship(self) -> bool:
        # Tightly coupled to customer - THIS IS GOOD!
        return self.customer.is_verified and self.total > 0


# ✅ LOOSE COUPLING - Between bounded contexts (GOOD)
class OrderService:
    def __init__(
        self,
        repository: OrderRepository,  # Loose coupling via interface
        payment: PaymentGateway,  # Loose coupling via interface
        shipping: ShippingService  # Loose coupling via interface
    ):
        # These are DIFFERENT bounded contexts
        # Should be loosely coupled
        ...
```

**Quote**: "Coupling is in some ways the cost of cohesion. In the areas of your system that are cohesive, they are likely to also be more tightly coupled."

## Async as a Tool for Loose Coupling

**From the book**: "Async as a Tool for Loose Coupling" - Section title

### Temporal Coupling

**Synchronous** = Temporal coupling

```python
# ❌ TEMPORALLY COUPLED - Must wait
def create_order(self, data: OrderData) -> Order:
    order = Order.from_data(data)
    self.repository.save(order)  # Wait for DB
    
    self.email.send_confirmation(order)  # Wait for email
    self.inventory.reserve(order.items)  # Wait for inventory
    self.analytics.track(order)  # Wait for analytics
    
    return order
    # If any step fails or is slow, everything fails/slows
```

**Asynchronous** = Temporal decoupling

```python
# ✅ TEMPORALLY DECOUPLED - Don't wait
def create_order(self, data: OrderData) -> Order:
    order = Order.from_data(data)
    self.repository.save(order)
    
    # Publish event (fire and forget)
    self.events.publish(OrderCreated(
        order_id=order.id,
        customer_id=order.customer_id,
        items=[item.to_dict() for item in order.items]
    ))
    
    return order
    # Email, inventory, analytics happen asynchronously
    # Order creation not coupled to their timing/availability


# Separate handlers (decoupled)
class EmailHandler:
    def on_order_created(self, event: OrderCreated):
        # Runs independently
        self.email.send_confirmation(event.order_id)

class InventoryHandler:
    def on_order_created(self, event: OrderCreated):
        # Runs independently
        self.inventory.reserve(event.items)
```

### Spatial Coupling

**Same process** = Spatial coupling

```python
# All in same process/memory space
order_service.create_order()
email_service.send()  # Same process
inventory_service.reserve()  # Same process
```

**Different processes** = Spatial decoupling

```python
# OrderService publishes to message queue
order_service.create_order()  # Process 1
→ RabbitMQ/Kafka

# EmailService subscribes from different process
email_service.handle()  # Process 2 (different machine even!)

# InventoryService subscribes from different process
inventory_service.handle()  # Process 3 (different machine!)
```

## Prefer Loose Coupling

**From the book**: "Prefer Loose Coupling" - Section title

### Strategies

**1. Depend on Abstractions**
```python
# ✅ Depend on interface, not implementation
class OrderService:
    def __init__(self, payment: PaymentGateway):  # Interface
        self.payment = payment

# Can swap implementation without changing OrderService
```

**2. Use Events/Messages**
```python
# ✅ Publish event, don't call directly
self.events.publish(OrderPlaced(order_id))
# Subscribers decide what to do
# Publisher doesn't know or care who listens
```

**3. Invert Dependencies**
```python
# ✅ High-level doesn't depend on low-level
# Both depend on abstraction

# High-level
class OrderService:
    def __init__(self, repository: OrderRepository):  # Abstraction
        ...

# Low-level
class PostgresOrderRepository(OrderRepository):  # Implements abstraction
    ...

# Dependency points from low-level → high-level (inverted!)
```

**4. Avoid Shared Mutable State**
```python
# ✅ Immutable data structures
@dataclass(frozen=True)  # Immutable!
class Order:
    id: str
    items: list[OrderItem]

# If you want to "change" it, create new instance
updated_order = order.model_copy(update={"status": "confirmed"})
```

## How Does This Differ from Separation of Concerns?

**From the book**: "How Does This Differ from Separation of Concerns?" - Section title

**Separation of Concerns**: WHAT to separate (essential vs accidental)

**Coupling**: HOW MUCH connection remains after separation

```python
# Good separation of concerns
class OrderService:  # Essential complexity
    def __init__(self, repository: OrderRepository):  # Accidental (separate)
        self.repository = repository

# But coupling can still be:

# ❌ HIGH COUPLING - Knows too much about repository
def create_order(self, data):
    # Knows about transaction management
    self.repository.begin_transaction()
    try:
        order = Order(data)
        self.repository.insert(order)
        self.repository.commit()
    except:
        self.repository.rollback()


# ✅ LOW COUPLING - Knows only the contract
def create_order(self, data):
    order = Order(data)
    return self.repository.save(order)
    # Repository handles transactions internally
```

## Designing for Loose Coupling

**From the book**: "Designing for Loose Coupling" - Section

### Design Principles

**1. Depend on Stable Abstractions**
```python
# ✅ Stable interface (rarely changes)
class PaymentGateway(Protocol):
    def charge(self, amount: Decimal, token: str) -> PaymentResult:
        ...

# Unstable implementation (changes often)
class StripePaymentGateway(PaymentGateway):
    # Stripe SDK updates don't affect interface
    ...
```

**2. Design Events for Loose Coupling**
```python
# ✅ Event contains all needed data
@dataclass(frozen=True)
class OrderCreated:
    order_id: str
    customer_id: str
    total: Decimal
    items: list[dict]
    created_at: datetime
    
    # Subscribers don't need to call back to Order service
    # All data in event (loose coupling)
```

**3. Avoid Chatty APIs**
```python
# ❌ CHATTY - Multiple calls, tight coupling
order = order_service.get_order(id)
customer = customer_service.get_customer(order.customer_id)
items = [product_service.get(item_id) for item_id in order.item_ids]
# 1 + N calls, tightly coupled


# ✅ COHESIVE - Single call, loose coupling
order_details = order_service.get_order_details(id)
# Returns complete DTO with all data
# One call, loosely coupled
```

## Loose Coupling in Human Systems

**From the book**: "Loose Coupling in Human Systems" - Section

**High-performing teams** (from State of DevOps):
- Can make decisions without asking outside team
- Don't need sign-offs from other teams
- Deploy independently
- Have clear service boundaries

**Quote**: "One of the leading predictors of high performance...is the ability of teams to make their own decisions without the need to ask permission of anyone outside the team."

### Team Coupling

```python
# ❌ TIGHTLY COUPLED TEAMS
# Frontend team must wait for backend team
# Backend team must wait for DBA
# Everyone blocks everyone

# ✅ LOOSELY COUPLED TEAMS  
# Each team owns complete vertical slice
# Team 1: Orders (frontend + backend + DB)
# Team 2: Payments (frontend + backend + DB)
# Team 3: Shipping (frontend + backend + DB)
# Communicate via APIs/events, deploy independently
```

## Anti-Patterns

❌ **"God Object"** - Everything coupled to one central object
```python
class Application:  # 5000 lines
    # Everything couples to this monster
    ...
```

❌ **"Stamp Coupling"** - Passing entire objects when only need part
```python
def calculate_shipping(order: Order):  # Only needs weight!
    return order.weight * RATE_PER_KG

# ✅ Better
def calculate_shipping(weight_kg: Decimal):
    return weight_kg * RATE_PER_KG
```

❌ **"Train Wreck"** - Chaining calls (Law of Demeter violation)
```python
# ❌
total = order.customer.address.country.tax_rate * order.total
# Coupled to: Order, Customer, Address, Country

# ✅
total = order.calculate_total_with_tax()
# Coupled only to: Order
```

## Integration with Other Skills

- **Enabled by**: `separation-of-concerns-enforcer`, `abstraction-patterns`
- **Balances**: `cohesion-coach` (cohesion vs coupling trade-off)
- **Requires**: `modularity-architect` (modules reduce coupling)
- **Validated by**: `feedback-driven-design` (tests reveal coupling)

## Success Metrics

- **Change impact**: >80% of changes isolated to single module
- **Build time**: Can build/test modules independently
- **Team velocity**: Teams deploy without coordinating
- **Dependency graph**: Acyclic, shallow depth

## Related References

See [reference/principles.md](reference/principles.md) for coupling theory and DRY discussion.
See [reference/examples.md](reference/examples.md) for async decoupling patterns.
