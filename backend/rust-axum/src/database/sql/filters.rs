use super::{enums::LogicalOperator, tables::SqlTableField, values::SqlValue};

// Define a trait for SQL filtering functionality
pub trait SqlFilterTrait {
    fn generate_sql(&self) -> (String, Vec<SqlValue>);
}

pub enum SqlFilter {
    Logical(SqlLogicalFilter),
    Conditional(SqlConditionalFilter),
}
impl SqlFilter {
    pub fn generate_sql(&self) -> (String, Vec<SqlValue>) {
        match self {
            SqlFilter::Logical(logical_filter) => logical_filter.generate_sql(),
            SqlFilter::Conditional(conditional_filter) => conditional_filter.generate_sql(),
        }
    }
}

pub enum SqlLogicalFilterValue {
    Single(SqlValue),
    List(Vec<SqlValue>),
}

impl SqlLogicalFilterValue {
    /// Helper to unwrap a Single SqlValue from a SqlLogicalFilterValue
    pub fn into_single(self) -> Result<SqlValue, String> {
        match self {
            SqlLogicalFilterValue::Single(val) => Ok(val),
            _ => Err("Expected a single value".to_string()),
        }
    }
}

pub struct SqlLogicalFilter {
    pub field: SqlTableField,
    pub operator: LogicalOperator,
    pub value: SqlLogicalFilterValue,
}

impl SqlLogicalFilter {
    pub fn new(
        field: SqlTableField,
        operator: LogicalOperator,
        value: SqlLogicalFilterValue,
    ) -> Self {
        SqlLogicalFilter {
            field,
            operator,
            value,
        }
    }
    pub fn generate_sql(&self) -> (String, Vec<SqlValue>) {
        let field = match &self.field.table_name {
            Some(table_name) => format!("{}.{}", table_name, self.field.field_name),
            None => self.field.field_name.clone(),
        };
        let operator = format!("{}", self.operator.to_sql());

        match (&self.operator, &self.value) {
            (LogicalOperator::In | LogicalOperator::NotIn, SqlLogicalFilterValue::List(values)) => {
                let placeholders = values
                    .iter()
                    .map(|_| "?".to_string())
                    .collect::<Vec<String>>()
                    .join(",");
                let sql = format!("{} {} ({})", field, operator, placeholders);
                (sql, values.clone())
            }
            (
                LogicalOperator::Between | LogicalOperator::NotBetween,
                SqlLogicalFilterValue::List(values),
            ) if values.len() == 2 => {
                let sql = format!("{} {} ? AND ?", field, operator);
                (sql, vec![values[0].clone(), values[1].clone()])
            }
            (LogicalOperator::IsNull | LogicalOperator::IsNotNull, _) => {
                let sql = format!("{} {}", field, operator);
                (sql, vec![])
            }
            (
                LogicalOperator::Contains
                | LogicalOperator::NotContains
                | LogicalOperator::ContainsCaseSensitive
                | LogicalOperator::NotContainsCaseSensitive,
                SqlLogicalFilterValue::Single(value),
            ) => {
                let sql = format!("{} {} ?", field, operator);
                let param = match value {
                    SqlValue::String(s) => SqlValue::String(format!("%{}%", s)),
                    _ => panic!("Expected a String value for LIKE operator"),
                };
                (sql, vec![param])
            }
            (
                LogicalOperator::StartsWith
                | LogicalOperator::NotStartsWith
                | LogicalOperator::StartsWithCaseSensitive
                | LogicalOperator::NotStartsWithCaseSensitive,
                SqlLogicalFilterValue::Single(value),
            ) => {
                let sql = format!("{} {} ?", field, operator);
                let param = match value {
                    SqlValue::String(s) => SqlValue::String(format!("{}%", s)),
                    _ => panic!("Expected a String value for LIKE operator"),
                };
                (sql, vec![param])
            }
            (
                LogicalOperator::EndsWith
                | LogicalOperator::NotEndsWith
                | LogicalOperator::EndsWithCaseSensitive
                | LogicalOperator::NotEndsWithCaseSensitive,
                SqlLogicalFilterValue::Single(value),
            ) => {
                let sql = format!("{} {} ?", field, operator);
                let param = match value {
                    SqlValue::String(s) => SqlValue::String(format!("%{}", s)),
                    _ => panic!("Expected a String value for LIKE operator"),
                };
                (sql, vec![param])
            }
            (_, SqlLogicalFilterValue::Single(value)) => {
                let sql = format!("{} {} ?", field, operator);
                (sql, vec![value.clone()])
            }
            _ => panic!(
                "Operator {} not implemented or invalid value type",
                operator
            ),
        }
    }
}

pub struct SqlConditionalFilter {
    pub operator: LogicalOperator,
    pub filters: Vec<SqlFilter>,
}

impl SqlConditionalFilter {
    pub fn new(operator: LogicalOperator, filters: Vec<SqlFilter>) -> Self {
        SqlConditionalFilter { operator, filters }
    }

    pub fn generate_sql(&self) -> (String, Vec<SqlValue>) {
        let mut sql_parts = Vec::new();
        let mut values = Vec::new();

        for filter in &self.filters {
            let (sql, vals) = match filter {
                SqlFilter::Logical(logical) => logical.generate_sql(),
                SqlFilter::Conditional(conditional) => conditional.generate_sql(),
            };
            sql_parts.push(format!("({})", sql));
            values.extend(vals);
        }

        let joined_sql = sql_parts.join(format!(" {} ", self.operator.to_sql()).as_str());
        (joined_sql, values)
    }
}
