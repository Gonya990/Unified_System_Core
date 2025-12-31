---
name: separation-of-concerns-enforcer
description: "Farley's most powerful design principle: 'One class, one thing. One method, one thing.' Separates essential from accidental complexity; use for all design decisions, code reviews, and refactoring work."
---

# Separation of Concerns Enforcer

**This is the primary design tool in Modern Software Engineering.** Activate for every design decision, code review, and refactoring.

## Core Principle

**"Separation of concerns is the most powerful principle of design in my own work. I apply it everywhere." - David Farley**

**The Rule**: "One class, one thing. One method, one thing."

## Essential vs Accidental Complexity

**From Fred Brooks' "No Silver Bullet", emphasized throughout the book:**

### Essential Complexity
"The complexity that is inherent in solving the problem"

**Examples**:
- Calculating interest on a bank account
- Adding items to shopping cart
- Matching buy and sell orders
- Validating customer data
- Determining shipping cost

**This is the real value your system provides.**

### Accidental Complexity
"Everything else—the problems that we are forced to solve as a side effect of doing something useful with computers"

**Examples**:
- Persisting data to database
- Serializing to JSON/XML
- Making HTTP requests
- Managing transactions
- Handling concurrency
- Clustering for scale
- Some security concerns

**Quote**: "It is in our interests to work to minimize, without ignoring, accidental complexity."

## The Golden Rule

**Separate essential from accidental complexity in EVERY component:**

```python
# ❌ MIXED CONCERNS - Essential + Accidental jumbled together
def add_to_cart(item_id: str, quantity: int):
    # Accidental: Database connection
    conn = sqlite3.connect('cart.db')
    cur = conn.cursor()
    
    # Essential: Business logic (hidden in SQL!)
    cur.execute(
        'INSERT INTO cart (item_id, quantity, price) VALUES (?, ?, ?)',
        (item_id, quantity, get_price(item_id))
    )
    
    # Accidental: Database transaction
    conn.commit()
    conn.close()
    
    # Essential: Total calculation (also hidden!)
    cur.execute('SELECT SUM(price * quantity) FROM cart')
    total = cur.fetchone()[0]
    
    # Accidental: Serialization
    return json.dumps({"total": total})


# ✅ SEPARATED CONCERNS - Clear boundaries
def add_to_cart(cart: Cart, item: Item, quantity: int) -> Cart:
    """
    Pure business logic - ESSENTIAL complexity only.
    
    No database, no HTTP, no JSON - just domain logic.
    """
    updated_items = cart.items + [CartItem(item=item, quantity=quantity)]
    return Cart(items=updated_items)


# Accidental complexity handled in ADAPTER layer:
@app.post("/cart/items")
def add_item_to_cart_endpoint(
    request: AddItemRequest,
    cart_service: CartService = Depends()  # Dependency injection
):
    """API layer - handles HTTP, JSON, transactions"""
    # Translate from HTTP/JSON (accidental)
    item = cart_service.get_item(request.item_id)
    cart = cart_service.get_cart(request.user_id)
    
    # Call pure business logic (essential)
    updated_cart = add_to_cart(cart, item, request.quantity)
    
    # Persist (accidental)
    cart_service.save_cart(updated_cart)
    
    # Serialize (accidental)
    return {"total": updated_cart.total}
```

## The Database Swap Story

**Real example from the book - Financial exchange built by Farley:**

**Context**: Didn't like commercial terms with database vendor

**Action**:
1. Downloaded open-source RDBMS
2. Made "a few simple changes to the code that interacted with the RDBMS"
3. Two tests failed, fixed the problems
4. Deployed to production few days later

**Timeline**: "This whole story took a single morning!"

**Quote**: "Without good separation of concerns, this would have taken months or years and probably wouldn't even have been contemplated as a result."

**Why it worked**: Database access was isolated in adapters, business logic knew nothing about databases.

## Dependency Injection as Separation Tool

**Key Insight**: "Dependency injection is where dependencies of a piece of code are supplied to it as parameters, rather than created by it."

### Common Misconception

❌ "Dependency injection needs a framework like Spring"

✅ "Dependency injection is something you can do in most languages...natively, and it is a powerful approach to design."

**Quote**: "I have even seen it used, to very good effect, in Unix shell scripts."

### Pure Python DI Example

```python
# ❌ CREATES dependencies (tightly coupled to specifics)
class OrderService:
    def __init__(self):
        self.db = PostgresDB(host="localhost", port=5432)
        self.payment = StripeAPI(key="sk_live_...")
        self.email = SendGridAPI(key="SG....")
    
    # Can ONLY work with Postgres + Stripe + SendGrid
    # Can't test without real services
    # Hard to swap implementations


# ✅ RECEIVES dependencies (loosely coupled to interfaces)
class OrderService:
    def __init__(
        self,
        repository: OrderRepository,  # Interface/Protocol
        payment_gateway: PaymentGateway,  # Interface/Protocol
        notification_service: NotificationService  # Interface/Protocol
    ):
        self.repository = repository
        self.payment_gateway = payment_gateway
        self.notification_service = notification_service
    
    # Works with ANY implementation of interfaces
    # Easy to test with fakes
    # Trivial to swap implementations
```

## The Layered Separation Pattern

### Layer 1: Domain/Core (Essential Only)

```python
# src/domain/order.py
from pydantic import BaseModel
from decimal import Decimal

class Order(BaseModel):
    """Pure domain model - no infrastructure dependencies"""
    model_config = {"frozen": True}
    
    id: str
    customer_id: str
    items: list[OrderItem]
    
    @property
    def total(self) -> Decimal:
        """Business logic - essential complexity"""
        return sum(item.subtotal for item in self.items)
    
    def add_item(self, item: OrderItem) -> "Order":
        """Pure function - returns new Order"""
        return self.model_copy(
            update={"items": self.items + [item]}
        )
```

### Layer 2: Service (Essential + Orchestration)

```python
# src/services/order_service.py
class OrderService:
    """
    Orchestrates domain logic.
    Uses ports (interfaces) for infrastructure.
    """
    def __init__(
        self,
        order_repo: OrderRepository,  # Port
        payment_gateway: PaymentGateway,  # Port
        event_bus: EventBus  # Port
    ):
        self.orders = order_repo
        self.payments = payment_gateway
        self.events = event_bus
    
    def create_order(self, data: OrderData) -> Order:
        """
        Business process - mostly essential complexity.
        Infrastructure hidden behind ports.
        """
        # Create domain object (essential)
        order = Order.from_data(data)
        
        # Persist (accidental - but hidden behind port)
        saved_order = self.orders.save(order)
        
        # Notify (accidental - but hidden behind port)
        self.events.publish(OrderCreated(order_id=saved_order.id))
        
        return saved_order
```

### Layer 3: Adapter (Accidental Only)

```python
# src/adapters/postgres_order_repository.py
class PostgresOrderRepository(OrderRepository):
    """
    Handles ALL database concerns.
    Domain/Service layers know nothing about this.
    """
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, order: Order) -> Order:
        # Translate domain model to database model (accidental)
        db_order = OrderTable(
            id=order.id,
            customer_id=order.customer_id,
            # ... mapping logic
        )
        
        # Database operations (accidental)
        self.session.add(db_order)
        self.session.commit()
        self.session.refresh(db_order)
        
        # Translate back to domain model
        return Order.from_db(db_order)
```

### Layer 4: API/Presentation (Accidental Only)

```python
# src/api/routes/orders.py
@router.post("/orders")
def create_order_endpoint(
    request: CreateOrderRequest,
    service: OrderService = Depends(get_order_service)
):
    """
    HTTP concerns only - JSON, status codes, headers.
    Business logic delegated to service.
    """
    try:
        # Translate HTTP/JSON to domain (accidental)
        order_data = OrderData(**request.dict())
        
        # Call business logic (essential - but we don't own it)
        order = service.create_order(order_data)
        
        # Translate domain to HTTP/JSON (accidental)
        return {"id": order.id, "total": str(order.total)}
        
    except ValidationError as e:
        # HTTP error handling (accidental)
        raise HTTPException(status_code=400, detail=str(e))
```

## The "One Thing" Test

For every class/function, ask: **"What is the ONE thing this does?"**

### Passes the Test

```python
def calculate_order_total(items: list[OrderItem]) -> Decimal:
    """ONE thing: Calculate total"""
    return sum(item.price * item.quantity for item in items)

class OrderRepository:
    """ONE thing: Persist and retrieve orders"""
    pass

class PaymentGateway:
    """ONE thing: Process payments"""
    pass
```

### Fails the Test

```python
def process_order(data: dict):
    """
    Does MANY things:
    - Parse JSON (accidental)
    - Validate data (essential)
    - Calculate total (essential)
    - Save to database (accidental)
    - Send email (accidental)
    - Log to file (accidental)
    - Return HTTP response (accidental)
    """
    pass  # THIS IS BAD!
```

**If you can't describe it in one sentence, it's doing too much.**

## Boundaries as Translation Points

**From the book**: "The seams or boundaries should be treated with more care. They should be translation and validation points for information."

### The Problem

```python
# ❌ Domain model = Database model = API model
class Order(Base):  # SQLAlchemy model used everywhere!
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    # ... database columns
    
# Now your API returns SQLAlchemy objects (leaky!)
# Now your domain logic deals with ORM sessions (mixed concerns!)
# Now changing DB means changing domain AND API (brittle!)
```

### The Solution

```python
# ✅ Each layer has its own model, translate at boundaries

# Domain model (essential)
@dataclass(frozen=True)
class Order:
    id: str
    total: Decimal

# Database model (accidental)
class OrderTable(Base):
    __tablename__ = 'orders'
    id = Column(String, primary_key=True)
    total_cents = Column(Integer)  # Different representation!

# API model (accidental)
class OrderResponse(BaseModel):
    id: str
    total: str  # JSON doesn't have Decimal!

# Translation happens at boundaries:
def to_domain(db_order: OrderTable) -> Order:
    return Order(
        id=db_order.id,
        total=Decimal(db_order.total_cents) / 100
    )

def to_api(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        total=f"{order.total:.2f}"
    )
```

## Testing Reveals Separation Quality

```python
# Can you test this WITHOUT database/HTTP/filesystem?

def process_payment(order_id: str) -> bool:
    order = db.query(Order).get(order_id)  # Needs database
    response = requests.post(f"{API}/charge", ...)  # Needs network
    with open('audit.log', 'a') as f:  # Needs filesystem
        f.write(f"Payment processed: {order_id}")
    return response.status_code == 200

# ❌ NO - concerns are mixed, test is brittle/slow


# Can you test this WITHOUT infrastructure?

def process_payment(
    order: Order,
    payment_gateway: PaymentGateway,
    audit_log: AuditLog
) -> PaymentResult:
    charge_amount = order.total
    result = payment_gateway.charge(charge_amount)
    audit_log.record(f"Payment: {order.id} = {result.status}")
    return result

# ✅ YES - use fakes for gateway and log, test is fast/deterministic
```

**TDD forces separation** - If hard to test, concerns are mixed.

## Anti-Patterns

❌ **"God Class"** - One class does everything
```python
class OrderManager:  # 2000 lines!
    def create(...)  # Database
    def update(...)  # Database
    def send_email(...)  # Email
    def charge_payment(...)  # Payment
    def generate_pdf(...)  # PDF
    # Essential + accidental all mixed together
```

❌ **"Leaky Repository"** - Database details escape
```python
class OrderService:
    def get_order(self, id: str):
        return session.query(Order).filter_by(id=id).first()
        # Now service knows about SQLAlchemy sessions!
```

❌ **"Anemic Domain"** - All logic in services, models are just data
```python
@dataclass
class Order:
    items: list
    # No behavior! Just bags of data.

class OrderService:
    def calculate_total(self, order: Order):
        # Business logic OUTSIDE domain model!
```

✅ **Rich Domain** - Essential logic IN domain
```python
@dataclass
class Order:
    items: list[OrderItem]
    
    def total(self) -> Decimal:
        # Business logic INSIDE domain where it belongs
        return sum(item.subtotal for item in self.items)
```

## The Ultimate Separation: Ports & Adapters

**Also called "Hexagonal Architecture"** (see `python-hexagonal-development` skill)

### Structure

```
Core (Essential)
└── Ports (Interfaces to outside world)
    └── Adapters (Accidental implementations)
```

### Example

```python
# CORE - Essential complexity
class OrderService:
    def __init__(self, repository: OrderRepository):  # Port!
        self.repository = repository
    
    def create_order(self, data: OrderData) -> Order:
        order = Order.from_data(data)
        return self.repository.save(order)  # Calls through port


# PORT - Interface defining what core needs
class OrderRepository(Protocol):
    def save(self, order: Order) -> Order: ...
    def find_by_id(self, id: str) -> Optional[Order]: ...


# ADAPTERS - Accidental implementations (swap these freely!)
class PostgresOrderRepository(OrderRepository): ...
class MongoOrderRepository(OrderRepository): ...
class InMemoryOrderRepository(OrderRepository): ...  # For tests!
```

## Quick Decision Tree

```
Is this code about:
├─ Domain rules, calculations, validations?
│  └─ YES → Essential → Lives in domain/service layer
└─ NO → Is it about:
    ├─ Database, HTTP, Files, Queues, External APIs?
    │  └─ YES → Accidental → Lives in adapter layer
    └─ Translating between layers?
        └─ YES → Boundary → Translation/validation only
```

## Integration with Other Skills

- **Enables**: All other complexity management skills
- **Pairs with**: `modularity-architect` (modules separate concerns)
- **Requires**: `feedback-driven-design` (TDD reveals violations)
- **Supports**: `dependency-injection` (native language feature)

## Success Metrics

- **Can swap database in <1 day** (like Farley's team)
- **Can test domain logic without infrastructure** (100% of business rules)
- **Can understand any function in <30 seconds** (one concern per function)
- **Low coupling metrics** (depends-on graph is acyclic, shallow)

## Related References

See [reference/principles.md](reference/principles.md) for book quotes on separation.
See [reference/examples.md](reference/examples.md) for before/after refactoring examples.
