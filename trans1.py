from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

with open('text.txt', 'r') as f:
    default_tran = f.read()
# default_tran = "No captions available for this video."

prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
    input_variables = ['context', 'question']
)

llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-flash",
    # api_key="AIzaSyA-x959UXNkvlcjTbVPfiwWSjzngSwT7Zo"
    api_key="AIzaSyBTBK2r8Bdaeg_BwvqzolrLc2tXVHptD5s"
    )

def embed():
    # Embedding model
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings

i = 1 
if i == 1:
    embeddings =  embed()
    i = i+1
else:
    print("embeddings already created")

def get_video_embed(video_id):
    video_id = video_id # only the ID, not full URL
    try:
        print(f"Fetching transcript for video ID: {video_id}")
    # If you don’t care which language, this returns the “best” one
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en","hi"])
    # Flatten it to plain text
        transcript = " ".join(chunk["text"] for chunk in transcript_list)
    
    except Exception as e:
        transcript = default_tran
        print("No captions available for this video.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])
    vector_store = FAISS.from_documents(chunks, embeddings)
    print("Vector store created successfully.")
    return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# call main llm function 
def llm_call(question,retriever):
    # retrieved_docs    = retriever.get_relevant_documents(question)
    retrieved_docs    = retriever.invoke(question)
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    final_prompt = prompt.invoke({"context": context_text, "question": question})
    answer = llm.invoke(final_prompt)
    return answer.content

# question   = "is the topic of nuclear fusion discussed in this video? if yes then what was discussed"
# question = input("Enter your question: ")
# id = input("Enter the video ID: ")  # e.g., "Gfr50f6ZBvo"
# question = "Sumarize it"
# id = "ZEF2PzDvdt8"
# # llm_call(question,retriever=get_video_embed("Gfr50f6ZBvo")) # only the ID, not full URL
# llm_call(question,retriever=get_video_embed(id)) # only the ID, not full URL
