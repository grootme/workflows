-- JARVIS Database Initialization
-- Creates required tables for n8n + LangChain memory + error handling

-- LangChain chat history table
CREATE TABLE IF NOT EXISTS message_store (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    message JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Error log table
CREATE TABLE IF NOT EXISTS error_log (
    id SERIAL PRIMARY KEY,
    workflow_name VARCHAR(255),
    error_message TEXT,
    error_severity VARCHAR(50),
    node_name VARCHAR(255),
    execution_id VARCHAR(255),
    payload JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics table
CREATE TABLE IF NOT EXISTS workflow_analytics (
    id SERIAL PRIMARY KEY,
    workflow_name VARCHAR(255),
    execution_id VARCHAR(255),
    status VARCHAR(50),
    duration_ms INTEGER,
    tokens_used INTEGER,
    cost_usd DECIMAL(10, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_message_store_session ON message_store(session_id);
CREATE INDEX IF NOT EXISTS idx_error_log_severity ON error_log(error_severity);
CREATE INDEX IF NOT EXISTS idx_error_log_created ON error_log(created_at);
CREATE INDEX IF NOT EXISTS idx_workflow_analytics_name ON workflow_analytics(workflow_name);
CREATE INDEX IF NOT EXISTS idx_workflow_analytics_created ON workflow_analytics(created_at);

-- Zep database (enterprise)
CREATE DATABASE IF NOT EXISTS zep;
