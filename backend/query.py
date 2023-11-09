from langchain.prompts import PromptTemplate
from langchain.llms import GPT4All
from langchain.chains.question_answering import load_qa_chain


from model import Model

llm_model = Model()


while True:
    question = input("Please enter your question: ")
    answer = llm_model.elaborate_answer(question=question)
    print(answer["output_text"])
    print()
    print()
    print()
