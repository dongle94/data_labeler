

def is_empty(data):
    if isinstance(data, str):
        return data.strip() == ""

    return False
