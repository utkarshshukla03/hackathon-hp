import hashlib

def generate_item_code(canonical_name):
    base = canonical_name.upper().replace(" ", "_")
    hash_part = hashlib.md5(canonical_name.encode()).hexdigest()[:4]
    return f"{base}_{hash_part}"
