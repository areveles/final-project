import re

def password_valid(passkey):
    pattern = r"\"?([-a-zA-Z0-9.`?{}_]+@\w+\.\w{3})\"?"
    chr_list = [r'[A-Z]', r'[a-z]', r'\d', r'[!@#$%^&*()-+]']   
    if not((len(passkey) >= 12) and (re.match(pattern, passkey))):
        return False
    else:
        for text_chunk in chr_list:
            if re.search(text_chunk, passkey) is None:
                return False
    return True

