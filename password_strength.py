import re
import random
import math
import streamlit as st

# List of common weak passwords
weak_passwords = ["password", "123456", "12345678", "qwerty", "abc123", "password123", "admin", "letmein"]

# Function to calculate password entropy
def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26  # Lowercase letters
    if re.search(r"[A-Z]", password): charset += 26  # Uppercase letters
    if re.search(r"\d", password): charset += 10     # Digits
    if re.search(r"[!@#$%^&*]", password): charset += 8  # Special characters

    entropy = len(password) * math.log2(charset) if charset else 0
    return entropy

# Function to check password strength with a complex scoring system
def check_password_strength(password):
    score = 0
    feedback = []

    # Blacklist Check
    if password.lower() in weak_passwords:
        return "❌ Weak - Common Password", "Choose a unique password not in the common list."

    # Length Check (Weighted Score)
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Entropy Calculation (Strength Prediction)
    entropy = calculate_entropy(password)
    if entropy > 60:
        strength = "✅ Very Strong"
    elif entropy > 45:
        strength = "✅ Strong"
    elif entropy > 30:
        strength = "⚠️ Moderate"
    else:
        strength = "❌ Weak"

    return strength, "\n".join(feedback) if feedback else "Good Job! Your password is secure."

# Function to generate a strong password
def generate_strong_password():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return "".join(random.sample(chars, 14))

# Streamlit UI
st.title("🔐 Password Strength Meter made by owais")
st.write("Enter a password to check its security and get improvement suggestions.")

password = st.text_input("Enter Password:", type="password")

if password:
    strength, feedback = check_password_strength(password)
    st.markdown(f"### **Strength: {strength}**")
    if feedback:
        st.warning(feedback)

    if strength.startswith("❌ Weak"):
        st.info(f"🔹 **Suggested Strong Password:** `{generate_strong_password()}`")
