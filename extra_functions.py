import re

def password_valid(passkey):
    chr_list = [r'[A-Z]', r'[a-z]', r'\d', r'[!@#$%^&*()-+]']   
    if not(len(passkey) >= 12):
        return False
    else:
        for text_chunk in chr_list:
            if re.search(text_chunk, passkey) is None:
                return False
    return True

