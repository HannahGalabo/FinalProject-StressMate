from features.authentication.model import User

class AuthRepository:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def find_by_email(self, email: str):
        conn = self.db_conn.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, password FROM users WHERE LOWER(email) = LOWER(?)", (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(id=row["id"], email=row["email"], password=row["password"])
        return None

    def create_user(self, email: str, password_hash: str):
        conn = self.db_conn.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email.lower(), password_hash))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return User(id=user_id, email=email.lower(), password=password_hash)