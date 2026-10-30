CREATE TABLE IF NOT EXISTS poll (
    poll_id INT NOT NULL AUTO_INCREMENT,
    poll_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (poll_id)
);

CREATE TABLE IF NOT EXISTS question (
    question_id INT NOT NULL AUTO_INCREMENT,
    poll_id INT NOT NULL,
    question_text VARCHAR(500) NOT NULL,
    PRIMARY KEY (question_id),
    UNIQUE (poll_id, question_text),
    FOREIGN KEY (poll_id) REFERENCES poll(poll_id)
);

CREATE TABLE IF NOT EXISTS answer_option (
    option_id INT NOT NULL AUTO_INCREMENT,
    question_id INT NOT NULL,
    option_text VARCHAR(255) NOT NULL,
    PRIMARY KEY (option_id),
    UNIQUE (question_id, option_text),
    FOREIGN KEY (question_id) REFERENCES question(question_id)
);

CREATE TABLE IF NOT EXISTS user_answer (
    answer_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    option_id INT,
    PRIMARY KEY (answer_id),
    UNIQUE (user_id, question_id),
    FOREIGN KEY (question_id) REFERENCES question(question_id),
    FOREIGN KEY (option_id) REFERENCES answer_option(option_id)
);
