CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users (
    user_id VARCHAR(40) PRIMARY KEY,
    name VARCHAR(40),
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE,
    mode VARCHAR(10),
    icon_url TEXT,
    status_message TEXT,
    link_token TEXT
);

CREATE TABLE analysis (
    analysis_id SERIAL PRIMARY KEY,
    user_id VARCHAR(40) REFERENCES users(user_id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    personality TEXT,
    strength TEXT,
    weakness TEXT
);

CREATE TABLE diary (
    diary_id SERIAL PRIMARY KEY,
    user_id VARCHAR(40) REFERENCES users(user_id),
    date DATE DEFAULT (CURRENT_DATE),
    title TEXT,
    summary TEXT,
    feedback TEXT
);

CREATE TABLE message (
    message_id SERIAL PRIMARY KEY,
    diary_id INTEGER REFERENCES diary(diary_id),
    user_id VARCHAR(40) REFERENCES users(user_id),
    media_type VARCHAR(10),
    content TEXT,
    sent_at TIME DEFAULT (CURRENT_TIME)
);

CREATE TABLE diary_vector (
    vector_id SERIAL PRIMARY KEY,
    user_id VARCHAR(40) REFERENCES users(user_id),
    diary_id INTEGER REFERENCES diary(diary_id),
    diary_content TEXT,
    diary_vector vector(1536),
    FOREIGN KEY(user_id) REFERENCES users (user_id),
    FOREIGN KEY(diary_id) REFERENCES diary (diary_id)
);