# NOTE: the tests are all ai generated, i dont know how to test.💩💩💩💩

import pytest
import ruuid4
import uuid
import re

# Regex patterns
# Standard UUID format (8-4-4-4-12 hex digits)
UUID_REGEX = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

# Version 4 specific regex (Version 4, Variant 1)
UUID4_REGEX = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")

def test_uuid1_format():
    """Test UUIDv1 (Time-based)"""
    u = ruuid4.uuid1()
    assert isinstance(u, str)
    assert UUID_REGEX.match(u)
    # Check version digit (13th char usually, but in string it's index 14)
    # xxxxxxxx-xxxx-1xxx-...
    assert u[14] == '1'

def test_uuid3_deterministic():
    """Test UUIDv3 (MD5) - should match python stdlib"""
    namespace = uuid.NAMESPACE_DNS
    name = "rust-python-bridge"
    
    # Expected from standard library
    expected = str(uuid.uuid3(namespace, name))
    
    # Test with stringified UUID namespace
    assert ruuid4.uuid3(str(namespace), name) == expected
    
    # Test with helper string "DNS"
    assert ruuid4.uuid3("DNS", name) == expected

def test_uuid4_format():
    """Test UUIDv4 (Random)"""
    u = ruuid4.uuid4()
    assert isinstance(u, str)
    assert UUID4_REGEX.match(u)
    # Explicitly check version '4'
    assert u[14] == '4'
    # Explicitly check variant (8, 9, a, b)
    assert u[19] in "89ab"

def test_uuid4_bulk():
    """Test Bulk Generation"""
    count = 1000
    uuids = ruuid4.uuid4_bulk(count)
    
    assert isinstance(uuids, list)
    assert len(uuids) == count
    assert isinstance(uuids[0], str)
    
    # Sanity check: verify valid v4 format for sample
    assert UUID4_REGEX.match(uuids[0])
    assert UUID4_REGEX.match(uuids[-1])
    
    # Probabilistic uniqueness check
    assert len(set(uuids)) == count

def test_uuid5_deterministic():
    """Test UUIDv5 (SHA-1) - should match python stdlib"""
    namespace = uuid.NAMESPACE_URL
    name = "https://www.rust-lang.org"
    
    expected = str(uuid.uuid5(namespace, name))
    
    # Test with stringified UUID namespace
    assert ruuid4.uuid5(str(namespace), name) == expected
    
    # Test with helper string "URL"
    assert ruuid4.uuid5("URL", name) == expected

def test_uuid6_format():
    """Test UUIDv6 (Sortable Gregorian)"""
    u = ruuid4.uuid6()
    assert UUID_REGEX.match(u)
    assert u[14] == '6'

def test_uuid7_format():
    """Test UUIDv7 (Sortable Unix Epoch)"""
    u = ruuid4.uuid7()
    assert UUID_REGEX.match(u)
    assert u[14] == '7'

def test_uuid8_custom():
    """Test UUIDv8 (Custom/Vendor)"""
    # 16 bytes of data
    data = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    u = ruuid4.uuid8(data)
    
    assert isinstance(u, str)
    assert UUID_REGEX.match(u)
    
    # The rust 'uuid' crate enforces RFC 4122 compliance for v8.
    # It modifies specific bits in byte 6 (version) and byte 8 (variant).
    # Byte 6: 0x06 -> 0x86 (Version 8)
    # Byte 8: 0x08 -> 0x88 (Variant 1)
    assert u == "00010203-0405-8607-8809-0a0b0c0d0e0f"

def test_error_handling():
    """Test invalid inputs raise ValueError"""
    
    # uuid8 with wrong length
    with pytest.raises(ValueError, match="uuid8 requires exactly 16 bytes"):
        ruuid4.uuid8(b'too short')
        
    # uuid3/5 with invalid namespace
    with pytest.raises(ValueError, match="Invalid Namespace"):
        ruuid4.uuid3("INVALID_NS", "test")

def test_namespace_helpers():
    """Test all supported namespace shortcuts"""
    name = "test"
    
    shortcuts = {
        "DNS": uuid.NAMESPACE_DNS,
        "URL": uuid.NAMESPACE_URL,
        "OID": uuid.NAMESPACE_OID,
        "X500": uuid.NAMESPACE_X500,
    }
    
    for shortcut, expected_ns in shortcuts.items():
        # Verify uuid3 resolution
        assert ruuid4.uuid3(shortcut, name) == str(uuid.uuid3(expected_ns, name))