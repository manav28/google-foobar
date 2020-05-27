"""
Decodes and prints the coded message after solving all 5 levels!
"""
from base64 import b64decode


def decode(key, message):
    """
    Decodes a base64 encoded message.

    Args:
        key: A string denoting the key for decoding.
        message: A string denoting the base64 encoding of the message.

    Returns:
        A string denoting the decoded message.
    """
    result = []
    for i, char in enumerate(b64decode(message)):
        result.append(chr(char ^ ord(key[i % len(key)])))

    return "".join(result)


USERNAME = "paste_user_name_here"
MESSAGE = """paste_base64_code_here"""
print(decode(USERNAME, MESSAGE))
