from fastapi import FastAPI
from settings import config


print("Application path: %s", config.get_app_path())
print("Data path: %s", config.get_data_path())
print("Model path: %s", config.get_model_path())

# app = FastAPI()


# @app.get("/")
# async def read_main():
#     return {"msg": "Hello World"}
