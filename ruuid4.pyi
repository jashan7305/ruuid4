def uuid1() -> str:
    """
    Generate a UUID version 1 (time-based) using a random multicast Node ID.
    
    The Node ID is generated once at startup to avoid expensive OS syscalls.
    """
    ...

def uuid3(namespace: str, name: str) -> str:
    """
    Generate a UUID version 3 (MD5 hash-based).
    
    Args:
        namespace: A UUID string or one of "DNS", "URL", "OID", "X500".
        name: The name string to hash.
    """
    ...

def uuid4() -> str:
    """
    Generate a UUID version 4 (random).
    (If you dont know what uuids are, use this)
    """
    ...

def uuid5(namespace: str, name: str) -> str:
    """
    Generate a UUID version 5 (SHA-1 hash-based).
    
    Args:
        namespace: A UUID string or one of "DNS", "URL", "OID", "X500".
        name: The name string to hash.
    """
    ...

def uuid6() -> str:
    """
    Generate a UUID version 6 (sortable time-based).
    
    Similar to v1, but field ordering is optimized for database sorting.
    """
    ...

def uuid7() -> str:
    """
    Generate a UUID version 7 (sortable Unix Epoch time).
    
    This is the modern standard for database primary keys.
    """
    ...

def uuid8(data: bytes) -> str:
    """
    Generate a UUID version 8 (custom/vendor-specific).
    
    Args:
        data: Exactly 16 bytes of data.
    """
    ...

def uuid4_bulk(count: int) -> list[str]:
    """
    Generate a list of UUID version 4 strings in bulk.
    
    This is significantly faster than calling uuid4() in a loop.
    """
    ...