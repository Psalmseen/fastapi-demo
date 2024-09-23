## FastAPI Production Template

A scalable and production ready boilerplate for FastAPI

### Table of Contents

- [Project Overview](#project-overview)
- [Installation Guide](#installation-guide)
- [Usage Guide](#usage-guide)
- [Advanced Usage](#advanced-usage)

### Project Overview

This boilerplate follows a layered architecture that includes a model layer, a repository layer, a controller layer, and an API layer. Its directory structure is designed to isolate boilerplate code within the core directory, which requires minimal attention, thereby facilitating quick and easy feature development. The directory structure is also generally very predictable. The project's primary objective is to offer a production-ready boilerplate with a better developer experience and readily available features. 


### Installation Guide

You need following to run this project:

- Python 3.11
- Uvicorn [standard]
- fastapi [standard] 
- Terminal access


1. Run the server:

```bash
uvicorn main:app --reload
```

The server should now be running on `http://localhost:8000`

### Directory Structure

The project is designed to be modular and scalable. There are 3 main directories in the project:

1. `core`: This directory contains the central part of this project. It contains most of the boiler plate code like security dependencies, database connections, configuration, middlewares etc. It also contains the base classes for the models, repositories, and controllers. The `core` directory is designed to be as minimal as possible and usually requires minimal attention. Overall, the `core` directory is designed to be as generic as possible and can be used in any project. While building additional feature you may not need to modify this directory at all except for adding more controllers to the `Factory` class in `core/factory.py`.

2. `app`: This directory contains the actual application code. It contains the models, repositories, controllers, and schemas for the application. This is the directory you will be spending most of your time in while building features. The directory has following sub-directories:

   - `models` Here is where you add new tables
   - `repositories` For each model, you need to create a repository. This is where you add the CRUD operations for the model.
   - `controllers` For each logical unit of the application, you need to create a controller. This is where you add the business logic for the application.
   - `schemas` This is where you add the schemas for the application. The schemas are used for validation and serialization/deserialization of the data.

3. `api`: This directory contains the API layer of the application. It contains the API router, it is where you add the API endpoints.


If you need to downgrade the database or reset it. You can use `make rollback` and `make reset-database` respectively.


#### Row Level Access Control

The boilerplate contains a custom row level permissions management module. It is inspired by [fastapi-permissions](https://github.com/holgi/fastapi-permissions). It is located in `core/security/access_control.py`. You can use this to enforce different permissions for different models. The module operates based on `Principals` and `permissions`. Every user has their own set of principals which need to be set using a function. Check `core/fastapi/dependencies/permissions.py` for an example. The principals are then used to check the permissions for the user. The permissions need to be defined at the model level. Check `app/models/user.py` for an example. Then you can use the dependency directly in the route to raise a `HTTPException` if the user does not have the required permissions. Below is an incomplete example:

```python
from fastapi import APIRouter, Depends
from core.security.access_control import AccessControl, UserPrincipal, RolePrincipal, Allow
from core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

    def __acl__(self):
        return [
            (Allow, UserPrincipal(self.id), "view"),
            (Allow, RolePrincipal("admin"), "delete"),
        ]

def get_user_principals(user: User = Depends(get_current_user)):
    return [UserPrincipal(user.id)]

Permission = AccessControl(get_user_principals)

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: int, user: User = get_user(user_id), assert_access = Permission("view")):
    assert_access(user)
    return user

```

#### Caching

You can directly use the `Cache.cached` decorator from `core.cache`. Example

```python
from core.cache import Cache

@Cache.cached(prefix="user", ttl=60)
def get_user(user_id: int):
    ...
```

#### Session Management

The sessions are already handled by the middleware and `get_session` dependency which injected into the repositories through fastapi dependency injection inside the `Factory` class in `core/factory.py`. There is also `Transactional` decorator which can be used to wrap the functions which need to be executed in a transaction. Example:

```python
@Transactional()
async def some_mutating_function():
    ...
```

Note: The decorator already handles the commit and rollback of the transaction. You do not need to do it manually.

If for any case you need an isolated sessions you can use `standalone_session` decorator from `core.database`. Example:

```python
@standalone_session
async def do_something():
    ...
```

#### Repository Pattern

The boilerplate uses the repository pattern. Every model has a repository and all of them inherit `base` repository from `core/repository`. The repositories are located in `app/repositories`. The repositories are injected into the controllers inside the `Factory` class in `core/factory/factory.py.py`.

The base repository has the basic crud operations. All customer operations can be added to the specific repository. Example:

```python
from core.repository import BaseRepository
from app.models.user import User
from sqlalchemy.sql.expression import select

class UserRepository(BaseRepository[User]):
    async def get_by_email(self, email: str):
        return await select(User).filter(User.email == email).gino.first()

```

To facilitate easier access to queries with complex joins, the `BaseRepository` class has a `_query` function (along with other handy functions like `_all()` and `_one_or_none()`) which can be used to write compplex queries very easily. Example:

```python
async def get_user_by_email_join_tasks(email: str):
    query = await self._query(join_)
    query = query.filter(User.email == email)
    return await self._one_or_none(query)
```

Note: For every join you want to make you need to create a function in the same repository with pattern `_join_{name}`. Example: `_join_tasks` for `tasks`. Example:

```python
async def _join_tasks(self, query: Select) -> Select:
    return query.options(joinedload(User.tasks))
```

#### Controllers

Kind of to repositories, every logical unit of the application has a controller. The controller also has a primary repository which is injected into it. The controllers are located in `app/controllers`.

These controllers contain all the business logic of the application. Check `app/controllers/auth.py` for an example.

#### Schemas

The schemas are located in `app/schemas`. The schemas are used to validate the request body and response body. The schemas are also used to generate the OpenAPI documentation. The schemas are inherited from `BaseModel` from `pydantic`. The schemas are primarily isolated into `requests` and `responses` which are pretty self explainatory.
