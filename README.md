# LangChain Development Container

A simple VSCode development container setup for testing and developing with LangChain and Jupyter Notebooks

## Quick Start

1. **Clone/create your project directory**
2. **Open in VSCode** and select "Reopen in Container" when prompted

## What's Included

### 🐍 Python Environment
- Python 3.13 slim base image
- All major LangChain packages pre-installed
- Popular LLM integrations (OpenAI, Anthropic, Google, Ollama)
- Vector stores (Chroma, Pinecone, PostgreSQL, FAISS)
- Document processing tools

### 🗄️ Database Stack
- **PostgreSQL 15** - Persistent database with vector storage support
- **Redis 7** - Caching and session storage
- **Automated setup** - Databases configured and ready to use
- **Data persistence** - Volumes survive container rebuilds

### 🛠️ Development Tools
- **Testing**: pytest with async support
- **Formatting**: black, isort for code formatting
- **Linting**: pylint, ruff, mypy for code quality
- **Jupyter**: Full Jupyter Lab environment for notebooks
- **Git**: Git and GitHub CLI pre-configured

### 📦 VSCode Extensions
- Python language support with IntelliSense
- Jupyter notebook support
- Code formatting and linting
- Test discovery and running
- YAML and JSON support

## Project Structure

```
your-project/
├── .devcontainer/
│   ├── devcontainer.json
│   ├── Dockerfile
│   └── docker-compose.yml
├── sql/
│   └── migrate           # Folder for SQL migration scripts
│   └── initdb.sql        # PostgreSQL initialization
├── examples/
│   ├── basic_example.py
│   ├── redis_example.py  # Redis integration examples
│   └── postgres_example.py # PostgreSQL examples
├── tests/
│   └── test_basic_langchain.py
├── notebooks/            # For Jupyter notebooks
├── data/                 # For data files
├── requirements.txt
├── setup.py
├── .env.example
├── .env                  # Your actual environment variables
└── README.md
```

## Getting Started

### 1. Environment Setup

On first build the script will copy `.env.example` to `.env` and add your API keys.

The container automatically reads environment variables from your host environment such as
`OPENAI_API_KEY` and `ANTHROPIC_API_KEY` but you can override specific ones in the `.env` file if required.

### 2. Test Your Setup

Run the basic example to verify everything works:

```bash
python examples/basic_example.py
```

This will:
- Test LangChain components without API calls
- Test a full chain with your configured LLM (if API key provided)
### 3. Test Database Connections

Test Redis integration:
```bash
python examples/redis_example.py
```

Test PostgreSQL integration:
```bash
python examples/postgres_example.py
```

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_basic_langchain.py
```

### 4. Start Jupyter Lab

```bash
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

## Common LangChain Patterns

### Basic Chain
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
llm = ChatOpenAI()
parser = StrOutputParser()

chain = prompt | llm | parser
result = chain.invoke({"topic": "AI"})
```

### With Memory
```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)
```

### With Redis Caching
```python
from langchain_community.cache import RedisCache
from langchain.globals import set_llm_cache
import redis

redis_client = redis.from_url("redis://redis:6379")
cache = RedisCache(redis_=redis_client)
set_llm_cache(cache)
```

### With PostgreSQL Vector Store
```python
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectorstore = PGVector.from_documents(
    documents=docs,
    embedding=embeddings,
    connection_string="postgresql://langchain:password@postgres:5432/langchain_dev"
)
```


### RAG Pattern
```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA

# Create vector store
vectorstore = Chroma.from_texts(
    texts=["Your documents here"],
    embedding=OpenAIEmbeddings()
)

# Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
```

## Customization

### Adding New Dependencies

Add to `requirements.txt` and rebuild the container:

```bash
# In VSCode command palette
> Dev Containers: Rebuild Container
```

### Changing Python Version

Modify the `FROM` line in `.devcontainer/Dockerfile`:

```dockerfile
FROM python:3.12-slim  # Change to desired version
```

### Adding System Packages

Add to the `apt-get install` section in the Dockerfile:

```dockerfile
RUN apt-get update && apt-get install -y \
    your-new-package \
    # ... existing packages
```

### Adding SQL Tables
The default DB uses the [Simple Schema Versions](https://github.com/marklynch/simple-schema-versions)
pattern and functions to manage the db migrations.

To update the initdb.sql you can run the following command and it will merge all migrations:
```bash
find migrate -name "*.sql" -type f | sort -V | while read file; do echo "-- source: $file";  cat "$file"; echo "\n"; done > initdb.sql
```
Note the DB persists between rebuilds - so you can manually run these scripts on the DB also.

## Port Forwarding

The container automatically forwards these ports:
- **8000**: General web development
- **8080**: Alternative web port
- **8888**: Jupyter Lab
- **6379**: Redis
- **5432**: PostgreSQL

## Data Persistence

### What Persists (Stored on Host)
- Your source code and configuration files
- Environment variables in `.env`
- Data files you create in `data/`, `notebooks/`, etc.

### What's Stored in Docker Volumes
- **PostgreSQL data**: Persists across container rebuilds
- **Redis data**: Persists across container rebuilds
- **Python packages**: Reinstalled on rebuild (cached for speed)

### Resetting Databases

**Reset everything:**
```bash
docker-compose -f .devcontainer/docker-compose.yml down
docker volume rm ai-poc_postgres-data ai-poc_redis-data
```

**Reset just PostgreSQL:**
```bash
docker volume rm ai-poc_postgres-data
```

## Troubleshooting

### Container Won't Start
- Check Docker is running
- Verify `.devcontainer/devcontainer.json` syntax
- Check Dockerfile for syntax errors

### Import Errors
- Ensure packages are in `requirements.txt`
- Rebuild container after adding dependencies
- Check Python path in VSCode settings

### API Key Issues
- Verify `.env` file is in project root
- Check environment variable names match exactly
- Restart container after adding new environment variables

### Permission Issues
- The container runs as `vscode` user (non-root)
- Files are owned by the user with UID 1000
- Use `sudo` if you need root access for system changes

## Next Steps

- Explore the `examples/` directory for more complex patterns
- Check out LangChain's documentation: https://python.langchain.com/
- Set up LangSmith for tracing: https://smith.langchain.com/
- Join the LangChain Discord community for support

## Architecture

This development environment provides a complete AI application stack:

```
┌───────────────────────────────────────-──┐
│           VSCode Dev Container           │
│  ┌─────────────────────────────────────┐ │
│  │         Python + LangChain          │ │
│  │     ┌─────────────────────────┐     │ │
│  │     │    Your Application     │     │ │
│  │     └─────────────────────────┘     │ │
│  └─────────────────────────────────────┘ │
│                      │                   │
│  ┌─────────────────────────────────────┐ │
│  │  Redis Container  │ PostgreSQL      │ │
│  │  (Caching &       │ Container       │ │
│  │   Sessions)       │ (Data & Vectors)│ │
│  └─────────────────────────────────────┘ │
└────────────────────────────────────────-─┘
```

Happy coding with LangChain! 🦜🔗🐘📮