def md5(string_to_hash: str):
    # Return MD5 string
    import hashlib
    return hashlib.md5(string_to_hash.encode()).hexdigest()
