---
name: modularity-architect
description: Creates systems where changes in one place don't break elsewhere through proper module boundaries and information hiding; use for system architecture decisions and service decomposition.
---

# Modularity Architect

Activate when designing system architecture, decomposing services, or establishing module boundaries. Modularity is fractal - applies from functions to microservices.

## Core Principle

**"A system is not modular if the internal workings of adjacent modules are exposed. Communication between modules (and services) should be a little more guarded than communication within them."**

## What Is a Module?

**From the book**: Any compartment in your system that hides detail:
- Function (hides implementation)
- Class (hides state and behavior)
- Package/Namespace (hides related classes)
- Service (hides business capability)
- Microservice (hides deployable unit)

**Critical**: "Simply throwing a collection of unrelated stuff into a file does not make the code modular in any but the most trivial sense."

## The Apollo Program Example

**Historical context from book**:

When NASA started the Apollo program, one driving innovation was **Lunar Orbit Rendezvous (LOR)** - dividing the spacecraft into task-specific modules:

1. **Saturn V** - Get everything to Earth orbit
2. **Service Module** - Earth to Moon and back
3. **Command Module** - Return astronauts from orbit to surface
4. **Lunar Excursion Module (LEM)**:
   - **Descent Module** - Lunar orbit to surface
   - **Ascent Module** - Surface back to orbit

**Benefits of modularity**:
- Each component focused on one part of problem (less compromise)
- Different companies could work independently
- Each module could be lighter (LEM didn't carry Earth-return fuel to surface)
- **Each module was simpler** than if designed for larger scope

**Quote**: "Although it is a stretch to call any Apollo spacecraft simple, each module could be simpler than if they were designed to cope with a larger part of the whole problem."

**Application to software**: Microservices, services, packages - same principle.

## The Two Scalability Strategies

**From the book - No middle ground**:

### Option 1: Monolith (Everything Together)

**Characteristics**:
- Single repository, single deployment pipeline
- Test everything together
- Deploy everything together
- Simpler architecture, no distributed system problems

**Requirement**: "We can either make the choice to build test and deploy everything that constitutes our system together...but then we must take on the responsibility to create fast enough feedback."

**Challenge**: As system grows, keeping tests fast becomes engineering problem

**When to choose**: 
- Team < 8 people
- Can keep full test suite < 10 minutes
- Domain is cohesive
- Want to avoid distributed system complexity

### Option 2: Microservices (Independent Modules)

**Characteristics**:
- Each service has own repository, pipeline
- Test each service independently
- Deploy each service independently
- Complex architecture, distributed system challenges

**Critical Definition**: "Part of the definition of a microservice is that they are 'independently deployable.' **If you are testing your microservices together, they aren't really microservices.**"

**Benefit**: "This is at least as much an organizational strategy problem as it is a technical one."

**When to choose**:
- Team > 8 people OR multiple teams
- Need organizational scalability
- Bounded contexts are clear
- Can handle distributed system complexity

**Quote**: "Nearly everyone would like some ideal middle ground between these two extremes, but in reality, it doesn't exist. The middle ground is a fudge and is often slower and more complex than the monolithic approach."

## Deployability Defines Modularity

**Critical Insight**: "The scope of an effective deployment pipeline is always an 'independently deployable unit of software.'"

### The Deployment Test

If your deployment pipeline output is "releasable," it must also be "independently deployable."

```
Pipeline says "good to go" → Should be ZERO more work to release
                          → No integration tests with other pipelines
                          → No staging environment validation
                          → No sign-offs
```

**Implication**: This forces an architectural decision:

**Either**:
- One giant pipeline for entire system (monolith)
- Everything tested together, deployed together

**Or**:
- Multiple small pipelines (microservices)
- Each tested independently, deployed independently

**Quote**: "If we don't trust the output of our deployment pipeline sufficiently and feel it necessary to test the results it generates with the output of other deployment pipelines, then that presents problems; the messages that our deployment pipeline is sending to us are now unclear."

## Boundaries as Seams

**From the book**: "Identifying 'seams' in the design of our systems where the rest of the system doesn't need to know and shouldn't care about, the detail of what is happening on the other side of those 'seams' is a very good idea. This is really the essence of design."

### The Common Problem

```python
# ❌ BOUNDARY LOOKS LIKE INTERIOR
# No distinction between module communication and internal communication

class OrderService:
    def create_order(self, data: dict):
        # Direct access to other service's internals
        customer = CustomerService().get_customer(data['customer_id'])
        
        # Passing internal data structures across boundary
        return customer.internal_state  # Leaking!


class CustomerService:
    def get_customer(self, id: str):
        # Returns ORM object - internal detail escapes!
        return session.query(Customer).filter_by(id=id).first()
```

### The Solution: Guarded Boundaries

```python
# ✅ BOUNDARY IS TRANSLATION & VALIDATION POINT

# Define explicit contract (the seam)
class CustomerPort(Protocol):
    """
    Port defines what OrderService needs from Customer domain.
    Implementation details hidden.
    """
    def get_customer_info(self, customer_id: str) -> CustomerInfo:
        """Returns immutable DTO, not internal model"""
        ...


# DTO for crossing boundary (translation)
@dataclass(frozen=True)
class CustomerInfo:
    """Public interface - safe to cross module boundary"""
    id: str
    name: str
    credit_limit: Decimal
    # Only what's needed, nothing internal


# Implementation hidden behind port
class CustomerAdapter(CustomerPort):
    def get_customer_info(self, customer_id: str) -> CustomerInfo:
        # Validation at boundary
        if not customer_id:
            raise ValueError("Customer ID required")
        
        # Internal details (ORM, DB)
        db_customer = session.query(Customer).filter_by(id=customer_id).first()
        
        if not db_customer:
            raise CustomerNotFoundError(customer_id)
        
        # Translation at boundary
        return CustomerInfo(
            id=db_customer.id,
            name=db_customer.full_name,
            credit_limit=Decimal(db_customer.credit_cents) / 100
        )


# Service uses port, knows nothing about implementation
class OrderService:
    def __init__(self, customer_port: CustomerPort):
        self.customers = customer_port
    
    def create_order(self, data: OrderData):
        # Clean boundary - receives DTO, not internal model
        customer = self.customers.get_customer_info(data.customer_id)
        # customer is CustomerInfo (immutable DTO)
        # No coupling to Customer internal implementation
```

## The REST API Accident

**From the book**: "There has been an advance in this respect, but it is a small step, and to some degree, we took that step by accident. That is the move to REST APIs."

### Why REST Helps (By Accident)

REST/HTTP forces translation at boundaries:
- Can't pass Python objects over HTTP
- Must serialize to JSON (translation)
- Must deserialize from JSON (translation)

**This is good!** Forces boundary thinking.

### Where REST Fails

```python
# ❌ STILL PASSING INTERNAL DETAILS THROUGH
@app.get("/orders/{id}")
def get_order(id: str):
    order = session.query(Order).get(id)
    return order  # SQLAlchemy object serialized!
    # Now API is coupled to database model
    # Now client knows about internal fields
    # Can't change DB without breaking API


# ✅ BOUNDARY WITH TRANSLATION
@app.get("/orders/{id}")
def get_order(id: str, service: OrderService = Depends()):
    # Service returns domain model (internal)
    order = service.get_order(id)
    
    # Translate to API model at boundary
    return OrderResponse(
        id=order.id,
        total=str(order.total),
        status=order.status.value,
        # Only expose what API contract promises
    )
```

**Quote from book**: "Software developers still get this wrong, though. Even in systems built along these lines, I still see code that passes the HTML straight through, and the whole service interacts with that HTML—yuck!"

## Modularity at Different Scales

**From the book**: "Modularity is important at every scale."

### Function Level

```python
# ❌ NOT MODULAR - Doing too much
def process_order(data):
    # Parse, validate, calculate, persist, notify - all mixed
    pass

# ✅ MODULAR - Single responsibility
def validate_order_data(data: dict) -> OrderData: ...
def create_order(data: OrderData) -> Order: ...
def persist_order(order: Order) -> Order: ...
def notify_order_created(order: Order) -> None: ...
```

### Class Level

```python
# Use dependency injection to expose surface area
class OrderService:
    def __init__(
        self,
        repository: OrderRepository,  # Seam
        payment: PaymentGateway,      # Seam
        events: EventBus              # Seam
    ):
        # Dependencies are calipers - points of measurement
        # Each dependency is a module boundary
        pass
```

**Quote**: "At smaller scales, dependency injection is the most effective tool to provide pressure on our code that encourages us to create systems composed of many small pieces. The dependencies are the calipers, the points of measurement, that we can inject into our system to achieve a more thoroughly testable outcome."

### Service Level

```python
# Clear module boundaries with ports
# OrderService module doesn't know about Customer implementation
# CustomerService module doesn't know about Order implementation
# Communicate only through public contracts (ports)
```

### System Level

```
Microservices are modules at system scale:
- Each has clear boundary (API contract)
- Each hides implementation (can be any tech stack)
- Each is independently deployable (true module)
```

## Small Teams Are More Productive

**Data from the book**: Study of 4,000+ software projects:

- Teams of 5: Delivered in 9 months
- Teams of 20: Delivered in 9 months + 1 week

**Analysis**: "Small teams are nearly 4 times as productive, per person, as larger teams."

**Also**: "Larger teams produced 5x more defects."

### Amazon's Two-Pizza Teams

**Quote**: "Amazon famously reorganized following a memo from CEO Jeff Bezos. In his memo Bezos stated that '…no team should be bigger than can be fed by two pizzas.'"

**Result**: "This approach...has allowed Amazon...to grow at an unprecedented rate."

### The Integration Problem

**Quote**: "The cost of integration is the killer! How do we integrate the work from separate streams of development?"

**Fred Brooks**: "You can't make a baby in a month with 9 women."

**But**: "You can make nine babies in nine months with nine women, which averages out at a baby per month."

**Application**: "The best way to parallelize things is to do it in a way where there is no need to re-integrate (nine babies). Essentially, this is the microservice approach."

**Critical**: "Microservices are an organizational scalability play; they don't really have any other advantage, but let's be clear, this is a big advantage if scalability is your problem!"

## Decision Framework

### When to Modularize

- [ ] **Can this be understood independently?** (If no, not cohesive enough for module)
- [ ] **Can this be tested independently?** (If no, coupling too tight)
- [ ] **Can this be deployed independently?** (If yes, consider microservice)
- [ ] **Will different teams maintain this?** (If yes, MUST be separate modules)

### Module Boundary Checklist

At every module boundary:

- [ ] **Public contract defined** (interface/protocol)
- [ ] **Translation layer exists** (DTOs cross boundary, not internal models)
- [ ] **Validation at boundary** (don't trust inputs)
- [ ] **Error handling at boundary** (translate exceptions)
- [ ] **Versioning strategy** (for APIs/services)
- [ ] **Tests for contract** (not implementation)

## Anti-Patterns

❌ **"Microservices for <10 people team"**
- Organizational overhead not worth it
- **Fix**: Start with modular monolith

❌ **"Testing services together"**
- Not really independent
- **Fix**: Contract tests, not integration tests

❌ **"Shared database between services"**
- Coupling through data model
- **Fix**: Each service owns its data, communicate via APIs

❌ **"Using internal models across boundaries"**
- Leaky abstraction
- **Fix**: DTOs/Value Objects for boundary crossing

❌ **"No translation at REST API"**
- Database model = API model
- **Fix**: Explicit response models

## Refactoring Toward Modularity

### Step 1: Identify Seams

Look for natural boundaries in your domain:
- Bounded contexts (DDD)
- Different rates of change
- Different teams/ownership
- Different deployment cycles

### Step 2: Define Ports

Create interfaces for communication across seams:
```python
# Port (interface)
class ProductCatalog(Protocol):
    def find_product(self, sku: str) -> ProductInfo: ...
```

### Step 3: Create Adapters

Implement ports with actual infrastructure:
```python
# Adapter
class PostgresProductCatalog(ProductCatalog):
    def find_product(self, sku: str) -> ProductInfo: ...
```

### Step 4: Inject Dependencies

Use dependency injection to wire adapters to ports:
```python
# Service knows only about port
class OrderService:
    def __init__(self, products: ProductCatalog):
        self.products = products
```

### Step 5: Add Translation

DTOs cross boundaries, not domain models:
```python
@dataclass(frozen=True)
class ProductInfo:  # DTO for boundary crossing
    sku: str
    price: Decimal
```

## Testing Modular Systems

### Unit Tests (Within Module)

```python
def test_order_calculation():
    # Test module internals in isolation
    # Use fakes for dependencies (other modules)
    fake_products = FakeProductCatalog()
    service = OrderService(products=fake_products)
    # ...
```

### Contract Tests (At Boundary)

```python
def test_product_catalog_contract():
    """Test that adapter fulfills port contract"""
    catalog: ProductCatalog = PostgresProductCatalog()
    product = catalog.find_product("SKU-123")
    assert isinstance(product, ProductInfo)
    # Contract fulfilled!
```

### Integration Tests (Optional)

Only if microservices architecture:
```python
# Test actual HTTP calls between services (sparingly!)
# Most validation in contract tests instead
```

## Integration with Other Skills

- **Requires**: `separation-of-concerns-enforcer` (modules separate concerns)
- **Pairs with**: `cohesion-coach` (cohesive modules)
- **Enables**: `coupling-minimizer` (module boundaries reduce coupling)
- **Supports**: `deployment-pipeline-designer` (deployment = module scope)

## Success Metrics

- **Module independence**: Can test module without touching others
- **Team autonomy**: Can deploy module without coordinating with other teams
- **Change localization**: >80% of changes affect single module
- **Build time**: <10 min for single module, parallel builds for multiple

## Related References

See [reference/principles.md](reference/principles.md) for book quotes on modularity.
See [reference/examples.md](reference/examples.md) for Apollo program and other examples.
