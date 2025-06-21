#!/usr/bin/env python3
"""
Privacy Test Application - Vulnerable by Design
This application contains intentional security vulnerabilities for testing purposes.
DO NOT USE IN PRODUCTION.
"""

import os
import sqlite3
import hashlib
import logging
from flask import Flask, request, jsonify
import requests
import jwt

app = Flask(__name__)

# Hardcoded credentials (VULNERABILITY: Hardcoded secrets)
API_KEY = "AIzaSyDrBGPrvperf5A3vEo9b9jdHGU7d8p7yGQ"
DATABASE_PASSWORD = "admin123!@#"
JWT_SECRET = "my-super-secret-jwt-key-2024"
ADMIN_TOKEN = "ghp_x0YfN6FzT8mtyDGCf5GlkJHvW2VnDc3Kjdhf"

# AWS credentials (VULNERABILITY: Embedded AWS credentials)
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Database connection string (VULNERABILITY: Connection string with password)
DB_CONNECTION = "postgresql://admin:SuperSecret123!@localhost:5432/userdb"

# Logging configuration (VULNERABILITY: Logging sensitive data)
logging.basicConfig(level=logging.DEBUG, filename='app.log')

def get_user(user_id):
    """VULNERABILITY: SQL Injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    logging.debug(f"Executing query: {query}")
    cursor.execute(query)
    return cursor.fetchone()

@app.route('/login', methods=['POST'])
def login():
    """VULNERABILITY: Password stored in plain text"""
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Log credentials (VULNERABILITY: Logging passwords)
    logging.info(f"Login attempt - Username: {username}, Password: {password}")
    
    # Simple MD5 hash (VULNERABILITY: Weak hashing)
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    # Hardcoded admin check (VULNERABILITY: Hardcoded credentials)
    if username == "admin" and password == "admin123":
        token = jwt.encode({'user': username}, JWT_SECRET, algorithm='HS256')
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/external', methods=['GET'])
def external_api():
    """VULNERABILITY: API key in URL"""
    url = f"https://api.example.com/data?api_key={API_KEY}"
    response = requests.get(url, verify=False)  # VULNERABILITY: SSL verification disabled
    return response.json()

@app.route('/user/<user_id>')
def user_profile(user_id):
    """VULNERABILITY: Direct object reference"""
    user = get_user(user_id)
    if user:
        # Return sensitive data (VULNERABILITY: Data exposure)
        return jsonify({
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'ssn': user[3],
            'credit_card': user[4]
        })
    return jsonify({'error': 'User not found'}), 404

# Private keys (VULNERABILITY: Embedded private keys)
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAn5R+cHW8H+k3kEgp5ftjTa5fC9Z5tu2r7g52pJBs8MxNVoMn
4xblqgQxCBS8mM8LiHqM1K7Lxvn6P5n5h7tZr5ViNwR7BFKJp7M6vMnkZJRLKFCp
-----END RSA PRIVATE KEY-----"""

if __name__ == '__main__':
    # Running in debug mode (VULNERABILITY: Debug mode in production)
    app.run(debug=True, host='0.0.0.0', port=5000)