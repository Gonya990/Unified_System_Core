---
name: cohesion-coach
description: Guides keeping related concepts together and unrelated concepts apart using Kent Beck's principle; use when designing classes, organizing code, or diagnosing unclear modules.
---

# Cohesion Coach

Activate when code is hard to understand, modules seem unfocused, or you're unsure what belongs together. Cohesion is slippery but critical.

## Core Principle

**Kent Beck's definition (quoted as Farley's favorite)**:

**"Pull the things that are unrelated further apart, and put the things that are related closer together."**

## Formal Definitions

**From the book**:

**Coupling**: "Given two lines of code, A and B, they are coupled when B must change behavior only because A changed."

**Cohesion**: "They are cohesive when a change to A allows B to change so that both add new value."

**Cohesion (Computer Science)**: "The degree to which the elements inside a module belong together."

## The Diagnostic Test

**Quote**: "If you have ever read a piece of code and thought 'I don't know what this code does,' it is probably because the cohesion is poor."

### Good Cohesion

```python
class ShoppingCart:
    """Everything here is about shopping cart behavior"""
    
    def __init__(self, items: list[CartItem]):
        self.items = items
    
    def add_item(self, item: CartItem) -> "ShoppingCart":
        return ShoppingCart(items=self.items + [item])
    
    def remove_item(self, item_id: str) -> "ShoppingCart":
        return ShoppingCart(
            items=[i for i in self.items if i.id != item_id]
        )
    
    @property
    def total(self) -> Decimal:
        return sum(item.subtotal for item in self.items)

# Can read this and immediately know: "This is a shopping cart"
```

### Poor Cohesion

```python
class OrderManager:
    """What does this do? Too many unrelated things!"""
    
    def __init__(self):
        self.db_connection = ...
        self.email_client = ...
        self.payment_api = ...
        self.shipping_calculator = ...
        self.tax_service = ...
        self.inventory = ...
    
    def process_order(self, data): ...
    def send_confirmation_email(self, email): ...
    def charge_credit_card(self, card): ...
    def calculate_shipping(self, address): ...
    def update_inventory(self, items): ...
    def generate_invoice_pdf(self, order): ...
    
# Can't understand what this is about without reading everything
# "I don't know what this code does" → Poor cohesion
```

## Context Matters

**From the book**: Cohesion is contextual, more than other complexity tools.

**Quote**: "Cohesion, more than the other tools to manage complexity, is contextual. Depending on context, 'All of these things may not be like the other.'"

### Sesame Street Test

Friend's recommendation quoted in book: "One of these things is not like another" (Sesame Street song)

**Point**: What's cohesive depends on perspective:

```python
# Context 1: Shopping perspective
class ShoppingCart:
    items: list[CartItem]
    total: Decimal
    discount_code: str
    # Cohesive - all about shopping experience

# Context 2: Persistence perspective  
class CartData:
    cart_json: str
    user_id: str
    created_at: datetime
    # Cohesive - all about storage

# Same domain, different cohesive groupings based on context
```

## Domain-Driven Design as Cohesion Guide

**From the book**: DDD helps identify natural cohesion boundaries.

### Bounded Contexts

**Definition**: "A part of a system that shares common concepts."

**Example**: "'Order' in order-management system probably has a different concept of 'order' from a billing system, so these are two, distinct bounded contexts."

**Value**: "They are naturally more loosely coupled in the real problem domain and so they are likely to guide us to create more loosely coupled systems."

### Ubiquitous Language

**Quote**: "We aim to create a 'ubiquitous language' to express ideas in the problem domain. This is an agreed, accurate way of describing ideas...using words consistently, and with agreed meanings."

**Example**: 
```python
# If business says "limit order matched"
# Code should say:

class LimitOrder:
    def match(self, other: Order) -> Match:
        ...

# Same words in code as in domain = cohesive
```

## The Evolution: Three Examples

**From the book** - Shopping cart adding item:

### Version 1: No Cohesion (Bad)

```python
def add_to_cart1(self, item):
    self.cart.add(item)
    
    # Database code mixed in
    conn = sqlite3.connect('my_db.sqlite')
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO cart (name, price) values (?, ?)',
        (item.name, item.price)
    )
    conn.commit()
    conn.close()
    
    # Calculation mixed in
    return self.calculate_cart_total()
```

**Analysis**: "This code bundles together the core focus of the function, adding something to a cart, with the esoteric detail of how things are stored in a relational database. It then, as a side effect, calculates some kind of total. Nasty!"

### Version 2: Better Cohesion

```python
def add_to_cart2(self, item):
    self.cart.add(item)
    self.store.store_item(item)  # Abstracted storage
    return self.calculate_cart_total()
```

**Analysis**: "A considerable step forward. Now we are initiating the storage but don't care how that works...This code is considerably more flexible as a result. It still knows that storage and cart-total calculation are involved, though."

### Version 3: Best Cohesion

```python
def add_to_cart3(self, item, listener):
    self.cart.add(item)
    listener.on_item_added(self, item)  # Just signals
```

**Analysis**: "The code executes the core behavior, adding something to the cart, and then merely signals that something was added. This code doesn't know and doesn't care what happens next. It is entirely decoupled from storage and total calculation. This code is considerably more cohesive and more modular as a result."

**Quote**: "The difference between the second two examples is more nuanced. This is more of a matter of context and choice."

## Cohesion vs Coupling Trade-Off

**Quote**: "Coupling is in some ways the cost of cohesion. In the areas of your system that are cohesive, they are likely to also be more tightly coupled."

### The Balance

```python
# HIGH COHESION + TIGHT COUPLING (within module)
class Order:
    def __init__(self, items: list[OrderItem]):
        self.items = items
        self._total = self._calculate_total()  # Tightly coupled
    
    def _calculate_total(self) -> Decimal:
        # Private method, tightly coupled to Order
        return sum(item.price * item.quantity for item in self.items)
    
    @property
    def total(self) -> Decimal:
        return self._total

# This is GOOD - cohesive internals can be tightly coupled


# LOW COHESION + LOOSE COUPLING (between modules)
class OrderService:
    def __init__(self, repository: OrderRepository):  # Loose coupling
        self.repository = repository  # Different concern
    
    def create_order(self, data: OrderData) -> Order:
        order = Order(items=data.items)  # Cohesive domain logic
        return self.repository.save(order)  # Loosely coupled to persistence
```

## TDD Drives Cohesion

**From the book**: "The discipline of TDD encourages us to hit the sweet spot for cohesion."

### How TDD Helps

```python
# Test for one behavior (cohesive)
def test_order_total_includes_all_items():
    """
    Focused test = cohesive implementation
    """
    order = Order(items=[
        OrderItem(price=Decimal("10"), quantity=2),
        OrderItem(price=Decimal("5"), quantity=1),
    ])
    
    assert order.total == Decimal("25")
    # Test forces Order to be cohesive around total calculation


# If test needs to do too much:
def test_order_creation_and_storage_and_email():
    """
    Unfocused test = poor cohesion signal
    """
    # Setup database
    # Setup email service
    # Setup payment gateway
    # Create order
    # Verify storage
    # Verify email sent
    # Verify payment processed
    
    # TOO MUCH! Poor cohesion in implementation.
```

**Quote**: "We create a test case before we write the code that describes the behavior that we aim to observe in the system...If we write too much code, more than is needed to meet the specification, we are cheating our development process and reducing the cohesion of the implementation."

## The Cost of Poor Cohesion

### Symptom 1: Can't Understand Code Quickly

```python
# ❌ What does this do?
class DataProcessor:
    def process(self, input_file, output_format, email, db_conn, api_key):
        # 500 lines of mixed concerns
        pass

# Takes 10+ minutes to understand because concerns are jumbled
```

### Symptom 2: Changes Ripple Everywhere

```python
# ❌ Change one thing, break many things
class OrderProcessor:
    def handle(self, data):
        # Mixed: parsing, validation, business logic, persistence, notification
        pass

# Change email format → must touch this
# Change database schema → must touch this
# Change business rule → must touch this
# Everything coupled because nothing cohesive
```

### Symptom 3: Hard to Test

```python
# ❌ Need entire infrastructure to test one rule
def validate_and_store_order(data):
    # Needs: database, email server, payment API
    # Just to test validation logic!
    pass
```

## Cohesion in Human Systems

**From the book**: Teams need cohesion too.

**Quote**: "Another way to think of that is that the information and skills of the team are cohesive, in that the team has all that it needs within its bounds to make decisions and to make progress."

### Team Cohesion

**High-performance teams** (from State of DevOps report):
- Can make decisions without asking outside team
- Have all skills needed within team
- Information is cohesive (not scattered across teams)

**Poor cohesion**:
- Need to coordinate with 5 other teams for simple change
- Skills distributed across teams (frontend team, backend team, DBA team)
- Information scattered (no one team has full picture)

## Practical Guidelines

### One Class, One Responsibility

```python
# ✅ COHESIVE - Single responsibility
class OrderValidator:
    """Only validates orders"""
    def validate(self, order: Order) -> ValidationResult:
        ...

class OrderRepository:
    """Only persists orders"""
    def save(self, order: Order) -> Order:
        ...

class OrderNotifier:
    """Only sends notifications"""
    def notify_created(self, order: Order) -> None:
        ...


# ❌ NOT COHESIVE - Multiple responsibilities
class OrderManager:
    """Validates, persists, and notifies"""
    def validate_and_save_and_notify(self, order):
        # Too many concerns!
        ...
```

### Variables Belong to Methods

**From the book**:

```python
# ❌ POOR COHESION - Variables unrelated to methods
class PoorCohesion:
    def __init__(self):
        self.a = 0  # Only used by process_a
        self.b = 0  # Only used by process_b
    
    def process_a(self, x):
        self.a = self.a + x
    
    def process_b(self, x):
        self.b = self.b * x
    
    # Variables stored together but are unrelated!


# ✅ BETTER COHESION - Each class has related data
class BetterCohesionA:
    def __init__(self):
        self.a = 0  # Used by this class's methods
    
    def process_a(self, x):
        self.a = self.a + x

class BetterCohesionB:
    def __init__(self):
        self.b = 0  # Used by this class's methods
    
    def process_b(self, x):
        self.b = self.b * x
```

## Refactoring for Cohesion

### Step 1: Identify Related Concepts

Look for:
- Methods that use same variables
- Functions that call each other
- Code that changes together
- Concepts from same bounded context (DDD)

### Step 2: Extract to Separate Module

```python
# Before: Mixed concerns in one class
class OrderService:
    def calculate_total(self, items): ...
    def send_email(self, recipient): ...
    def log_to_file(self, message): ...

# After: Cohesive modules
class OrderCalculator:
    def calculate_total(self, items): ...

class EmailService:
    def send(self, recipient, message): ...

class AuditLogger:
    def log(self, message): ...
```

### Step 3: Validate with Tests

```python
# Can you test each module independently?
def test_order_calculator():
    # No email, no logging, no database
    calc = OrderCalculator()
    total = calc.calculate_total([item1, item2])
    assert total == expected
    # YES - cohesive!
```

## Anti-Patterns

❌ **"God Class"** - One class does everything
- 1000+ lines, 50+ methods
- **Fix**: Extract responsibilities to separate classes

❌ **"Utility Class"** - Random static methods
```python
class Utils:
    @staticmethod
    def format_date(d): ...
    @staticmethod
    def calculate_tax(amount): ...
    @staticmethod
    def send_email(to): ...
    # No cohesion - unrelated functions
```

❌ **"Feature Envy"** - Method uses another class's data more than its own
```python
class Order:
    def calculate_shipping(self, customer):
        # Uses mostly customer data, not order data
        return customer.address.state.tax_rate * self.total
        # Should be in Customer or ShippingCalculator
```

❌ **"Shotgun Surgery"** - One change requires touching many classes
- Symptom of poor cohesion
- Related concepts scattered across codebase

## Integration with Other Skills

- **Pairs with**: `modularity-architect` (modules should be cohesive)
- **Requires**: `separation-of-concerns-enforcer` (separate to achieve cohesion)
- **Enabled by**: `feedback-driven-design` (TDD reveals cohesion issues)
- **Balances**: `coupling-minimizer` (cohesion vs coupling trade-off)

## Success Metrics

- **Understanding time**: <30 seconds to understand what class does
- **Change locality**: >80% of changes within single cohesive unit
- **Test simplicity**: Can test unit without complex setup
- **Name clarity**: Can name class/function in one clear word/phrase

## Related References

See [reference/principles.md](reference/principles.md) for Kent Beck quote and cohesion theory.
See [reference/examples.md](reference/examples.md) for shopping cart evolution example.
