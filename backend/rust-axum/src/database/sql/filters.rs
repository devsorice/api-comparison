pub enum SqlFilter {
    Logical(SqlLogicalFilter),
    Conditional(SqlConditionalFilter),
}

pub struct SqlLogicalFilter {
    pub field: SqlTableField,
    pub operator: LogicalOperator,
    pub values: Vec<SqlValue>,
}

impl SqlLogicalFilter {
    pub fn new(field: SqlTableField, operator: LogicalOperator, values: Vec<SqlValue>) -> Self {
        SqlLogicalFilter {
            field,
            operator,
            values,
        }
    }

    pub fn generate_sql(&self) -> (String, Vec<SqlValue>) {
        let operator_sql = match self.operator {
            LogicalOperator::Equal => "=",
            LogicalOperator::NotEqual => "!=",
            LogicalOperator::LessThan => "<",
            // Other operators...
            _ => panic!("Unsupported operator"),
        };
        let field_name = self.field.full_name();
        let sql = format!("{} {} ?", field_name, operator_sql);
        (sql, self.values.clone())
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
