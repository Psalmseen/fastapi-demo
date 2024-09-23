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
