from flask import Flask, request, render_template_string
import sqlite3
import base64

app = Flask(__name__)

# In-memory SQLite database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Dark-Themed HTML Template
login_page = """
<!doctype html>
<html lang="en">
    <head>
        <title>Login</title>
        <style>
            body {
                background-color: #121212;
                color: #e0e0e0;
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                color: #cf2d2d;
            }
            form {
                background-color: #1e1e1e;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
            }
            label {
                display: block;
                margin: 10px 0 5px;
            }
            input {
                width: 100%;
                padding: 8px;
                margin-bottom: 15px;
                border: none;
                border-radius: 4px;
                background-color: #2c2c2c;
                color: #e0e0e0;
            }
            button {
                width: 100%;
                padding: 10px;
                background-color: #cc3535;
                color: #121212;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #d94545;
            }
            p {
                color: #cc3535;
            }
        </style>
    </head>
    <body>
        <h1>Super Secret Site</h1>
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" name="username" id="username" required>
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" required>
            <button type="submit">Login</button>
        </form>
        {% if error %}
        <p>{{ error }}</p>
        {% endif %}
    </body>
</html>
"""
string = 'YmFqYWJsYXN0aXNiZXN0'
pswd = base64.b64decode(string).decode()
secret_page = f"""
    <!doctype html>
    <html lang="en">
        <head>
            <title>Secret Password</title>
            <style>
                body {{
                    background-color: #121212;
                    color: #cc3535;
                    font-family: Arial, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }}
                h1 {{
                    color: #cc3535;
                }}
                p {{
                    font-size: 18px;
                    color: #cc3535;
                }}
                strong {{
                    color: #cc3535;
                }}
            </style>
        </head>
        <body>
            <h1>Welcome!</h1>
            <p>The secret password is: <strong>{pswd}</strong></p>
        </body>
    </html>
    """

# Routes
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # SQL Injection Vulnerable Query
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing Query: {query}")  # Debugging purpose
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template_string(secret_page)
        else:
            error = "Invalid username or password!"

    return render_template_string(login_page, error=error)

if __name__ == "__main__":
    app.run(debug=True)
