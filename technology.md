## June 2025

### 20 Jun 2025
- I have been using GCP & Azure, but wanted to explore container services available in AWS. Here are few notes based on findings:
  - Amazon ECS
    - proprietary Container Service, this is not based on K8s.
    - Supports 2 types of launch modes:
      - EC2 - User manage ec2 instance - good if we already have reserved instances.
      - Fargate Launch type - Serverless.
  - Amazon EKS (Elastic K8 service) - Typical like GKE & AKS
  - App Runner - Very similar to Cloud run, but still lacks.
    - This is more higher level compared to ECS in terms of abstraction.
    - Can't really scale to 0 [Issue still open?](https://github.com/aws/apprunner-roadmap/issues/9)
      - On further read, I see it has been implemented. It can scale 0, when idle time of 5minutes. And it will resume on https traffic with cold start like Cloud Run.
    - For production process, I guess we should stick to Fargate.
  - AWS Lambda - Great and popular. If use case has <15mins runtime.

### 24 Jun 2025
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

### 25 Jun 2025
- Wanted to explore and do hands-on in dbt. Here are the findings:
  - Notes from Data Engineering project [DBT DE Project with Snowflake](https://www.youtube.com/watch?v=zZVQluYDwYY&t=5725s)
    - DBT doesn't extract or load data. It focuses on transformation step in ETL.
    - DBT works on top of Data Warehouse. Compute happens in the DW.
    - I still wonder, I can have .sql in my source code repo and control using that, why dbt then?
      - Benefits - Documentation out of box | Reusability | Testing Framework built-in | Dependency management | Modular
    - DBT Cloud vs DBT Core
      - DBT Core doesn't include built-in semantic layer. It can be done via MetricFlow but expose via api is only feature of cloud.
      - Cube.dev -> Is an alternative, if one want to stick to dbt core for semantic layer.
  - DBT markdown notes - [Link here](https://publish.obsidian.md/datavidhya/Course+Notes/Dbt(databuildtool)/1.+Introduction+to+DBT)
  - DBT Models
    - SQL Scripts are written here. Can reference other models.
    ```shell
    dbt run
    ```
    - [DBT Materialisation](https://docs.getdbt.com/docs/build/materializations) for each folder. Supports - table | view | incremental | ephemeral
      - For incremental, you need to write the logic
        - {% if is_incremental() %} 
      - For ephemeral, it's more like creating table in memory, it doesn't get created in warehouse, however, you can still reference it.
    - Look in dbt_project.yml -> Overwrite possible with config {{ }} in the model sql files
  - DBT Seed - Not really helpful for large data. It can be used for smaller dataset.
  - DBT Sources - Helpful for documentation
    - Create sources.yml under models/
  - DBT Snapshots
    - Built in implementation of type-2 scd.
    - There are dbt packages, which are like reusable functions.
    - Very useful, if one needs SCD in their data warehouse.
  - DBT Test
    - Generic Test - Define in the models/schema.yaml file
    - Singular Test - Custom sql -> tests/check_custom_business_logic.sql
    - Test Config - Severity - warn, error -> Things like this can be defined.
  - DBT Document
    - Powerful feature, out of box available in cloud
      ```bash
      dbt docs generate
      dbt docs serve
      ```
    - Lot of features and customisation. Loved it. Lineage is very good.
  - DBT Macros
    - It is more like function. Reuse!
  - Hooks 
    - Can be used for logging operation
    - Maybe access permissions you want to give during start of job & stop at end.
  - Operation Tasks
    - We can create custom operation by defining a macro Ex - Add partition at specific time
  - CICD should be setup in the repo.
  - Airflow can be used to trigger models based on schedule.
  - Model Organisation & naming convention would be very critical here. Inspiration can be taken from [here](https://publish.obsidian.md/datavidhya/Course+Notes/Dbt(databuildtool)/14.+Advance+DBT+Concept#Project+Organization)

### 26 Jun 2025
- Notes from AWS Sumit India 2025
  - Gen AI
    - Where amazon actually used in production genai internally? - chatbot | Audio, video & image generator tool | Inventory management
    - Amazon Q Developer
      - Very similar to Cursor, Copilot.
    - Amazon Q Business
      - Out of box chatbot, on top of your internal data.
      - It can integrate with sharepoint. We did this similar in Microsoft Copilot, but observed the cost to be really high for indexing of the documents.
        - Need to check on the cost side, how different it is.
    - Amazon developed AI Chips to help on cost reduction - AWS Trainium2 and Inferentia2.
    - AWS Bedrock Agents:
      - Simple multi agent flow use-case without coding can be done here. It points to a knowledge base.
      - For tools, it allows access to Lambda functions. 
    - AWS Sagemaker - Hyperpod - Fine tuning of LLM's. Hardware support.
      - Reserved Capacity - 6months - Observed 68% cost reduction.
      - Slurm(Simple Linux Utility for Resource Manager) - Open Source orchestrator & cluster management system for linux based.
      - Peplexity AI | Stabality AI use Hyperpod for their training.
    - Storage
      - Amazon FSx for Lustre
  - Data
    - Amazon is going the Azure way of Fabric, by introducing Amazon Sagemaker Unified Studio (All in one plarform). Rebrand & name change! Iceberg format native. 
    - But supports all 3 - Hudi, Delta & Iceberg.
    - Zero-ETL Integration - Federated Querying.
    - Valkey on Amazon - In-memeory Database
      - Amazon Elasticache (Serverless option also) - Microsecond write
      - Amazon Memory DB (In memory with durability) - milli-second write coz data commiteed to multi AZ transaction log. - (Instance based.)
        - Free tier available for small workload.
      - Valkey - Community replacement of Redis, since 7.2, it was not under open-source license.
    - Bedrock can be directly called in a SQL query for redshift. Directly create a sentiment score with just query. No need of Python etc. Good use-case.
    - Zero-etl supported for Salesforce via Glue ETL. No need of creating a ingestion framework for this. Auto incremental setups available. 
    - Amazon s3 Table buckets - namespaces - tables
      - Amazon S3 tables with Amazon Sagemaker Lakehouse.
      - Auto handling of compaction | snapshots | file-cleaning
      - Good support for Iceberg using Amazon Kinesis Data Streams & data firehose stream for ingestion to S3 Tables. (Transform using lambda)
      - Query using Athena and can modify realtime.
    - Amazon Quicksight - Good Integration with Amazon Q for out of box dashboard creations.