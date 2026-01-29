---
name: abstraction-patterns
description: Information hiding at every scale - from functions to microservices - preventing "big balls of mud" and leaky abstractions; use when designing interfaces, APIs, or detecting coupling issues.
---

# Abstraction Patterns

Activate when designing interfaces, creating APIs, or when internal details are escaping module boundaries. Abstraction = information hiding.

## Core Principle

**"Always Prefer to Hide Information"** - From the book's chapter on Information Hiding and Abstraction

**Key Distinction**: Abstraction OR information hiding? They're related but different:
- **Abstraction**: Simplifying by removing detail
- **Information Hiding**: Deliberately concealing detail

**Both are essential** for managing complexity.

## What Causes "Big Balls of Mud"?

**From the book**: Two root causes:

### 1. Organizational and Cultural Problems

- Not valuing design quality
- Rushing to "just make it work"
- No time for refactoring
- Lack of design skills
- No architectural vision

### 2. Technical Problems and Problems of Design

- **Poor abstraction** - Internal details leak everywhere
- **No information hiding** - Everything knows about everything
- **Tight coupling** - Can't change anything without breaking everything

**Quote**: "What Causes 'Big Balls of Mud'?" - Entire book section dedicated to this

## The Power of Abstraction

**From the book**: "Abstraction is one of the most powerful tools that we have to manage complexity."

### Good Abstraction Hides Detail

```python
# ✅ HIGH-LEVEL ABSTRACTION - Details hidden
def create_order(customer_id: str, items: list[OrderItem]) -> Order:
    """
    User doesn't need to know:
    - How order is stored
    - How ID is generated
    - How validation works
    - How events are published
    
    Just: give me customer and items, get order
    """
    ...


# ❌ NO ABSTRACTION - All details exposed
def create_order(
    customer_id: str,
    items: list[OrderItem],
    db_session: Session,  # Leaked detail
    id_generator: IdGenerator,  # Leaked detail
    validator: OrderValidator,  # Leaked detail
    event_bus: EventBus,  # Leaked detail
    transaction_manager: TransactionManager,  # Leaked detail
) -> tuple[Order, list[Event], ValidationResult]:  # Complex return
    """
    User must know about:
    - Database sessions
    - ID generation strategy
    - Validation mechanism
    - Event publishing
    - Transaction management
    
    Too much! Abstraction leaked.
    """
    ...
```

## Leaky Abstractions

**From the book**: "Even good abstractions can leak in ways that expose underlying details."

### Classic Example: ORM Leaking

```python
# ❌ LEAKY ABSTRACTION - SQLAlchemy details escape
def get_order(order_id: str) -> Order:
    return session.query(Order).filter_by(id=order_id).first()
    # Returns SQLAlchemy model object
    # Client must know:
    # - How to handle lazy loading
    # - Session management
    # - None vs empty results
    # - Detached entities


# ✅ SEALED ABSTRACTION - Implementation hidden
def get_order(order_id: str) -> Optional[Order]:
    db_order = session.query(OrderTable).filter_by(id=order_id).first()
    if db_order is None:
        return None
    # Translate to domain model (pure dataclass)
    return Order(
        id=db_order.id,
        items=[OrderItem.from_db(item) for item in db_order.items],
        total=Decimal(db_order.total_cents) / 100
    )
    # Returns domain model (frozen dataclass)
    # Client knows nothing about database
```

### REST API Leaking

```python
# ❌ LEAKY - Database structure exposed in API
@app.get("/orders/{id}")
def get_order_endpoint(id: str):
    order = db.query(OrderTable).get(id)
    return order  # Serializes SQLAlchemy object
    # API response reveals:
    # - Database column names
    # - Foreign key relationships
    # - Internal IDs
    # - Nullable vs required (from DB schema)


# ✅ SEALED - API contract independent of implementation
@app.get("/orders/{id}")
def get_order_endpoint(
    id: str,
    service: OrderService = Depends()
):
    order = service.get_order(id)
    if order is None:
        raise HTTPException(404, "Order not found")
    
    # Explicit API model
    return OrderResponse(
        id=order.id,
        total=str(order.total),  # Decimal → string for JSON
        status=order.status.name,  # Enum → string
        items=[
            ItemResponse(
                name=item.product.name,
                quantity=item.quantity,
                price=str(item.price)
            )
            for item in order.items
        ]
    )
    # API contract stable even if database changes
```

## Picking Appropriate Abstractions

**From the book**: "Choosing the right abstractions is hard but critical."

### Abstractions from the Problem Domain

**Quote**: "Abstractions from the Problem Domain" - Section title

**Principle**: Abstract in terms of **what** the system does, not **how** it does it.

```python
# ✅ DOMAIN ABSTRACTION - Business language
class OrderService:
    def place_order(self, customer_id: str, items: list[Item]) -> Order:
        """Business language: 'place an order'"""
        ...
    
    def cancel_order(self, order_id: str) -> Order:
        """Business language: 'cancel an order'"""
        ...
    
    def ship_order(self, order_id: str, carrier: str) -> Order:
        """Business language: 'ship an order'"""
        ...


# ❌ TECHNICAL ABSTRACTION - Implementation language
class OrderService:
    def insert_order_record(self, data: dict) -> int:
        """Database language: 'insert record'"""
        ...
    
    def update_order_status(self, id: int, status: int) -> None:
        """Database language: 'update status'"""
        ...
    
    def select_orders_by_customer(self, customer_id: int) -> list[dict]:
        """SQL language: 'select records'"""
        ...
```

**DDD Ubiquitous Language** (from book):

**Quote**: "If I am talking about my software and I say that this 'Limit-order matched,' then that makes sense in terms of the code, where the concepts of 'limit orders' and 'matching' are clearly represented, and named LimitOrder and Match."

### Abstract Accidental Complexity

**From the book**: Section on abstracting infrastructure concerns.

```python
# Accidental complexity (infrastructure) should be abstracted

# ✅ ABSTRACTED - Service doesn't know about HTTP/JSON/DB
class OrderService:
    def __init__(
        self,
        repository: OrderRepository,  # Abstraction over DB
        payment: PaymentGateway,  # Abstraction over HTTP API
        events: EventBus  # Abstraction over messaging
    ):
        ...
    
    # Business logic in terms of domain, not infrastructure
    def create_order(self, data: OrderData) -> Order:
        order = Order.create(data)
        persisted = self.repository.save(order)  # Don't care HOW
        self.events.publish(OrderCreated(persisted.id))  # Don't care HOW
        return persisted


# ❌ NOT ABSTRACTED - Service tied to infrastructure details
class OrderService:
    def create_order(self, data: dict):
        # Knows about PostgreSQL
        conn = psycopg2.connect(...)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders ...")
        
        # Knows about Stripe API
        stripe.api_key = "sk_live_..."
        charge = stripe.Charge.create(...)
        
        # Knows about RabbitMQ
        connection = pika.BlockingConnection(...)
        channel = connection.channel()
        channel.basic_publish(...)
```

### Isolate Third-Party Systems and Code

**From the book**: "Isolate Third-Party Systems and Code" - Section title

**Why**: Third-party libraries change independently of your code. Isolate them behind your own abstractions.

```python
# ✅ ISOLATED - Third-party library behind our abstraction

# Our abstraction (stable interface)
class PaymentGateway(Protocol):
    """Our interface - won't change when library changes"""
    def charge(self, amount: Decimal, token: str) -> PaymentResult:
        ...


# Adapter for third-party library (unstable implementation)
class StripePaymentGateway(PaymentGateway):
    """Isolates Stripe SDK - only this changes when Stripe updates"""
    
    def __init__(self, api_key: str):
        import stripe  # Third-party dependency
        self.stripe = stripe
        self.stripe.api_key = api_key
    
    def charge(self, amount: Decimal, token: str) -> PaymentResult:
        try:
            # Translate our domain to Stripe's API
            charge = self.stripe.Charge.create(
                amount=int(amount * 100),  # Cents
                currency="usd",
                source=token
            )
            
            # Translate Stripe's response to our domain
            return PaymentResult(
                success=True,
                transaction_id=charge.id
            )
        except stripe.CardError as e:
            # Translate Stripe exceptions to our exceptions
            return PaymentResult(
                success=False,
                error=str(e)
            )


# Service depends on OUR abstraction, not third-party
class OrderService:
    def __init__(self, payment: PaymentGateway):
        self.payment = payment  # Any implementation works
    
    # If Stripe API changes, only StripePaymentGateway changes
    # If we switch to different gateway, only swap adapter
    # Service code unchanged!
```

## Abstraction at Different Scales

**From the book**: "Modularity is fractal...same is true for abstraction."

### Function Level

```python
# Hide loop details
def total_price(items: list[Item]) -> Decimal:
    return sum(item.price for item in items)
    # Caller doesn't know: loop, sum function, etc.
```

### Class Level

```python
# Hide state and behavior
class ShoppingCart:
    def __init__(self):
        self._items: list[Item] = []  # Private!
    
    def add(self, item: Item) -> None:
        self._items.append(item)  # Caller doesn't know list structure
    
    @property
    def total(self) -> Decimal:
        return sum(item.price for item in self._items)
        # Caller doesn't know: internal collection, calculation
```

### Service Level

```python
# Hide entire bounded context
class OrderService:
    """
    Entire order management hidden behind this interface.
    Caller doesn't know:
    - How orders are stored
    - How validation works
    - How events are published
    - How transactions are managed
    """
    
    def create_order(self, data: OrderData) -> Order: ...
    def cancel_order(self, order_id: str) -> Order: ...
    def get_order(self, order_id: str) -> Optional[Order]: ...
```

### System Level (Microservices)

```http
# Hide entire service behind API
POST /api/orders HTTP/1.1

{
  "customer_id": "cust_123",
  "items": [...]
}

# Client doesn't know:
# - What language service is written in
# - What database it uses
# - How it's deployed
# - How many instances are running
```

## Fear of Over-Engineering

**From the book**: "Fear of Over-Engineering" - Section addressing common objection.

**Common worry**: "If I abstract everything, won't my code be overly complex?"

**Answer**: Good abstraction REDUCES complexity, not increases it.

### Over-Abstraction (Bad)

```python
# ❌ TOO MANY LAYERS - Abstraction for abstraction's sake
class OrderServiceFactoryBuilderProviderManager:
    def create_service_factory_builder_provider(self):
        return ServiceFactoryBuilderProvider(
            OrderServiceFactory(
                OrderServiceBuilder(
                    OrderService()
                )
            )
        )
# This is not abstraction, this is madness!
```

### Right Abstraction (Good)

```python
# ✅ APPROPRIATE LAYERS - Each abstracts meaningful concept

# Domain layer (abstracts business rules)
@dataclass(frozen=True)
class Order:
    id: str
    items: list[OrderItem]
    
    def total(self) -> Decimal:
        return sum(item.subtotal for item in self.items)


# Service layer (abstracts use cases)
class OrderService:
    def create_order(self, data: OrderData) -> Order:
        ...


# Repository layer (abstracts persistence)
class OrderRepository(Protocol):
    def save(self, order: Order) -> Order:
        ...


# Each layer has clear purpose, meaningful abstraction
```

## Improving Abstraction Through Testing

**From the book**: "Improving Abstraction Through Testing" - Section title

**Key insight**: If hard to test, abstraction is poor.

```python
# ❌ HARD TO TEST - Poor abstraction (details leaked)
def process_payment(order_id: str) -> bool:
    order = db.query(Order).get(order_id)  # Needs database
    response = requests.post(f"{STRIPE_API}/charge", ...)  # Needs network
    with open('audit.log', 'a') as f:  # Needs filesystem
        f.write(f"Payment: {order_id}")
    return response.status_code == 200
    # Must set up database, network, filesystem to test!


# ✅ EASY TO TEST - Good abstraction (details hidden)
def process_payment(
    order: Order,  # Abstraction (can be fake)
    gateway: PaymentGateway,  # Abstraction (can be fake)
    audit: AuditLog  # Abstraction (can be fake)
) -> PaymentResult:
    result = gateway.charge(order.total, order.payment_token)
    audit.log(f"Payment: {order.id} = {result.status}")
    return result
    # Test with fakes - no infrastructure needed!
```

**Quote**: "Testing, when done well, exposes something important and true about the nature of our code, the nature of our designs, and the nature of the problem that we are solving that is not otherwise easily accessible."

## What to Abstract

### DO Abstract

- **Infrastructure concerns**: Database, HTTP, filesystem, messaging
- **Third-party libraries**: Payment gateways, email services, external APIs
- **Complex algorithms**: Hide implementation, expose intent
- **State management**: Internal collections, caches, flags
- **Platform details**: Operating system, network, concurrency

### DON'T Abstract (Yet)

- **Domain rules**: Keep business logic explicit, not hidden
- **Simple functions**: `add(a, b)` doesn't need abstraction layer
- **Obvious mappings**: Direct translations don't need hiding
- **Things that never change**: Don't abstract constants that never change

**Rule of thumb**: Abstract when you have TWO implementations (or anticipate needing them).

## Anti-Patterns

❌ **"Lasagna Architecture"** - Too many layers of abstraction
```python
# Controller → Service → Manager → Handler → Processor → Worker
# Each layer does almost nothing, just passes through
```

❌ **"Primitive Obsession"** - Not abstracting domain concepts
```python
def create_order(
    customer: str,  # Should be Customer object
    items: list[tuple[str, int, float]],  # Should be list[OrderItem]
    status: int  # Should be OrderStatus enum
):
    # Using primitives instead of domain abstractions
    pass
```

❌ **"Inappropriate Intimacy"** - Abstraction violated
```python
class OrderService:
    def create_order(self, data):
        order = Order(**data)
        # Reaching into repository internals!
        self.repository._session.add(order)  # BAD!
        self.repository._session.commit()  # BAD!
        # Should use: self.repository.save(order)
```

❌ **"Shotgun Surgery"** - Abstraction missing
```python
# Changing payment provider requires changes in 20 files
# Should have been abstracted behind PaymentGateway interface
# Would only need to change one adapter implementation
```

## Testing Abstraction Quality

### Checklist

- [ ] **Can describe interface without mentioning implementation?**
  - Yes: "Place an order" (good)
  - No: "Insert into orders table" (leaky)

- [ ] **Can swap implementations without changing clients?**
  - Yes: Interface is stable (good)
  - No: Clients know too much (leaky)

- [ ] **Can test clients with fake implementation?**
  - Yes: Well abstracted (good)
  - No: Tied to real infrastructure (leaky)

- [ ] **Interface uses domain language, not technical language?**
  - Yes: `place_order()` (good)
  - No: `insert_order_record()` (technical)

## Integration with Other Skills

- **Requires**: `separation-of-concerns-enforcer` (separate to abstract)
- **Enables**: `coupling-minimizer` (abstraction reduces coupling)
- **Pairs with**: `modularity-architect` (modules hide via abstraction)
- **Validated by**: `feedback-driven-design` (tests reveal poor abstraction)

## Success Metrics

- **Swap implementations**: <1 day to change infrastructure (like database swap story)
- **Test without infrastructure**: >90% of tests use fakes, not real DB/HTTP
- **Interface stability**: API changes <1% when implementation changes 100%
- **Understanding**: Can explain interface without describing implementation

## Related References

See [reference/principles.md](reference/principles.md) for book quotes on abstraction vs information hiding.
See [reference/examples.md](reference/examples.md) for leaky abstraction examples and fixes.
