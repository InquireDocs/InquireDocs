from langchain.prompts import PromptTemplate
from langchain.llms import GPT4All
from langchain.chains.question_answering import load_qa_chain

from db import Database


PROMPT_TEMPLATE = """
You are a helpful assistant that accurately answers queries using the following pieces of context: "{context}"
Do not mention that a context has been provided. Answer the questions as if they were coming straight from you.
Use the context provided to form your answer, but avoid copying word-for-word from the text. Try to use your own words when possible. Keep your answer under 5 sentences.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Be accurate, helpful, concise, and clear.
Always use the given context to provide an answer to the question: "{question}".
"""


class Model():
    def __init__(self):
        self.vector_db = Database().langchain_chroma

        self.prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])

        self.chain_mistral_openorca = load_qa_chain(
            GPT4All(model="./models/mistral-7b-openorca.Q4_0.gguf"),
            chain_type="stuff",
            prompt=self.prompt,
            verbose=False
        )


    def elaborate_answer(self, question):
        documents = self.vector_db.similarity_search(question)

        return self.chain_mistral_openorca(
          {
              "input_documents": documents,
              "question": question
          },
          return_only_outputs=True
        )
