-- Initialize LangChain development database
-- This file runs automatically when PostgreSQL container starts for the first time

-- Create extensions for vector operations (if needed)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create a simple table for testing
CREATE TABLE IF NOT EXISTS langchain_test (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some test data
INSERT INTO langchain_test (content, metadata) VALUES
    ('This is a test document for LangChain', '{"type": "test", "source": "init"}'),
    ('Another test document', '{"type": "test", "source": "init"}')
ON CONFLICT DO NOTHING;

-- Create a table for LangChain conversation history
CREATE TABLE IF NOT EXISTS conversation_history (
    id SERIAL PRIMARY KEY,
    session_id UUID DEFAULT uuid_generate_v4(),
    message_type VARCHAR(20) NOT NULL, -- 'human' or 'ai'
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_conversation_session ON conversation_history(session_id);
CREATE INDEX IF NOT EXISTS idx_conversation_created ON conversation_history(created_at);

-- Notify that initialization is complete
DO $$
BEGIN
    RAISE NOTICE 'LangChain database initialization complete!';
END $$;