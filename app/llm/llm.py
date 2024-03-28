from langchain.prompts import PromptTemplate
from langchain.llms import GPT4All
from langchain.chains.question_answering import load_qa_chain

from db import Database
from settings import Settings


PROMPT_TEMPLATE = """
You are a helpful assistant that accurately answers queries using the following pieces of context: "{context}"
Do not mention that a context has been provided. Answer the questions as if they were coming straight from you.
Use the context provided to form your answer, but avoid copying word-for-word from the text. Try to use your own words when possible. Keep your answer under 5 sentences.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Be accurate, helpful, concise, and clear.
Always use the given context to provide an answer to the question: "{question}".
"""


class LLM():

    def __init__(self, config: Settings, database: Database, verbose=False):
        model_file_path = config.get_model_path() + "/mistral-7b-openorca.Q4_0.gguf"

        self.__vector_db = database
        self.__prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])
        self.__qa_chain = load_qa_chain(
            GPT4All(model=model_file_path),
            chain_type="stuff",
            prompt=self.__prompt,
            verbose=verbose
        )

    def elaborate_answer(self, question):
        """Answer a question.
        """
        documents = self.__vector_db.similarity_search(question)

        return self.__qa_chain(
          {
              "input_documents": documents,
              "question": question
          },
          return_only_outputs=True
        )
