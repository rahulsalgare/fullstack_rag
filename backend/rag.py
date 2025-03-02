from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_community.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from operator import itemgetter

from qdrant import vector_store
from dotenv import load_dotenv

load_dotenv()

# model = ChatOpenAI(
#     model_name="gpt-4o",
#     temperature=0.5,
# )
model = ChatOllama(model="llama3.2", format="json", temperature=0)

prompt_template = """
Answer the question based on the context, in a concise manner, in markdown and using bullet points where applicable.

Context: {context}
Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(prompt_template)

retriever = vector_store.as_retriever()

def create_chain():
    chain = (
        {
            "context": retriever.with_config(top_k=4),
            "question": RunnablePassthrough(),
        }
        | RunnableParallel({
            "response": prompt | model,
            "context": itemgetter("context"),
            })
    )
    return chain

def get_answer_and_docs(question: str):
    chain = create_chain()
    response = chain.invoke(question)
    answer = response["response"].content
    context = response["context"]
    return {
        "answer": answer,
        "context": context
    }

if __name__ == '__main__':
    question = "What did Yohji Yamamoto say ?"
    ans = get_answer_and_docs(question)
    print(ans)