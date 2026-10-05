import hashlib
import re

class AuthService:
    def __init__(self, repository):
        self.repo = repository
        self.current_user = None

    def _hash_pw(self, raw_password: str) -> str:
        return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()

    def validate_registration(self, email: str, password: str, confirm_password: str = None):
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email.strip()):
            return False, "Please enter a valid email address."

        if len(password) < 7:
            return False, "Password must be at least 7 characters long."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least 1 uppercase letter."
        if not re.search(r"\d", password):
            return False, "Password must contain at least 1 number."

        if confirm_password is not None and password != confirm_password:
            return False, "Passwords do not match."

        return True, ""

    def register(self, email: str, password: str, confirm_password: str = None):
        valid, msg = self.validate_registration(email, password, confirm_password)
        if not valid:
            return False, msg

        if self.repo.find_by_email(email):
            return False, "An account with this email already exists."

        self.repo.create_user(email, self._hash_pw(password))
        return True, "Account registered successfully! Please log in."

    def login(self, email: str, password: str):
        email = email.strip()
        user = self.repo.find_by_email(email)
        if not user or user.password != self._hash_pw(password):
            return False, "Invalid email or password."
        self.current_user = user
        return True, "Login successful!"

    def logout(self):
        self.current_user = None