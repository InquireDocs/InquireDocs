# InquireDocs

TODO: Describe the application

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Contents

- [Development](#development)
  - [Directory structure](#directory-structure)
  - [How to run locally](#how-to-run-locally)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Development

### Directory structure

1. `app/api/`: This is where version-specific API implementations go. Each version (e.g., v1, v2) has its own directory with endpoints files. This structure isolates versioned logic, allowing independent updates to each API version.
2. `app/core/`: Contains configuration and utility code, such as app settings, which are shared across different parts of the app.
3. `app/models/`: Defines database models and shared schemas used across different versions.
4. `app/services/`: Contains the business logic, which is organized by feature or service and is agnostic to API versions. This is where the core application logic lives, making it reusable across multiple API versions.
5. `app/db/`: Responsible for database connection setup and management, such as connection pooling and session creation.
6. `app/main.py`: This is the entry point where the FastAPI app instance is created and configured, including mounting versioned routes.
7. `tests/`: Contains test files organized by API version. Separate directories for each version make it easy to manage version-specific test cases.

### How to run locally

The application requires some environment variables. To run locally those can be set in a .env file in the root of the repository.
Those are:
- *PROJECT_NAME*: The name of the application. Default value is `InquireDocs`.
- *DEBUG*: Boolean value to indicate if should include debug logs. Defaults to `false`.

Run the application:
```bash
virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install --requirement requirements.txt
uvicorn app.main:app --reload
```

To enable debug mode set the variable `DEBUG` to true.
```bash
DEBUG=TRUE uvicorn app.main:app --reload
```
