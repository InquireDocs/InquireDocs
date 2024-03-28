# InquireDocs

TODO: Describe the application

## Start the application

### How to run locally

The application requires some environment variables. To run locally those can be set in a .env file in the root of the repository.
Those are:
- *PROJECT_NAME*: The name of the application. Default value is `PaaS Chat Backend`.
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
