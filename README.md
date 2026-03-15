# Order API

## Design considerations

### GET endpoint

Create a schema including the total number of returned orders for a possible frontend later.

#### Filtering

Delegate the filtering to a filter class. Makes is easier to change later. The filters all called by the
service not the repository. I think this is fine for an in-memory store of data.

For filtering I am using simple list comprehensions. This does not scale well but if the API scales
the filtering should really be performed by the database.

#### Sorting

I added sorting because there is pagination. This makes it more reproducible.
