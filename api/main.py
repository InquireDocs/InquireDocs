from fastapi import FastAPI

from src.db import Database
from src.llm import LLM
from src.settings import Settings


def main():
    """ Main function
    """
    config = Settings()
    print(f"Application path: {config.get_app_path()}")
    print(f"Data path: {config.get_data_path()}")
    print(f"Model path: {config.get_model_path()}")

    database = Database(config=config)
    # llm = LLM(config=config, database=database, verbose=False)

    database.load_pdf_document(file_path="/Users/juliannonino/Julian/InquireDocs/InquireDocs/api/Deep Learning.pdf")

    question = "What is Deep Learning"

    print()
    print()
    print()
    print("#########################")
    print("### similarity_search ###")
    print("#########################")
    documents_a = database.similarity_search(question)
    print(documents_a)

    print()
    print()
    print()
    print("###############################################")
    print("### similarity_search_with_relevance_scores ###")
    print("###############################################")
    documents_b = database.similarity_search_with_relevance_scores(question)
    print(documents_b)

    print()
    print()
    print()
    print("################")
    print("### retrieve ###")
    print("################")
    documents_c = database.retrieve(question)
    print(documents_c)

    # app = FastAPI()

    # while True:
    #     print("###################")
    #     print("### InquireDocs ###")
    #     print("###################")
    #     question = input("Please enter your question: ")
    #     answer = llm.elaborate_answer(question=question)
    #     print(answer["output_text"])
    #     print()
    #     print()
    #     print()


    # @app.get("/")
    # async def read_main():
    #     return {"msg": "Hello World"}

if __name__ == "__main__":
    main()
