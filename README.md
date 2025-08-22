# LangChain Development Container

A complete VSCode development container setup for testing and developing with LangChain.

## Quick Start

1. **Clone/create your project directory**
2. **Create .env file** from the .env.example
3. **Open in VSCode** and select "Reopen in Container" when prompted

## What's Included

### 🐍 Python Environment
- Python 3.11 slim base image
- All major LangChain packages pre-installed
- Popular LLM integrations (OpenAI, Anthropic, Google, Ollama)
- Vector stores (Chroma, Pinecone, FAISS)
- Document processing tools

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
│   └── Dockerfile
├── examples/
│   └── basic_example.py
├── tests/
│   └── test_basic_langchain.py
├── notebooks/          # For Jupyter notebooks
├── data/              # For data files
├── requirements.txt
├── setup.py
├── .env.example
├── .env              # Your actual environment variables
└── README.md
```

## Getting Started

### 1. Environment Setup

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### 2. Test Your Setup

Run the basic example to verify everything works:

```bash
python examples/basic_example.py
```

This will:
- Test LangChain components without API calls
- Test a full chain with your configured LLM (if API key provided)

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

## Port Forwarding

The container automatically forwards these ports:
- **8000**: General web development
- **8080**: Alternative web port  
- **8888**: Jupyter Lab

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

Happy coding with LangChain! 🦜🔗