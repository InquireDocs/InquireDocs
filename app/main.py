from fastapi import FastAPI

from app.api.v1.routes import router as v1_router
from app.core.config import settings
from app.core.logging_config import logger
from app.db import database

#########################
# Create base directories
settings.APP_PATH.mkdir(parents=True, exist_ok=True)
logger.info("Application path: %s", settings.APP_PATH)

settings.DATA_PATH.mkdir(parents=True, exist_ok=True)
logger.info("Data path: %s", settings.DATA_PATH)

settings.LLM_PATH.mkdir(parents=True, exist_ok=True)
logger.info("Model path: %s", settings.LLM_PATH)

####################
# Create FastAPI app
app = FastAPI(title=settings.PROJECT_NAME)

logger.info("Starting API version 1")
app.include_router(v1_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    # Check DB is online
    logger.info("Checking database status")
    # vector_store.


@app.get("/health", tags=["Health Check"])
def health_check():
    """Health check endpoint"""
    return {"status": "OK"}












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













###############################################################################
# Test
###############################################################################
# from app.models import pdf


# pdfs_to_load = [
#   # "https://docs.aws.amazon.com/pdfs/wellarchitected/latest/devops-guidance/devops-guidance.pdf",
#   "https://docs.aws.amazon.com/pdfs/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.pdf"
#   # "https://docs.aws.amazon.com/pdfs/wellarchitected/latest/management-and-governance-guide/management-and-governance-cloud-environment-guide.pdf"
# ]

# database.print_record_manager_list()

# for pdf_url in pdfs_to_load:
#     pdf.add_pdf(pdf_url)
#     database.print_record_manager_list()


# query = "What is a disaster?"

# logger.info("BEFORE DELETE # Similarity Search with Euclidean Distance (Default)")
# docs_with_score = database.search_with_score(query=query, method="similarity", items_to_return=3)
# for doc, score in docs_with_score:
#     logger.info("Score: %s", score)
#     # logger.info(doc)

# # logger.info("# Maximal Marginal Relevance Search (MMR)")
# # docs_with_score = database.search_with_score(query=query, method="max_marginal_relevance", items_to_return=3)
# # for doc, score in docs_with_score:
# #     logger.info("Score: %s", score)
#     # logger.info(doc.page_content)

# pdf_to_delete = "https://docs.aws.amazon.com/pdfs/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.pdf"
# pdf.delete_pdf(pdf_to_delete)
# database.print_record_manager_list()

# logger.info("AFTER DELETE # Similarity Search with Euclidean Distance (Default)")
# database.print_record_manager_list()
# docs_with_score = database.search_with_score(query=query, method="similarity", items_to_return=3)
# for doc, score in docs_with_score:
#     logger.info("Score: %s", score)
# #     logger.info(doc)
