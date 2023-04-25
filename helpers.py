from functools import wraps

from flask import redirect, render_template, request, session


# Asks to login users without session 
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Check password strength
def password_strength(password, username):
    #TODO: check password strength according to 
    # https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements
    
    # Check if username is in password
    if username.lower() in password.lower():
        return "Password should not include username."
    
    # Check if has uppercase letters
    if not (any(char.isupper() for char in password)):
        return "Password should include uppercase letters."
    
    # Check if has lowercase letters
    if not (any(char.islower() for char in password)):
        return "Password should include lowercase letters."
    
    # Check if has base digits
    if not (any(char.isdigit() for char in password)):
        return "Password should include digits."
    
    # Check if has special charcters
    special_characters = ['~','!','@','#','$','%','^','&','*','_','-',
                          '+','=','`','|','\\','(',')','{','}','[',']',
                          ':',';','"',"'",'<','>',',','.','?','/']
    if not (any(char in special_characters for char in password)):
        return "Password should include special characters."
    
    # Check minimum length of 8 characters
    if len(password) < 8:
        return "Password should be longer than 8 characters."
    
    return True