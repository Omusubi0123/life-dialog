CREATE TABLE user (
    user_id SERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    icon_url TEXT,
    linkToken TEXT,
    line_status TEXT,
);

CREATE TABLE analysis (
    user_id INT REFERENCES users(user_id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    personality TEXT,
    strengths TEXT,
    weaknesses TEXT,
);

CREATE TABLE diary (
    diary_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title TEXT,
    content TEXT,
    feedback TEXT,
);

CREATE TABLE message (
    message_id SERIAL PRIMARY KEY,
    diary_id INT REFERENCES diary(diary_id),
    user_id INT REFERENCES users(user_id),
    message_text TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);
