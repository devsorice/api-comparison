pub struct SqlWhere {
    pub condition: SqlFilter,
}

impl SqlWhere {
    pub fn new(condition: SqlFilter) -> Self {
        SqlWhere { condition }
    }

    pub fn generate_sql(&self) -> (String, Vec<SqlValue>) {
        let (cond_sql, values) = self.condition.generate_sql();
        let sql = format!("WHERE {}", cond_sql);
        (sql, values)
    }
}

pub struct SqlJoin {
    pub join_type: SqlJoinType,
    pub table: SqlTable,
    pub left_field: SqlTableField,
    pub right_field: SqlTableField,
    pub sql_filter: Option<SqlFilter>,
}

impl SqlJoin {
    pub fn new(
        join_type: SqlJoinType,
        table: SqlTable,
        left_field: SqlTableField,
        right_field: SqlTableField,
        sql_filter: Option<SqlFilter>,
    ) -> Self {
        SqlJoin {
            join_type,
            table,
            left_field,
            right_field,
            sql_filter,
        }
    }

    pub fn generate_sql(&self) -> (String, Vec<SqlValue>) {
        let base_sql = format!(
            "{} JOIN {} ON {}.{} = {}.{}",
            self.join_type.to_sql(),
            self.table.name,
            self.left_field.table_name.unwrap_or_default(),
            self.left_field.field_name,
            self.right_field.table_name.unwrap_or_default(),
            self.right_field.field_name
        );
        match &self.sql_filter {
            Some(filter) => {
                let (filter_sql, values) = filter.generate_sql();
                let sql = format!("{} AND {}", base_sql, filter_sql);
                (sql, values)
            }
            None => (base_sql, vec![]),
        }
    }
}

pub struct SqlGroupBy {
    fields: Vec<SqlTableField>,
}

impl SqlGroupBy {
    pub fn new(fields: Vec<SqlTableField>) -> Self {
        SqlGroupBy { fields }
    }

    pub fn generate_sql(&self) -> String {
        let field_list = self
            .fields
            .iter()
            .map(|field| field.full_name())
            .collect::<Vec<_>>()
            .join(", ");
        format!("GROUP BY {}", field_list)
    }
}

pub struct SqlHaving {
    condition: SqlFilter,
}

impl SqlHaving {
    pub fn new(condition: SqlFilter) -> Self {
        SqlHaving { condition }
    }

    pub fn generate_sql(&self) -> (String, Vec<SqlValue>) {
        let (cond_sql, values) = self.condition.generate_sql();
        let sql = format!("HAVING {}", cond_sql);
        (sql, values)
    }
}

pub struct SqlOrderBy {
    orderings: Vec<(SqlTableField, bool)>, // bool indicates ascending (true) or descending (false)
}

impl SqlOrderBy {
    pub fn new(orderings: Vec<(SqlTableField, bool)>) -> Self {
        SqlOrderBy { orderings }
    }

    pub fn generate_sql(&self) -> String {
        let orderings_sql = self
            .orderings
            .iter()
            .map(|(field, asc)| {
                format!(
                    "{} {}",
                    field.full_name(),
                    if *asc { "ASC" } else { "DESC" }
                )
            })
            .collect::<Vec<_>>()
            .join(", ");
        format!("ORDER BY {}", orderings_sql)
    }
}
