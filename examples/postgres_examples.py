"""
PostgreSQL integration example with LangChain
"""
import asyncio
import os

import asyncpg
import psycopg2
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

def get_database_url():
    """Get the database URL from environment variables"""
    database_url = os.getenv("DATABASE_URL", None)
    if not database_url:
        print("❌ DATABASE_URL not set! Please check your .env file.")
        exit(1)
    return database_url

def test_postgres_connection():
    """Test PostgreSQL connection using psycopg2"""

    database_url = get_database_url()
    print(f"🔗 Connecting to PostgreSQL: {database_url}")

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Test connection
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL connection successful!")
        print(f"📊 Version: {version['version'][:50]}...")

        # Test our initialized table
        cursor.execute("SELECT COUNT(*) as count FROM langchain_test;")
        count = cursor.fetchone()
        print(f"📝 Test table has {count['count']} records")

        # Insert a test record
        cursor.execute(
            "INSERT INTO langchain_test (content, metadata) VALUES (%s, %s) RETURNING id;",
            ("Test from Python", '{"source": "python_test"}')
        )
        new_id = cursor.fetchone()
        print(f"📝 Inserted new record with ID: {new_id['id']}")

        # Clean up
        cursor.execute("DELETE FROM langchain_test WHERE id = %s;", (new_id['id'],))
        conn.commit()
        print("🧹 Cleaned up test data")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("Make sure PostgreSQL container is running!")
        return False

async def test_async_postgres():
    """Test async PostgreSQL connection using asyncpg"""

    database_url = get_database_url()
    print(f"🔗 Testing async connection to PostgreSQL...")

    try:

        # Connect to PostgreSQL
        conn = await asyncpg.connect(database_url)

        # Test connection
        version = await conn.fetchval("SELECT version();")
        print(f"✅ Async PostgreSQL connection successful!")
        print(f"📊 Version: {version[:50]}...")

        # Test query
        records = await conn.fetch("SELECT content, metadata FROM langchain_test LIMIT 2;")
        print(f"📚 Found {len(records)} test records:")
        for record in records:
            print(f"   - {record['content'][:30]}...")

        await conn.close()
        return True

    except Exception as e:
        print(f"❌ Async PostgreSQL connection failed: {e}")
        return False

def demo_langchain_postgres():
    """Demonstrate using PostgreSQL with LangChain"""
    try:
        database_url = get_database_url()

        print("✅ LangChain PostgreSQL integration available!")
        print("💡 You can use PGVector for vector storage")
        print("📖 Example usage:")
        print("   embeddings = OpenAIEmbeddings()")
        print("   vectorstore = PGVector.from_documents(docs, embeddings, connection_string=database_url)")

        return True

    except ImportError as e:
        print(f"⚠️  LangChain PostgreSQL not available: {e}")
        print("This is normal if you haven't set up OpenAI embeddings yet")
        return False

def demo_conversation_storage():
    """Demonstrate storing conversation history in PostgreSQL"""
    database_url = get_database_url()
    try:
        import uuid

        import psycopg2
        from psycopg2.extras import RealDictCursor

        conn = psycopg2.connect(database_url)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Create a sample conversation
        session_id = str(uuid.uuid4())

        # Add messages to conversation
        messages = [
            ("human", "Hello, I want to learn about LangChain"),
            ("ai", "LangChain is a framework for building applications with language models..."),
            ("human", "Can you give me an example?"),
            ("ai", "Sure! Here's a simple example of using LangChain...")
        ]

        for msg_type, content in messages:
            cursor.execute(
                """INSERT INTO conversation_history (session_id, message_type, content, metadata)
                   VALUES (%s, %s, %s, %s)""",
                (session_id, msg_type, content, '{"example": true}')
            )

        conn.commit()

        # Retrieve conversation
        cursor.execute(
            "SELECT message_type, content FROM conversation_history WHERE session_id = %s ORDER BY created_at",
            (session_id,)
        )

        conversation = cursor.fetchall()
        print("💬 Sample conversation stored and retrieved:")
        for msg in conversation:
            print(f"   {msg['message_type'].upper()}: {msg['content'][:50]}...")

        # Clean up
        cursor.execute("DELETE FROM conversation_history WHERE session_id = %s", (session_id,))
        conn.commit()
        print("🧹 Cleaned up conversation data")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Conversation storage demo failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing PostgreSQL integration...\n")

    # Test basic PostgreSQL connection
    if test_postgres_connection():
        print("\n" + "="*50 + "\n")

        # Test async connection
        asyncio.run(test_async_postgres())

        print("\n" + "="*50 + "\n")

        # Test LangChain integration
        demo_langchain_postgres()

        print("\n" + "="*50 + "\n")

        # Test conversation storage
        demo_conversation_storage()

    print("\n🎉 PostgreSQL testing complete!")
    print("💡 Your database is ready for LangChain applications!")
