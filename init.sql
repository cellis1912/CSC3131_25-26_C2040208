CREATE TABLE IF NOT EXISTS job_allocations 
(
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    person VARCHAR(255) NOT NULL,
    time_estimate DECIMAL(5, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO job_allocations (title, person, time_estimate)
VALUES 
('Design Homepage', 'Alice Johnson', 12.50),
('Write Blog Post', 'Ben Carter', 3.75),
('Database Optimization', 'Clara Zhang', 8.25),
('Client Meeting', 'David Lee', 2.00),
('Code Review', 'Ella Thompson', 4.50),
('Marketing Strategy', 'Frank O’Neil', 6.00),
('UX Testing', 'Grace Kim', 5.25),
('Server Maintenance', 'Henry Wallace', 7.00),
('Social Media Campaign', 'Isla Morgan', 4.75),
('Product Demo Prep', 'Jack Patel', 3.25);