pub struct SqlTable {
    pub name: String,
}

impl SqlTable {
    pub fn new(name: &str) -> Self {
        SqlTable {
            name: name.to_string(),
        }
    }
}

pub struct SqlTableField {
    pub field_name: String,
    pub table_name: Option<String>,
}

impl SqlTableField {
    pub fn new(field_name: &str, table_name: Option<&str>) -> Self {
        SqlTableField {
            field_name: field_name.to_string(),
            table_name: table_name.map(String::from),
        }
    }

    pub fn full_name(&self) -> String {
        match &self.table_name {
            Some(name) => format!("`{}`.`{}`", name, self.field_name),
            None => self.field_name.clone(),
        }
    }
}
