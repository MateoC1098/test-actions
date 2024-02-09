import uuid

def is_valid_uuid4(s):
    try:
        uuid_obj = uuid.UUID(s)
        return str(uuid_obj) == s
    except ValueError:
        return False