use std::collections::HashMap;

use super::{components::*, enums::*, errors::*, filters::*, statements::*, tables::*, values::*};

#[derive(Debug, Clone)]
pub struct SimpleFilter {
    pub field: String,
    pub table: String,
    pub operator: String,
    pub value: SqlValue,
}

#[derive(Debug, Clone)]
pub struct ConditionalFilter {
    pub operator: String,
    pub filters: Vec<Filter>,
}

#[derive(Debug, Clone)]
pub enum Filter {
    Simple(SimpleFilter),
    Conditional(ConditionalFilter),
    Map(HashMap<String, Filter>),
}

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

#[derive(Debug, Clone)]
pub enum Field {
    Simple(String), // Simple field name
    WithTableName {
        // Aggregated field with optional table and aggregation function
        field: String,
        table: Option<String>,
    },
}

// Structs for different SQL parameters
#[derive(Debug, Clone)]
pub struct SelectParams {
    pub from_table: String,
    pub projection: Option<Vec<ProjectionField>>,
    pub where_clause: Option<HashMap<String, Filter>>,
    pub join: Option<Vec<HashMap<String, String>>>,
    pub groupby: Option<Vec<Field>>,
    pub having: Option<HashMap<String, Filter>>,
    pub orderby: Option<HashMap<String, i32>>,
    pub limit: Option<i32>,
    pub offset: Option<i32>,
    pub distinct: Option<bool>,
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
    pub where_clause: Option<HashMap<String, Filter>>,
}

#[derive(Debug, Clone)]
pub struct DeleteParams {
    pub from_table: String,
    pub where_clause: Option<HashMap<String, Filter>>,
}

pub struct SQLQueryBuilder;

impl SQLQueryBuilder {
    pub fn build_filter(filter_params: &Filter) -> Result<SqlFilter, SqlError> {
        match filter_params {
            Filter::Simple(simple) => {
                let sql_value = match &simple.value {
                    SqlValue::Str(v) => SqlValue::Str(v.clone()),
                    SqlValue::Int(v) => SqlValue::Int(*v),
                    SqlValue::Float(v) => SqlValue::Float(*v),
                    SqlValue::Bool(v) => SqlValue::Bool(*v),
                    SqlValue::None => SqlValue::None,
                };
                let logical_operator = match simple.operator.as_str() {
                    "gt" => LogicalOperator::Gt,
                    "eq" => LogicalOperator::Eq,
                    _ => {
                        return Err(SqlError {
                            message: format!("Unsupported operator {}", simple.operator),
                        })
                    }
                };
                Ok(SqlFilter::Logical(SqlLogicalFilter {
                    field: SqlTableField::new(simple, None);,
                    operator: logical_operator,
                    value: sql_value,
                }))
            }
            Filter::Conditional(conditional) => {
                let op = match conditional.operator.as_str() {
                    "and" => LogicalOperator::And,
                    "or" => LogicalOperator::Or,
                    _ => {
                        return Err(SqlError {
                            message: format!(
                                "Unsupported logical operator {}",
                                conditional.operator
                            ),
                        })
                    }
                };
                let mut constructed_filters: Vec<SqlFilter> = Vec::new();
                for filter in &conditional.filters {
                    let constructed_filter = Self::build_filter(filter)?;
                    constructed_filters.push(constructed_filter);
                }
                Ok(SqlFilter::Conditional(SqlConditionalFilter {
                    operator: op,
                    filters: constructed_filters,
                }))
            }
            Filter::Map(_) => Err(SqlError {
                message: "Invalid filter format".to_string(),
            }),
        }
    }

    pub fn build_select_statement(params: &SelectParams) -> Result<SelectStatement, SqlError> {
        let from_table = SqlTable::new(params.from_table.clone());

        let projection = if let Some(projection_fields) = &params.projection {
            let mut proj = Vec::new();
            for item in projection_fields {
                match item {
                    ProjectionField::Simple(field) => {
                        proj.push(SqlProjectionField::new(field.clone(), None));
                    }
                    ProjectionField::Aggregated {
                        field,
                        table,
                        aggregation,
                    } => {
                        let agg_type = match aggregation.as_deref() {
                            Some("SUM") => SqlAggregationType::Sum,
                            Some("AVG") => SqlAggregationType::Avg,
                            _ => {
                                return Err(SqlError {
                                    message: format!(
                                        "Unsupported aggregation type: {:?}",
                                        aggregation
                                    ),
                                })
                            }
                        };
                        let table_field = SqlTableField::new(field.clone(), table.clone());
                        proj.push(SqlAggregation::new(agg_type, table_field));
                    }
                }
            }
            proj
        } else {
            Vec::new()
        };

        let where_clause = if let Some(where_params) = &params.where_clause {
            let filter = Self::build_filter(where_params.get("filter").unwrap())?;
            Some(SqlWhere::new(filter))
        } else {
            None
        };

        let joins = if let Some(join_params) = &params.join {
            let mut joins_vec = Vec::new();
            for join in join_params {
                let join_type = match join.get("type").map(|s| s.as_str()) {
                    Some("INNER") => SqlJoinType::Inner,
                    Some("LEFT") => SqlJoinType::Left,
                    _ => {
                        return Err(SqlError {
                            message: "Unsupported join type".to_string(),
                        })
                    }
                };
                let left_field = SqlTableField::new(join.get("left_field").unwrap().clone(), None);
                let right_field =
                    SqlTableField::new(join.get("right_field").unwrap().clone(), None);
                joins_vec.push(SqlJoin::new(
                    join_type,
                    from_table.clone(),
                    left_field,
                    right_field,
                    None,
                ));
            }
            joins_vec
        } else {
            Vec::new()
        };

        let group_by = if let Some(groupby_params) = &params.groupby {
            let mut grouped_fields = Vec::new();
            for field in groupby_params {
                match field {
                    Field::Simple(f) => grouped_fields.push(SqlTableField::new(f.clone(), None)),
                    Field::WithTableName { field, table } => {
                        grouped_fields.push(SqlTableField::new(field.clone(), table.clone()))
                    }
                }
            }
            Some(SqlGroupBy::new(grouped_fields))
        } else {
            None
        };

        let having_clause = if let Some(having_params) = &params.having {
            let filter = Self::build_filter(having_params.get("filter").unwrap())?;
            Some(SqlHaving::new(filter))
        } else {
            None
        };

        let order_by = if let Some(orderby_params) = &params.orderby {
            let orderings = orderby_params
                .iter()
                .map(|(field, ascending)| {
                    (SqlTableField::new(field.clone(), None), *ascending != 0)
                })
                .collect();
            Some(SqlOrderBy::new(orderings))
        } else {
            None
        };

        let limit = params.limit.map(SqlLimit::new);
        let offset = params.offset.map(SqlOffset::new);
        let distinct = params.distinct.unwrap_or(false);

        Ok(SelectStatement::new(
            from_table,
            SqlProjection::new(projection),
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

    pub fn build_insert_statement(params: &InsertParams) -> Result<InsertStatement, SqlError> {
        let into_table = SqlTable::new(params.into_table.clone());
        let fields: Vec<SqlTableField> = params
            .entity
            .keys()
            .map(|field| SqlTableField::new(field.clone(), None))
            .collect();
        let values: Vec<SqlValue> = params.entity.values().cloned().collect();
        Ok(InsertStatement::new(into_table, fields, values))
    }

    pub fn build_update_statement(params: &UpdateParams) -> Result<UpdateStatement, SqlError> {
        let table = SqlTable::new(params.table.clone());
        let updates: Vec<SqlUpdatePair> = params
            .updates
            .iter()
            .map(|(field, value)| {
                let field = SqlTableField::new(field.clone(), None);
                let value = value.clone();
                SqlUpdatePair::new(field, value)
            })
            .collect();

        let where_clause = if let Some(where_params) = &params.where_clause {
            let filter = Self::build_filter(where_params.get("filter").unwrap())?;
            Some(SqlWhere::new(filter))
        } else {
            None
        };

        Ok(UpdateStatement::new(table, updates, where_clause))
    }

    pub fn build_delete_statement(params: &DeleteParams) -> Result<DeleteStatement, SqlError> {
        let from_table = SqlTable::new(params.from_table.clone());
        let where_clause = if let Some(where_params) = &params.where_clause {
            let filter = Self::build_filter(where_params.get("filter").unwrap())?;
            Some(SqlWhere::new(filter))
        } else {
            None
        };
        Ok(DeleteStatement::new(from_table, where_clause))
    }
}
