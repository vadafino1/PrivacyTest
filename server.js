const express = require('express');
const crypto = require('crypto');
const mysql = require('mysql2');
const jwt = require('jsonwebtoken');
const fs = require('fs');

const app = express();
app.use(express.json());

// Hardcoded secrets (VULNERABILITY: Hardcoded credentials)
const JWT_SECRET = 'super-secret-jwt-key-do-not-share';
const ENCRYPTION_KEY = 'MySecretEncryptionKey123!@#';
const ADMIN_PASSWORD = 'SuperAdmin2024!';

// API Keys (VULNERABILITY: Hardcoded API keys)
const STRIPE_SECRET_KEY = 'sk_live_fake_51HCgMAD5L5DhKR1M9I4vGo3wZzjH2jIqpKnJgCKYZo6XRMqGYhpvLZGrWe8MZJXf2nYfQRJkjH8hNdv';
const GOOGLE_API_KEY = 'AIzaSyBxkNKL4TGZZoKjvpJGRWNTJh7SgKVzHaY';
const FACEBOOK_APP_SECRET = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6';

// Twilio credentials with corrected prefix (VULNERABILITY: Hardcoded Twilio credentials)
const TWILIO_ACCOUNT_SID = 'TWL6ffc125ba936a44d3b6e80d1b5c3e1234';
const TWILIO_AUTH_TOKEN = 'your_auth_token_here_12345';

// Database connection (VULNERABILITY: Hardcoded database credentials)
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'RootPassword123!',
    database: 'sensitive_data',
    port: 3306
});

// Private key (VULNERABILITY: Embedded private key)
const PRIVATE_KEY = `-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKB
wko1vdKEOpMTgKOvBhUvpQcL9+Xf+/YCk4fgOyLJh+8gqFNhEKGfvKI2IQD7OT8u
lp/8Uh5Aq9Gm6hD/vfGI8Qnm7Ql7YP3YXQNJj5Nf8b8I6Q3gqL5Wj7Ys3m3Dn0gv
RYCNZgHEFfvBJvhFQvDvLgRjAHG3lJcQaRdIWfGq6JfTlcfTwQ6TBjgQrVgzQCPE
P0yTFNKvTXKL3lXHXJ8mLaXhqv7bJPfQNrP3Bj6uqpqrHWrRgVaGrGdpEP4qbYZc
-----END PRIVATE KEY-----`;

// Logging function (VULNERABILITY: Logs sensitive data)
function logSensitiveData(data) {
    const logEntry = `${new Date().toISOString()} - Sensitive data: ${JSON.stringify(data)}\n`;
    fs.appendFileSync('server.log', logEntry);
}

// Vulnerable SQL query (VULNERABILITY: SQL Injection)
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    
    // Log credentials (VULNERABILITY: Logging passwords)
    console.log(`Login attempt: ${username}:${password}`);
    logSensitiveData({ username, password, timestamp: new Date() });
    
    // SQL Injection vulnerability
    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
    
    db.query(query, (err, results) => {
        if (err) {
            console.error('Database error:', err);
            return res.status(500).json({ error: 'Database error' });
        }
        
        if (results.length > 0) {
            const token = jwt.sign({ userId: results[0].id }, JWT_SECRET);
            res.json({ token, user: results[0] });
        } else {
            res.status(401).json({ error: 'Invalid credentials' });
        }
    });
});

// Vulnerable user data endpoint (VULNERABILITY: Exposes PII)
app.get('/api/users/:id', (req, res) => {
    const userId = req.params.id;
    
    // Direct object reference vulnerability
    const query = `SELECT id, username, email, ssn, phone, address, credit_card FROM users WHERE id = ${userId}`;
    
    db.query(query, (err, results) => {
        if (err) {
            return res.status(500).json({ error: 'Database error' });
        }
        
        if (results.length > 0) {
            // Log sensitive data access (VULNERABILITY: Logging PII)
            logSensitiveData({ 
                action: 'user_data_access', 
                userId: userId, 
                ssn: results[0].ssn,
                creditCard: results[0].credit_card 
            });
            
            res.json(results[0]);
        } else {
            res.status(404).json({ error: 'User not found' });
        }
    });
});

// Payment processing endpoint (VULNERABILITY: Exposes payment data)
app.post('/api/payments', (req, res) => {
    const { amount, cardNumber, cvv, expiryDate } = req.body;
    
    // Log payment details (VULNERABILITY: Logging payment card data)
    const paymentLog = {
        timestamp: new Date(),
        amount: amount,
        cardNumber: cardNumber,
        cvv: cvv,
        expiryDate: expiryDate,
        stripeKey: STRIPE_SECRET_KEY
    };
    
    logSensitiveData(paymentLog);
    
    // Simulate payment processing
    res.json({ 
        success: true, 
        transactionId: crypto.randomBytes(16).toString('hex'),
        cardLast4: cardNumber.slice(-4)
    });
});

// Admin endpoint with hardcoded password (VULNERABILITY: Hardcoded admin access)
app.post('/admin/backdoor', (req, res) => {
    const { password } = req.body;
    
    if (password === ADMIN_PASSWORD) {
        res.json({ 
            message: 'Admin access granted',
            databasePassword: 'RootPassword123!',
            awsKey: 'AKIAIOSFODNN7EXAMPLE',
            awsSecret: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        });
    } else {
        res.status(401).json({ error: 'Access denied' });
    }
});

// Environment variables exposure (VULNERABILITY: Exposes environment)
app.get('/debug/env', (req, res) => {
    res.json({
        environment: process.env,
        secrets: {
            jwtSecret: JWT_SECRET,
            stripeKey: STRIPE_SECRET_KEY,
            googleApiKey: GOOGLE_API_KEY
        }
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`JWT Secret: ${JWT_SECRET}`);
    console.log(`Stripe Key: ${STRIPE_SECRET_KEY}`);
});