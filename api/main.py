import logging
import sys

from fastapi import FastAPI

# from src.db import Database
# from src.llm import LLM
from .config import settings
from .routers import v1


#######################
# Configure root logger
logging_level = logging.DEBUG if settings.debug else logging.INFO

logging.basicConfig(level=logging_level)

formatter = logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging_level)
stdout_handler.setFormatter(formatter)
logging.getLogger().addHandler(stdout_handler)

logger = logging.getLogger()

#########################
# Create base directories
settings.app_path.mkdir(parents=True, exist_ok=True)
logger.info("Application path: %s", settings.app_path)

settings.data_path.mkdir(parents=True, exist_ok=True)
logger.info("Data path: %s", settings.data_path)

settings.llm_path.mkdir(parents=True, exist_ok=True)
logger.info("Model path: %s", settings.llm_path)

####################
# Create FastAPI app
app = FastAPI()
app.include_router(v1.router)




# def main():
#     """ Main function
#     """
    # database = Database(config=config)
    # # llm = LLM(config=config, database=database, verbose=False)

    # database.load_pdf_document(file_path="/Users/juliannonino/Julian/InquireDocs/InquireDocs/api/Deep Learning.pdf")

    # question = "What is Deep Learning"

    # print()
    # print()
    # print()
    # print("#########################")
    # print("### similarity_search ###")
    # print("#########################")
    # documents_a = database.similarity_search(question)
    # print(documents_a)

    # print()
    # print()
    # print()
    # print("###############################################")
    # print("### similarity_search_with_relevance_scores ###")
    # print("###############################################")
    # documents_b = database.similarity_search_with_relevance_scores(question)
    # print(documents_b)

    # print()
    # print()
    # print()
    # print("################")
    # print("### retrieve ###")
    # print("################")
    # documents_c = database.retrieve(question)
    # print(documents_c)

    # # app = FastAPI()

    # # while True:
    # #     print("###################")
    # #     print("### InquireDocs ###")
    # #     print("###################")
    # #     question = input("Please enter your question: ")
    # #     answer = llm.elaborate_answer(question=question)
    # #     print(answer["output_text"])
    # #     print()
    # #     print()
    # #     print()


    # # @app.get("/")
    # # async def read_main():
    # #     return {"msg": "Hello World"}

# if __name__ == "__main__":
#     main()
