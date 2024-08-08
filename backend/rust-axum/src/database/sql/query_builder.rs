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
    pub filters: Vec<HashMap<String, FilterInput>>,
}

#[derive(Debug, Clone)]
// Represents the input for a filter, which can either be a direct value, a sub-filter, or a list of sub-filters.
pub enum FilterInput {
    Value(SqlValue),
    SubFilter(HashMap<String, FilterInput>),
    SubFilters(Vec<HashMap<String, FilterInput>>),
}

// Define enum to handle both simple and aggregated fields
#[derive(Debug, Clone)]
pub enum SqlProjectionField {
    Simple(String), // Simple field name
    Aggregated {
        // Aggregated field with optional table and aggregation function
        field: String,
        table: Option<String>,
        aggregation: Option<String>,
    },
}

impl SqlProjectionField {
    // Create an instance of SqlProjectionField::Simple
    pub fn simple(field: String) -> Self {
        SqlProjectionField::Simple(field)
    }

    // Create an instance of SqlProjectionField::Aggregated
    pub fn aggregated(field: String, table: Option<String>, aggregation: Option<String>) -> Self {
        SqlProjectionField::Aggregated {
            field,
            table,
            aggregation,
        }
    }
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
    pub projection: Option<Vec<SqlProjectionField>>,
    pub where_clause: Option<HashMap<String, FilterInput>>,
    pub join: Option<Vec<HashMap<String, Field>>>,
    pub groupby: Option<Vec<Field>>,
    pub having: Option<HashMap<String, FilterInput>>,
    pub orderby: Option<HashMap<String, i32>>,
    pub limit: Option<u64>,
    pub offset: Option<u64>,
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
    pub where_clause: Option<HashMap<String, FilterInput>>,
}

#[derive(Debug, Clone)]
pub struct DeleteParams {
    pub from_table: String,
    pub where_clause: Option<HashMap<String, FilterInput>>,
}

pub struct SQLQueryBuilder;

impl SQLQueryBuilder {
    // // Parses a field from the given JSON value, which might be a simple string or a dictionary with "field" and optional "table" keys.
    // fn parse_field(value: Option<&serde_json::Value>) -> Result<Field, SqlError> {
    //     match value {
    //         Some(serde_json::Value::String(field)) => Ok(Field::Simple(field.clone())),
    //         Some(serde_json::Value::Object(obj)) => {
    //             let field = obj.get("field").and_then(|f| f.as_str()).ok_or_else(|| {
    //                 SqlError::new("Field key is missing in the object".to_string())
    //             })?;
    //             let table = obj.get("table").and_then(|t| t.as_str());
    //             Ok(Field::WithTableName {
    //                 field: field.to_string(),
    //                 table: table.map(ToString::to_string),
    //             })
    //         }
    //         _ => Err(SqlError::new(
    //             "Invalid or missing field specification".to_string(),
    //         )),
    //     }
    // }
    // pub fn parse_value(value: &serde_json::Value) -> Result<SqlLogicalFilterValue, String> {
    //     match value {
    //         serde_json::Value::String(s) => {
    //             Ok(SqlLogicalFilterValue::Single(SqlValue::String(s.clone())))
    //         }
    //         serde_json::Value::Number(num) => {
    //             if let Some(i) = num.as_i64() {
    //                 Ok(SqlLogicalFilterValue::Single(SqlValue::Integer(i)))
    //             } else if let Some(f) = num.as_f64() {
    //                 Ok(SqlLogicalFilterValue::Single(SqlValue::Float(f)))
    //             } else {
    //                 Err("Invalid number value".to_string())
    //             }
    //         }
    //         serde_json::Value::Bool(b) => Ok(SqlLogicalFilterValue::Single(SqlValue::Boolean(*b))),
    //         serde_json::Value::Null => Ok(SqlLogicalFilterValue::Single(SqlValue::Null)),
    //         serde_json::Value::Array(arr) => {
    //             let mut sql_values = Vec::new();
    //             for item in arr {
    //                 sql_values.push(SQLQueryBuilder::parse_value(item)?.into_single()?);
    //                 // Convert each item and unwrap the single value
    //             }
    //             Ok(SqlLogicalFilterValue::List(sql_values))
    //         }
    //         _ => Err("Unsupported value type for SQL filter".to_string()),
    //     }
    // }

    // /// Builds an SQL filter from a structured input.
    // pub fn build_filter(
    //     filter_params: &HashMap<String, FilterInput>,
    // ) -> Result<Box<dyn SqlFilterTrait>, SqlError> {
    //     if let Some(FilterInput::SubFilters(filters)) = filter_params.get("filters") {
    //         let operator = match filter_params.get("operator").and_then(|op| match op {
    //             FilterInput::Value(SqlValue::String(s)) => LogicalOperator::from_str(s),
    //             _ => None,
    //         }) {
    //             Some(op) => op,
    //             None => {
    //                 return Err(SqlError {
    //                     message: format!("Invalid or missing operator for conditional filters"),
    //                 })
    //             }
    //         };

    //         let mut built_filters = Vec::new();
    //         for filter in filters {
    //             built_filters.push(SQLQueryBuilder::build_filter(filter)?);
    //         }
    //         return Ok(Box::new(SqlConditionalFilter::new(operator, built_filters)));
    //     }

    //     if let (Some(field), Some(op), Some(value)) = (
    //         filter_params.get("field").and_then(|f| {
    //             if let FilterInput::Value(SqlValue::String(s)) = f {
    //                 Some(s)
    //             } else {
    //                 None
    //             }
    //         }),
    //         filter_params.get("operator").and_then(|o| {
    //             if let FilterInput::Value(SqlValue::String(s)) = o {
    //                 LogicalOperator::from_str(s)
    //             } else {
    //                 None
    //             }
    //         }),
    //         filter_params.get("value").and_then(|v| {
    //             if let FilterInput::Value(val) = v {
    //                 Some(val.clone())
    //             } else {
    //                 None
    //             }
    //         }),
    //     ) {
    //         let field = SqlTableField::new(field, None); // Adjust if needed to include potential table names
    //         return Ok(Box::new(SqlLogicalFilter::new(
    //             field,
    //             op,
    //             SqlLogicalFilterValue::Single(value),
    //         )));
    //     }
    //     Err(SqlError {
    //         message: format!("Invalid filter format"),
    //     })
    // }
    pub fn build_select_statement(params: &SelectParams) -> Result<SelectStatement, SqlError> {
        let from_table = SqlTable::new(&params.from_table);

        let projection: Option<SqlProjection> = None;

        let where_clause: Option<SqlWhere> = None;

        let joins: Option<Vec<SqlJoin>> = None;

        let group_by: Option<SqlGroupBy> = None;

        let having: Option<SqlHaving> = None;

        let order_by: Option<SqlOrderBy> = None;

        let limit: Option<SqlLimit> = params.limit.map(SqlLimit::new);
        let offset: Option<SqlOffset> = params.offset.map(SqlOffset::new);
        let distinct: Option<SqlDistinct> =
            Some(SqlDistinct::new(params.distinct.unwrap_or(false)));

        Ok(SelectStatement::new(
            from_table,
            projection,
            where_clause,
            joins,    // Ensure it's wrapped in Some even if it's an empty Vec
            group_by, // Same as above
            having,
            order_by, // Same as above
            limit,
            offset,
            distinct,
        ))
    }

    // pub fn build_insert_statement(params: &InsertParams) -> Result<InsertStatement, SqlError> {
    //     let into_table = SqlTable::new(&params.into_table);
    //     let fields: Vec<SqlTableField> = params
    //         .entity
    //         .keys()
    //         .map(|field| SqlTableField::new(&field, None))
    //         .collect();
    //     let values: Vec<SqlValue> = params.entity.values().cloned().collect();
    //     Ok(InsertStatement::new(into_table, fields, values))
    // }

    // pub fn build_update_statement(params: &UpdateParams) -> Result<UpdateStatement, SqlError> {
    //     let table = SqlTable::new(&params.table);
    //     let updates: Vec<SqlUpdatePair> = params
    //         .updates
    //         .iter()
    //         .map(|(field, value)| {
    //             let field = SqlTableField::new(&field, None);
    //             let value = value.clone();
    //             SqlUpdatePair::new(field, value)
    //         })
    //         .collect();

    //     let where_clause = if let Some(where_params) = &params.where_clause {
    //         let filter = Self::build_filter(where_params.get("filter").unwrap())?;
    //         Some(SqlWhere::new(filter))
    //     } else {
    //         None
    //     };

    //     Ok(UpdateStatement::new(table, updates, where_clause))
    // }

    // pub fn build_delete_statement(params: &DeleteParams) -> Result<DeleteStatement, SqlError> {
    //     let from_table = SqlTable::new(&params.from_table);
    //     let where_clause = if let Some(where_params) = &params.where_clause {
    //         let filter = Self::build_filter(where_params.get("filter").unwrap())?;
    //         Some(SqlWhere::new(filter))
    //     } else {
    //         None
    //     };
    //     Ok(DeleteStatement::new(from_table, where_clause))
    // }
}
