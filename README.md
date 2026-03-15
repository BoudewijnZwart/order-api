# Order API

# Running the API

The app can be started with:

```bash
uv run python -m order_api.main
```
. UV is required to install the dependencies and run the app. Alteratively, the
app can be run using Podman/Docker. UV is then not necessary.

**Docker**
```bash
docker build -t fastapi-app . && docker run -p 8000:8000 fastapi-app
```

**Podman**
```bash
podman build -t fastapi-app . && podman run -p 8000:8000 fastapi-app
```

After starting the app, the swagger docs can then be viewed by visiting: `http://localhost:8000/docs` in a browser.

## Demo data

Claude created some demo data in the file `demo_data.json`. After starting the api this can be
inserted into the "database" by running:

```bash
curl -X POST http://localhost:8000/orders/batch   -H "Content-Type: application/json"   -d @demo_data.json
```
. This demo data contains six wrong orders that will be rejected:

| Order | Invalid reason |
|---|---|
| ORD-0031 | `quantity: -5` — violates `gt=0` |
| ORD-0032 | `unit_price: -9.99` — violates `ge=0` |
| ORD-0033 | `items: []` — violates `min_length=1` |
| ORD-0034 | `order_timestamp` is not a valid datetime |
| ORD-0035 | `unit_price` field missing from item |
| ORD-0040 | `quantity: 0` — violates `gt=0` (strictly greater than) |

## Tests

To support the code, some integration tests have been written. These can be executed by running:

```bash
uv run pytest
```

## Design considerations

### GET endpoint

I created a schema for the return type of the get orders endpoint that includes the total number of returned orders. This could be nice for a possible frontend later.

#### Filtering

Delegate the filtering to a filter class. Makes is easier to change later. The filters are called by the
service not the repository. I think this is fine for an in-memory store of data.

For filtering I am using simple list comprehensions. This does not scale well but if the API scales
the filtering should really be performed by the database.

#### Sorting

I added sorting because there is pagination. This makes it more reproducible.

### Summary endpoint

Normally, I would implement a service for the summary that also gets the repository as a dependency. I now added this functionality to the order service.
