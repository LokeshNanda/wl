## June 2025

### 25 Jun 2025
- Came across a graph database - [DGraph](https://docs.hypermode.com/dgraph/overview)
  - Found it to be very interesting open source project
    - Explored its competitor - Neo4j atlas:
      - Created an account in neo4j atlas online. Self hosting was also an option, but went ahead with this.
      - created an itegration to extract wiki pages using langgraph and extract entities.
          ```python
              from dotenv import load_dotenv  
              import os  
              from langchain_neo4j import Neo4jGraph  
              
              from langchain_core.runnables import (  
                  RunnableBranch,  
                  RunnableLambda,  
                  RunnableParallel,  
                  RunnablePassthrough,  
              )  
              from langchain_core.prompts import ChatPromptTemplate  
              from langchain_core.prompts.prompt import PromptTemplate  
              from pydantic import BaseModel, Field  
              # from langchain_core.pydantic_v1 import BaseModel, Field  
              from typing import Tuple, List  
              from langchain_core.messages import AIMessage, HumanMessage  
              from langchain_core.output_parsers import StrOutputParser  
              from langchain_community.document_loaders import WikipediaLoader  
              from langchain.text_splitter import TokenTextSplitter  
              from langchain_openai import ChatOpenAI  
              from langchain_experimental.graph_transformers import LLMGraphTransformer  
              
              from langchain_neo4j import Neo4jVector  
              from langchain_openai import OpenAIEmbeddings  
              from langchain_neo4j.vectorstores.neo4j_vector import remove_lucene_chars  
              
              load_dotenv()  
              
              AURA_INSTANCENAME = os.environ["AURA_INSTANCENAME"]  
              NEO4J_URI = os.environ["NEO4J_URI"]  
              NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]  
              NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]  
              AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)  
              
              OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  
              OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")  
              
              chat = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model="gpt-4o-mini")  
              
              
              kg = Neo4jGraph(  
                url=NEO4J_URI,  
                username=NEO4J_USERNAME,  
                password=NEO4J_PASSWORD,  
              ) #database=NEO4J_DATABASE,  
              
              # # # read the wikipedia page for the Roman Empire  
              raw_documents = WikipediaLoader(query="The Indian Politics").load()  
              
              # # # # # Define chunking strategy  
              text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)  
              documents = text_splitter.split_documents(raw_documents[:3])  
              print(documents)  
              
              llm_transformer = LLMGraphTransformer(llm=chat)  
              graph_documents = llm_transformer.convert_to_graph_documents(documents)  
              
              # store to neo4j  
              res = kg.add_graph_documents(  
                graph_documents,  
                include_source=True,  
                baseEntityLabel=True,  
              )
          ```
      - Doing similar in DGraph would require creating a wrapper as it doesn't have out of box integration with Dgraph.

### 26 Jun 2025
- 