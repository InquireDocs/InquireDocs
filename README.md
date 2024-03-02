# InquireDocs

## Start the application

### How to run locally

Start the local database:
```bash
docker-compose --file utils/docker-compose.yaml up
```

Run the application:
```bash
virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install --requirement requirements.txt
uvicorn api.main:app --reload
```

To enable debug mode set the variable `DEBUG` to true.
```bash
DEBUG=TRUE uvicorn api.main:app --reload
```
