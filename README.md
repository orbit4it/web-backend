# Orbit Web Backend

GraphQL backend for Orbit website.

## Getting started

1. Clone this repository
2. Create `.env` file ([see example](https://github.com/orbit4it/web-backend/blob/dev/.env.example))
3. Install dependencies

```
pip install -r requirements.txt
```

4. Run

```
python src/main.py
```

5. Open `localhost:8000/graphql`

## Adding new features

To add new features, create new module in the `src/core` folder. The standard simple file structure of a feature would look something like this.

```
.
├── __init__.py
├── model.py
├── mutation.py
├── query.py
└── type.py
```

Look at existing features in `src/core` as examples to start writing code.

After you finish writing the code. Follow these steps to register the feature to the app.

### Register Model

Register a model to create a table in the database. You just simply need to import the model.

`src/db/tables.py`

```python
import core.user.model
import core.grade.model
import core.division.model
# Import models here

from .database import Base, engine


Base.metadata.create_all(engine)
...
```

### Register Query & Mutation

To register queries & mutations to the graphql schema, edit the following files:

`src/schema/query.py`

```python
import strawberry

from core.user import Query as UserQuery
# Import query here

@strawberry.type
class Query(
    UserQuery,
    # Register query here
):
    ...
```

Same as Query, to register Mutation edit `src/schema/mutation.py`.

### Validation

See the following example:

`src/helpers/validation.py`

```python
def validate_something(input: string):
    try:
        valid_email(input)
        not_empty("Input", input)
        min_len("Input", input, 10)
        max_len("Input", input, 12)
    except ValidationError as e:
        raise e
```

The usage would look something like this in Query/Mutation:

```python
try:
    validate_something(input)
except ValidationError as e:
    return Error(str(e))
```

## Managing database

The database schema will be created automatically when the server starts up. If there is a schema change, to see the changes the table must be dropped first. To drop tables and seeders use `script.py`

Drop all tables:

```
python script.py drop-all
```

Seeder (insert dummy data):

```
python script.py seed
```

## Testing

Please create unit tests for each feature you add. Test for successful, failed, and invalid cases. (for now, let just test the GraphQL). To run unit tests use this command:

```
pytest
```

