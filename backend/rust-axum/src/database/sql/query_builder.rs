use std::collections::HashMap;

use super::{components::*, filters::*, statements::*, tables::*, values::*};

// Define enum to handle both simple and aggregated fields
#[derive(Debug, Clone)]
pub enum ProjectionField {
    Simple(String), // Simple field name
    Aggregated {
        // Aggregated field with optional table and aggregation function
        field: String,
        table: Option<String>,
        aggregation: Option<String>,
    },
}

// Structs for different SQL parameters
#[derive(Debug, Clone)]
pub struct SelectParams {
    pub from_table: SqlTable,
    pub projection: Option<SqlProjection>,
    pub where_clause: Option<SqlWhere>,
    pub join: Option<SqlJoin>, // Simplified for example
    pub groupby: Option<SqlGroupBy>,
    pub having: Option<SqlHaving>,
    pub orderby: Option<SqlOrderBy>,
    pub limit: Option<SqlLimit>,
    pub offset: Option<SqlOffset>,
    pub distinct: Option<SqlDistinct>,
}

#[derive(Debug, Clone)]
pub struct InsertParams {
    pub into_table: String,
    pub entity: HashMap<String, SqlValue>,
}

#[derive(Debug, Clone)]
pub struct UpdateParams {
    pub table: String,
    pub updates: HashMap<String, SqlValue>,
    pub where_clause: Option<SqlWhere>,
}

#[derive(Debug, Clone)]
pub struct DeleteParams {
    pub from_table: String,
    pub where_clause: Option<SqlWhere>,
}

struct SQLQueryBuilder;

impl SQLQueryBuilder {
    pub fn build_filter(
        filter_params: &Filter,
        root_filter: bool,
    ) -> Result<Box<dyn SqlFilter>, SqlError> {
        match filter_params {
            Filter::SimpleFilter {
                field,
                operator,
                value,
            } => {
                let sql_value = match value {
                    Value::Text(t) => SqlValue::Text(t.clone()),
                    Value::Integer(i) => SqlValue::Integer(*i),
                    Value::Float(f) => SqlValue::Float(*f),
                    Value::Boolean(b) => SqlValue::Boolean(*b),
                    Value::None => SqlValue::Null,
                };
                let logical_operator = match operator.as_str() {
                    "gt" => LogicalOperator::Gt,
                    "eq" => LogicalOperator::Eq,
                    _ => {
                        return Err(SqlError {
                            message: format!("Unsupported operator {}", operator),
                        })
                    }
                };
                Ok(Box::new(SimpleFilter {
                    field: field.clone(),
                    operator: logical_operator,
                    value: sql_value,
                }))
            }
            Filter::ConditionalFilter { operator, filters } => {
                let op = match operator.as_str() {
                    "and" => LogicalOperator::And,
                    "or" => LogicalOperator::Or,
                    _ => {
                        return Err(SqlError {
                            message: format!("Unsupported logical operator {}", operator),
                        })
                    }
                };
                let mut constructed_filters: Vec<Box<dyn SqlFilter>> = Vec::new();
                for filter in filters {
                    let constructed_filter = Self::build_filter(filter, false)?;
                    constructed_filters.push(constructed_filter);
                }
                Ok(Box::new(ConditionalFilter {
                    operator: op,
                    filters: constructed_filters,
                }))
            }
            _ => Err(SqlError {
                message: "Invalid filter format".to_string(),
            }),
        }
    }

    pub fn build_select_statement(params: &SelectParams) -> Result<SelectStatement, String> {
        let from_table = SqlTable::new(params.from_table.clone());

        let mut projection = Vec::new();
        for item in &params.projection {
            match item {
                ProjectionField::Field(field) => {
                    projection.push(SqlTableField::new(field.clone(), None));
                }
                ProjectionField::Aggregated {
                    aggregation,
                    field,
                    table,
                } => {
                    let agg_type = SqlAggregationType::from_str(aggregation)
                        .map_err(|_| format!("Unsupported aggregation type: {}", aggregation))?;
                    let table_field = SqlTableField::new(field.clone(), table.clone());
                    projection.push(SqlAggregation::new(agg_type, table_field));
                }
            }
        }

        let where_clause = if let Some(where_params) = &params.where_clause {
            Some(SQLQueryBuilder::build_filter(where_params)?)
        } else {
            None
        };

        let mut joins = Vec::new();
        for join in &params.join {
            let join_type = SqlJoinType::from_str(&join.join_type)
                .map_err(|_| format!("Unsupported join type: {}", join.join_type))?;
            let left_field = SqlTableField::new(join.left_field.clone(), Some(join.table.clone()));
            let right_field =
                SqlTableField::new(join.right_field.clone(), Some(join.table.clone()));
            joins.push(SqlJoin::new(
                join_type,
                from_table.clone(),
                left_field,
                right_field,
                None,
            ));
        }

        let group_by = match &params.groupby {
            Some(fields) => {
                let grouped_fields = fields
                    .iter()
                    .map(|f| SqlTableField::new(f.clone(), None))
                    .collect();
                Some(SqlGroupBy::new(grouped_fields))
            }
            None => None,
        };

        let having_clause = if let Some(having_params) = &params.having {
            Some(SQLQueryBuilder::build_filter(having_params)?)
        } else {
            None
        };

        let order_by = if !params.orderby.is_empty() {
            let orderings = params
                .orderby
                .iter()
                .map(|(field, ascending)| (SqlTableField::new(field.clone(), None), *ascending))
                .collect();
            Some(SqlOrderBy::new(orderings))
        } else {
            None
        };

        let limit = params.limit.map(SqlLimit::new);
        let offset = params.offset.map(SqlOffset::new);
        let distinct = params.distinct.then(|| SqlDistinct::new(true));

        Ok(SelectStatement::new(
            from_table,
            projection,
            where_clause,
            joins,
            group_by,
            having_clause,
            order_by,
            limit,
            offset,
            distinct,
        ))
    }

    pub fn build_insert_statement(params: &InsertParams) -> Result<InsertStatement, String> {
        let into_table = SqlTable::new(params.into_table.clone());

        let fields: Vec<SqlTableField> = params
            .entity
            .keys()
            .map(|field| SqlTableField::new(field.clone(), None))
            .collect();

        let values: Vec<SqlValue> = params
            .entity
            .values()
            .map(|value| match value {
                Value::Str(v) => SqlValue::String(v.clone()),
                Value::Int(v) => SqlValue::Integer(*v),
                Value::Float(v) => SqlValue::Float(*v),
                Value::Bool(v) => SqlValue::Boolean(*v),
                Value::None => SqlValue::Null,
            })
            .collect();

        Ok(InsertStatement::new(into_table, fields, values))
    }

    pub fn build_update_statement(params: &UpdateParams) -> Result<UpdateStatement, String> {
        let table = SqlTable::new(params.table.clone());
        let updates: Vec<SqlUpdatePair> = params
            .updates
            .iter()
            .map(|(field, value)| {
                let field = SqlTableField::new(field.clone(), None);
                let value = match value {
                    Value::Str(v) => SqlValue::String(v.clone()),
                    Value::Int(v) => SqlValue::Integer(*v),
                    Value::Float(v) => SqlValue::Float(*v),
                    Value::Bool(v) => SqlValue::Boolean(*v),
                    Value::None => SqlValue::Null,
                };
                SqlUpdatePair::new(field, value)
            })
            .collect();

        let where_clause = if let Some(where_params) = &params.where_clause {
            match SQLQueryBuilder::build_filter(where_params) {
                Ok(filter) => Some(SqlWhere::new(filter)),
                Err(e) => return Err(e),
            }
        } else {
            None
        };

        Ok(UpdateStatement::new(table, updates, where_clause))
    }
}
