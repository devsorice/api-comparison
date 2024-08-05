use std::collections::HashMap;
use std::fmt;

// Define a custom error type for handling SQL generation errors.
#[derive(Debug, Clone)]
pub struct SqlError {
    pub message: String,
}

impl fmt::Display for SqlError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "SQL Error: {}", self.message)
    }
}
