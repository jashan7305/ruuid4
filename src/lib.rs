use pyo3::{exceptions::PyValueError, prelude::*};
use uuid::{Uuid};
use std::sync::OnceLock;

// helper functions and constants
static NODE_ID: OnceLock<[u8; 6]> = OnceLock::new();

// gets node id once. does not use actual mac address
#[inline]
fn get_node_id() -> &'static [u8; 6] {
    NODE_ID.get_or_init(|| {
        let rand_uuid = Uuid::new_v4();
        let bytes = rand_uuid.as_bytes();
        let mut node = [0u8; 6];
        node.copy_from_slice(&bytes[0..6]);
        node[0] |= 0x01;
        node
    })
}

// converts user input to valid namespace
// also accepts custom namespace
#[inline]
fn resolve_namespace(name: &str) -> PyResult<Uuid> {
    match name.to_uppercase().as_str() {
        "DNS" => Ok(Uuid::NAMESPACE_DNS),
        "URL" => Ok(Uuid::NAMESPACE_URL),
        "OID" => Ok(Uuid::NAMESPACE_OID),
        "X500" => Ok(Uuid::NAMESPACE_X500),
        _ => Uuid::parse_str(name)
            .map_err(|e| PyValueError::new_err(format!("Invalid Namespace {}", e)))
    }
}

// uuid v4 (ruuid4 v0.1.5)
// Version 4 UUIDs with random data.
#[pyfunction]
fn uuid4() -> PyResult<String> {
    Ok(Uuid::new_v4().to_string())
}

// uuid v1 (ruuid4 v 0.2.0)
// Version 1 UUIDs using a timestamp and monotonic counter.
#[pyfunction]
fn uuid1() -> PyResult<String> {
    Ok(Uuid::now_v1(get_node_id()).to_string())
}

// uuid v3 (ruuid4 v 0.2.0)
// Version 3 UUIDs based on the MD5 hash of some data.
#[pyfunction]
fn uuid3(namespace: &str, name: &str) -> PyResult<String> {
    let ns = resolve_namespace(namespace)?;
    Ok(Uuid::new_v3(&ns, name.as_bytes()).to_string())
}

// uuid v5 (ruuid4 v 0.2.0)
// Version 5 UUIDs based on the SHA1 hash of some data.
#[pyfunction]
fn uuid5(namespace: &str, name: &str) -> PyResult<String> {
    let ns = resolve_namespace(namespace)?;
    Ok(Uuid::new_v5(&ns, name.as_bytes()).to_string())
}

// uuid v6 (ruuid4 v 0.2.0)
// Version 6 UUIDs using a timestamp and monotonic counter.
// UUIDv6 is like v1, but the timestamp bits are rearranged so the UUIDs are lexicographically sortable.
#[pyfunction]
fn uuid6() -> PyResult<String> {
    Ok(Uuid::now_v6(get_node_id()).to_string())
}

// uuid v7 (ruuid4 v 0.2.0)
// Version 7 UUIDs using a Unix timestamp.
#[pyfunction]
fn uuid7() -> PyResult<String> {
    Ok(Uuid::now_v7().to_string())
}

// uuid v8 (ruuid4 v 0.2.0)
// Version 8 UUIDs using user-defined data.
// requires exactly 16 bytes
#[pyfunction]
fn uuid8(data: &[u8]) -> PyResult<String> {
    if data.len() != 16 {
        return Err(PyValueError::new_err("uuid8 requires exactly 16 bytes"));
    } else {
        let mut bytes = [0u8; 16];
        bytes.copy_from_slice(data);
        Ok(Uuid::new_v8(bytes).to_string())
    }
}

// uuid v4 bulk (ruuid4 v 0.2.0)
#[pyfunction]
fn uuid4_bulk(count: usize) -> PyResult<Vec<String>> {
    let mut results = Vec::with_capacity(count);
    for _ in 0..count {
        results.push(Uuid::new_v4().to_string());
    }
    Ok(results)
}

#[pymodule]
fn ruuid4(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(uuid4, m)?)?;
    m.add_function(wrap_pyfunction!(uuid1, m)?)?;
    m.add_function(wrap_pyfunction!(uuid3, m)?)?;
    m.add_function(wrap_pyfunction!(uuid5, m)?)?;
    m.add_function(wrap_pyfunction!(uuid6, m)?)?;
    m.add_function(wrap_pyfunction!(uuid7, m)?)?;
    m.add_function(wrap_pyfunction!(uuid8, m)?)?;
    m.add_function(wrap_pyfunction!(uuid4_bulk, m)?)?;
    Ok(())
}