# ruuid4

## Installation
```bash
pip install ruuid4
```

🔗 **Source:**
https://github.com/jashan7305/ruuid4

`ruuid4` is a tiny, fast UUID generator implemented in rust and exposed to python using PyO3.

## Features
- Generates RFC-4122 compliant UUID values (v1, v3, v4, v5, v6, v7, v8)
- Powered by Rust’s `uuid` crate
- Zero dependencies for Python users

## Functions
- `uuid1()` : Returns a UUIDv1 string (time-based using a random multicast Node ID).
- `uuid3(namespace, name)` : Returns a UUIDv3 string (MD5 hash-based).
- `uuid4()` : Returns a UUIDv4 string (random).
- `uuid5(namespace, name)` : Returns a UUIDv5 string (SHA-1 hash-based).
- `uuid6()` : Returns a UUIDv6 string (sortable, Gregorian time-based).
- `uuid7()` : Returns a UUIDv7 string (sortable, Unix Epoch time-based).
- `uuid8(data)` : Returns a UUIDv8 string (custom, requires exactly 16 bytes).
- `uuid4_bulk(count)` : Returns a list of UUIDv4 strings (optimized for bulk generation).

## Example

```python
import ruuid4

print(ruuid4.uuid4())
```