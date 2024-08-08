use sqlx::{mysql::MySqlArguments, postgres::PgArguments, Arguments};

use super::{components::*, converters::*, enums::DatabaseType, tables::*, values::*};

pub trait SqlStatement {
    fn generate_query(&self) -> (String, Vec<SqlValue>);
}

pub enum DatabaseArguments {
    Postgres(PgArguments),
    MySql(MySqlArguments),
}
impl DatabaseArguments {
    pub fn as_postgres(self) -> Option<PgArguments> {
        if let DatabaseArguments::Postgres(args) = self {
            Some(args)
        } else {
            None
        }
    }

    pub fn as_mysql(self) -> Option<MySqlArguments> {
        if let DatabaseArguments::MySql(args) = self {
            Some(args)
        } else {
            None
        }
    }
}

pub struct SelectStatement {
    from_table: SqlTable,
    projection: Option<SqlProjection>,
    where_clause: Option<SqlWhere>,
    joins: Option<Vec<SqlJoin>>,
    group_by: Option<SqlGroupBy>,
    having: Option<SqlHaving>,
    order_by: Option<SqlOrderBy>,
    limit: Option<SqlLimit>,
    offset: Option<SqlOffset>,
    distinct: Option<SqlDistinct>,
}

impl SelectStatement {
    pub fn new(
        from_table: SqlTable,
        projection: Option<SqlProjection>,
        where_clause: Option<SqlWhere>,
        joins: Option<Vec<SqlJoin>>,
        group_by: Option<SqlGroupBy>,
        having: Option<SqlHaving>,
        order_by: Option<SqlOrderBy>,
        limit: Option<SqlLimit>,
        offset: Option<SqlOffset>,
        distinct: Option<SqlDistinct>,
    ) -> Self {
        SelectStatement {
            from_table,
            projection,
            where_clause,
            joins,
            group_by,
            having,
            order_by,
            limit,
            offset,
            distinct,
        }
    }

    pub fn generate_query(&self, db_type: DatabaseType) -> (String, DatabaseArguments) {
        let mut query = String::from("SELECT ");
        let mut params = Vec::new();
        let quote_char = match db_type {
            DatabaseType::MySQL => '`',
            DatabaseType::PostgreSQL => '"',
        };

        if let Some(distinct) = &self.distinct {
            query.push_str(&distinct.generate_sql());
        }

        match &self.projection {
            Some(proj) => {
                let proj_sql = proj.generate_sql(); // Assuming no values needed for projection
                query.push_str(&proj_sql);
            }
            None => query.push('*'),
        }

        query.push_str(&format!(
            " FROM {}{}{}",
            quote_char, self.from_table.name, quote_char
        ));

        // Handle joins
        if let Some(joins) = &self.joins {
            for join in joins {
                let (join_sql, join_values) = join.generate_sql();
                query.push_str(&format!(" {}", join_sql));
                params.extend(join_values);
            }
        }

        if let Some(where_clause) = &self.where_clause {
            let (where_sql, where_values) = where_clause.generate_sql();
            query.push_str(&format!(" {}", where_sql));
            params.extend(where_values);
        }

        if let Some(group_by) = &self.group_by {
            query.push_str(&format!(" {}", group_by.generate_sql()));
        }

        if let Some(having) = &self.having {
            let (having_sql, having_values) = having.generate_sql();
            query.push_str(&format!(" {}", having_sql));
            params.extend(having_values);
        }

        if let Some(order_by) = &self.order_by {
            query.push_str(&format!(" {}", order_by.generate_sql()));
        }

        if let Some(limit) = &self.limit {
            query.push_str(&format!(" {}", limit.generate_sql()));
        }

        if let Some(offset) = &self.offset {
            query.push_str(&format!(" {}", offset.generate_sql()));
        }

        let args = match db_type {
            DatabaseType::MySQL => DatabaseArguments::MySql(MySqlArguments::convert(params)),
            DatabaseType::PostgreSQL => DatabaseArguments::Postgres(PgArguments::convert(params)),
        };

        (query, args)
    }
}

pub struct InsertStatement {
    into_table: SqlTable,
    fields: Vec<SqlTableField>,
    values: Vec<SqlValue>,
}

impl InsertStatement {
    pub fn new(into_table: SqlTable, fields: Vec<SqlTableField>, values: Vec<SqlValue>) -> Self {
        InsertStatement {
            into_table,
            fields,
            values,
        }
    }

    pub fn generate_query(&self) -> (String, Vec<SqlValue>) {
        let field_names = self
            .fields
            .iter()
            .map(|f| f.full_name())
            .collect::<Vec<_>>()
            .join(", ");
        let placeholders = self
            .values
            .iter()
            .map(|_| "?")
            .collect::<Vec<_>>()
            .join(", ");
        let query = format!(
            "INSERT INTO `{}` ({}) VALUES ({})",
            self.into_table.name, field_names, placeholders
        );

        (query, self.values.clone())
    }
}

pub struct UpdateStatement {
    table: SqlTable,
    updates: Vec<(SqlTableField, SqlValue)>,
    where_clause: Option<SqlWhere>,
}

impl UpdateStatement {
    pub fn new(
        table: SqlTable,
        updates: Vec<(SqlTableField, SqlValue)>,
        where_clause: Option<SqlWhere>,
    ) -> Self {
        UpdateStatement {
            table,
            updates,
            where_clause,
        }
    }

    pub fn generate_query(&self) -> (String, Vec<SqlValue>) {
        let update_parts = self
            .updates
            .iter()
            .map(|(field, _)| format!("{} = ?", field.full_name()))
            .collect::<Vec<_>>()
            .join(", ");
        let mut query = format!("UPDATE `{}` SET {}", self.table.name, update_parts);
        let mut values = self
            .updates
            .iter()
            .map(|(_, value)| value.clone())
            .collect::<Vec<_>>();

        if let Some(where_clause) = &self.where_clause {
            let (where_sql, where_values) = where_clause.generate_sql();
            query.push_str(&format!(" {}", where_sql));
            values.extend(where_values);
        }

        (query, values)
    }
}

pub struct DeleteStatement {
    from_table: SqlTable,
    where_clause: Option<SqlWhere>,
}

impl DeleteStatement {
    pub fn new(from_table: SqlTable, where_clause: Option<SqlWhere>) -> Self {
        DeleteStatement {
            from_table,
            where_clause,
        }
    }

    pub fn generate_query(&self) -> (String, Vec<SqlValue>) {
        let mut query = format!("DELETE FROM `{}`", self.from_table.name);
        let mut values = Vec::new();

        if let Some(where_clause) = &self.where_clause {
            let (where_sql, where_values) = where_clause.generate_sql();
            query.push_str(&format!(" {}", where_sql));
            values.extend(where_values);
        }

        (query, values)
    }
}
