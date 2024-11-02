CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mode VARCHAR(10),
    icon_url TEXT,
    status_message TEXT,
    link_token TEXT
);

CREATE TABLE analysis (
    analysis_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    personality TEXT,
    strength TEXT,
    weakness TEXT
);

CREATE TABLE diary (
    diary_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    date DATE,
    title TEXT,
    summary TEXT,
    feedback TEXT
);

CREATE TABLE message (
    message_id SERIAL PRIMARY KEY,
    diary_id INTEGER REFERENCES diary(diary_id),
    user_id INTEGER REFERENCES users(user_id),
    media_type VARCHAR(10),
    content TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analysis_user_id ON analysis(user_id);
CREATE INDEX idx_diary_user_id ON diary(user_id);
CREATE INDEX idx_message_diary_id ON message(diary_id);
CREATE INDEX idx_message_user_id ON message(user_id);

CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$
 language 'plpgsql';

CREATE TRIGGER update_user_modtime
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

