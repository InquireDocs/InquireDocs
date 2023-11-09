from langchain.vectorstores import Chroma
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain

import config


prompt_template = """
You are a helpful assistant that accurately answers queries using the following pieces of context: "{context}"
Do not mention that a context has been provided. Answer the questions as if they were coming straight from you.
Use the context provided to form your answer, but avoid copying word-for-word from the text. Try to use your own words when possible. Keep your answer under 5 sentences.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Be accurate, helpful, concise, and clear.
Always use the given context to provide an answer to the question: "{question}".
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# https://huggingface.co/TheBloke/vicuna-7B-v1.5-GGUF/resolve/main/vicuna-7b-v1.5.Q4_K_M.gguf
llm = LlamaCpp(
  model_path="./models/vicuna-7b-v1.5.Q4_K_M.gguf",
  temperature=0.75,
  max_tokens=2000,
  top_p=1,
  callback_manager=callback_manager,
  verbose=True  # Verbose is required to pass to the callback manager
)
llm_chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt, verbose=False)

chroma_db = Chroma(
  persist_directory=config.CHROMA_PERSIST_DIRECTORY,
  embedding_function=config.CHROMA_EMBEDDING_FUNCTION
)


def query_vectordb(query):
    """Query VectorDB
    @param query: Question to ask
    """
    docs = chroma_db.similarity_search(query)
    return docs


def elaborate_answer(docs):
    """Elaborate answer based on returned docs by VectorDB.
    @params docs: Docs retrieved from VectorDB.
    """
    answer = llm_chain({"input_documents": docs, "question": query}, return_only_outputs=True)
    return answer


print("==========")
print("==========")
print("==========")
query = "What are the approaches to Task Decomposition?"
docs = query_vectordb(query)
answer = elaborate_answer(docs)
print(answer)

print("==========")
print("==========")
print("==========")
query = "What are autonomous agents?"
docs = query_vectordb(query)
answer = elaborate_answer(docs)
print(answer)
