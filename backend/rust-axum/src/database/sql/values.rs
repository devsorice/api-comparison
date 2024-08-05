#[derive(Debug, Clone)]
pub enum SqlValue {
    Integer(i32),
    Float(f64),
    String(String),
    Boolean(bool),
    Null,
}

impl SqlValue {
    pub fn new(value: impl Into<SqlValue>) -> Self {
        value.into()
    }
}
