use std::collections::HashMap;

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
pub enum SqlAggregationType {
    Sum,
    Avg,
    Max,
    Min,
    Count,
    Distinct,
}

impl SqlAggregationType {
    pub fn from_str(val: &str) -> Option<Self> {
        match val.to_uppercase().as_str() {
            "SUM" => Some(SqlAggregationType::Sum),
            "AVG" => Some(SqlAggregationType::Avg),
            "MAX" => Some(SqlAggregationType::Max),
            "MIN" => Some(SqlAggregationType::Min),
            "COUNT" => Some(SqlAggregationType::Count),
            "DISTINCT" => Some(SqlAggregationType::Distinct),
            _ => None,
        }
    }
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
pub enum SqlJoinType {
    InnerJoin,
    LeftJoin,
    RightJoin,
    FullJoin,
    CrossJoin,
    NaturalJoin,
    LeftOuterJoin,
    RightOuterJoin,
    FullOuterJoin,
}

impl SqlJoinType {
    pub fn from_str(val: &str) -> Option<Self> {
        match val.to_uppercase().as_str() {
            "INNER JOIN" => Some(SqlJoinType::InnerJoin),
            "LEFT JOIN" => Some(SqlJoinType::LeftJoin),
            "RIGHT JOIN" => Some(SqlJoinType::RightJoin),
            "FULL JOIN" => Some(SqlJoinType::FullJoin),
            "CROSS JOIN" => Some(SqlJoinType::CrossJoin),
            "NATURAL JOIN" => Some(SqlJoinType::NaturalJoin),
            "LEFT OUTER JOIN" => Some(SqlJoinType::LeftOuterJoin),
            "RIGHT OUTER JOIN" => Some(SqlJoinType::RightOuterJoin),
            "FULL OUTER JOIN" => Some(SqlJoinType::FullOuterJoin),
            _ => None,
        }
    }
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
pub enum LogicalOperator {
    Equal,
    NotEqual,
    LessThan,
    GreaterThan,
    LessThanOrEqual,
    GreaterThanOrEqual,
    In,
    NotIn,
    IncludesAll,
    NotIncludesAll,
    Contains,
    NotContains,
    ContainsCaseSensitive,
    NotContainsCaseSensitive,
    Between,
    NotBetween,
    IsNull,
    IsNotNull,
    StartsWith,
    NotStartsWith,
    StartsWithCaseSensitive,
    NotStartsWithCaseSensitive,
    EndsWith,
    NotEndsWith,
    EndsWithCaseSensitive,
    NotEndsWithCaseSensitive,
    Or,
    And,
}

impl LogicalOperator {
    pub fn from_str(val: &str) -> Option<Self> {
        match val.to_lowercase().as_str() {
            "eq" => Some(LogicalOperator::Equal),
            "ne" => Some(LogicalOperator::NotEqual),
            "lt" => Some(LogicalOperator::LessThan),
            "gt" => Some(LogicalOperator::GreaterThan),
            "lte" => Some(LogicalOperator::LessThanOrEqual),
            "gte" => Some(LogicalOperator::GreaterThanOrEqual),
            "in" => Some(LogicalOperator::In),
            "nin" => Some(LogicalOperator::NotIn),
            "ina" => Some(LogicalOperator::IncludesAll),
            "nina" => Some(LogicalOperator::NotIncludesAll),
            "contains" => Some(LogicalOperator::Contains),
            "ncontains" => Some(LogicalOperator::NotContains),
            "containss" => Some(LogicalOperator::ContainsCaseSensitive),
            "ncontainss" => Some(LogicalOperator::NotContainsCaseSensitive),
            "between" => Some(LogicalOperator::Between),
            "nbetween" => Some(LogicalOperator::NotBetween),
            "null" => Some(LogicalOperator::IsNull),
            "nnull" => Some(LogicalOperator::IsNotNull),
            "startswith" => Some(LogicalOperator::StartsWith),
            "nstartswith" => Some(LogicalOperator::NotStartsWith),
            "startswiths" => Some(LogicalOperator::StartsWithCaseSensitive),
            "nstartswiths" => Some(LogicalOperator::NotStartsWithCaseSensitive),
            "endswith" => Some(LogicalOperator::EndsWith),
            "nendswith" => Some(LogicalOperator::NotEndsWith),
            "endswiths" => Some(LogicalOperator::EndsWithCaseSensitive),
            "nendswiths" => Some(LogicalOperator::NotEndsWithCaseSensitive),
            "or" => Some(LogicalOperator::Or),
            "and" => Some(LogicalOperator::And),
            _ => None,
        }
    }
}

#[derive(Debug, Clone)]
pub struct SqlValue {
    pub value: Option<String>,
}

impl SqlValue {
    pub fn new(value: Option<&str>) -> Self {
        SqlValue {
            value: value.map(String::from),
        }
    }
}

#[derive(Debug, Clone)]
pub struct SqlTable {
    pub name: String,
}

impl SqlTable {
    pub fn new(name: &str) -> Self {
        SqlTable {
            name: String::from(name),
        }
    }
}

#[derive(Debug, Clone)]
pub struct SqlTableField {
    pub field_name: String,
    pub table_name: Option<String>,
}

impl SqlTableField {
    pub fn new(field_name: &str, table_name: Option<&str>) -> Self {
        SqlTableField {
            field_name: String::from(field_name),
            table_name: table_name.map(String::from),
        }
    }
}

#[derive(Debug, Clone)]
pub struct SqlAggregation {
    pub aggregation: SqlAggregationType,
    pub field: SqlTableField,
}

impl SqlAggregation {
    pub fn new(aggregation: SqlAggregationType, field: SqlTableField) -> Self {
        SqlAggregation { aggregation, field }
    }
}

#[derive(Debug, Clone)]
pub struct SqlLogicalFilter {
    pub field: SqlTableField,
    pub operator: LogicalOperator,
    pub value: SqlValue,
}

impl SqlLogicalFilter {
    pub fn new(field: SqlTableField, operator: LogicalOperator, value: SqlValue) -> Self {
        if operator == LogicalOperator::Or || operator == LogicalOperator::And {
            panic!("Operator 'or' or 'and' is not valid for LogicalFilter.");
        }
        SqlLogicalFilter {
            field,
            operator,
            value,
        }
    }

    pub fn generate_sql(&self) -> (String, Vec<String>) {
        let operator_map = [
            (LogicalOperator::Equal, "="),
            (LogicalOperator::NotEqual, "!="),
            (LogicalOperator::LessThan, "<"),
            (LogicalOperator::GreaterThan, ">"),
            (LogicalOperator::LessThanOrEqual, "<="),
            (LogicalOperator::GreaterThanOrEqual, ">="),
            (LogicalOperator::In, "IN"),
            (LogicalOperator::NotIn, "NOT IN"),
            (LogicalOperator::Contains, "LIKE"),
            (LogicalOperator::NotContains, "NOT LIKE"),
            (LogicalOperator::Between, "BETWEEN"),
            (LogicalOperator::NotBetween, "NOT BETWEEN"),
            (LogicalOperator::IsNull, "IS NULL"),
            (LogicalOperator::IsNotNull, "IS NOT NULL"),
        ]
        .iter()
        .cloned()
        .collect::<HashMap<_, _>>();

        let field = format!(
            "{}{}",
            self.field
                .table_name
                .clone()
                .map_or("".to_string(), |tn| format!("{}.", tn)),
            self.field.field_name
        );
        let operator = operator_map.get(&self.operator).unwrap();

        if self.operator == LogicalOperator::In || self.operator == LogicalOperator::NotIn {
            let placeholders = self
                .value
                .value
                .as_ref()
                .unwrap()
                .split(',')
                .map(|_| "?")
                .collect::<Vec<_>>()
                .join(", ");
            return (
                format!("{} {} ({})", field, operator, placeholders),
                self.value
                    .value
                    .as_ref()
                    .unwrap()
                    .split(',')
                    .map(|s| s.to_string())
                    .collect(),
            );
        } else if self.operator == LogicalOperator::Between
            || self.operator == LogicalOperator::NotBetween
        {
            return (
                format!("{} {} ? AND ?", field, operator),
                self.value
                    .value
                    .as_ref()
                    .unwrap()
                    .split(',')
                    .map(|s| s.to_string())
                    .collect(),
            );
        } else if self.operator == LogicalOperator::IsNull
            || self.operator == LogicalOperator::IsNotNull
        {
            return (format!("{} {}", field, operator), vec![]);
        } else {
            return (
                format!("{} {} ?", field, operator),
                vec![self.value.value.clone().unwrap()],
            );
        }
    }
}

#[derive(Debug, Clone)]
pub struct SqlConditionalFilter {
    pub operator: LogicalOperator,
    pub filters: Vec<SqlLogicalFilter>,
}

impl SqlConditionalFilter {
    pub fn new(operator: LogicalOperator, filters: Vec<SqlLogicalFilter>) -> Self {
        if operator != LogicalOperator::Or && operator != LogicalOperator::And {
            panic!("Operator must be 'or' or 'and' for SqlConditionalFilter.");
        }
        SqlConditionalFilter { operator, filters }
    }

    pub fn generate_sql(&self) -> (String, Vec<String>) {
        let mut sql_parts = vec![];
        let mut params = vec![];

        for f in &self.filters {
            let (sql, p) = f.generate_sql();
            sql_parts.push(format!("({})", sql));
            params.extend(p);
        }

        return (
            sql_parts.join(&format!(" {} ", self.operator.to_string().to_uppercase())),
            params,
        );
    }
}

pub enum SqlFilter {
    Logical(SqlLogicalFilter),
    Conditional(SqlConditionalFilter),
}

#[derive(Debug, Clone)]
pub struct SqlWhere {
    pub condition: SqlFilter,
}

impl SqlWhere {
    pub fn new(condition: SqlFilter) -> Self {
        SqlWhere { condition }
    }

    pub fn generate_sql(&self) -> (String, Vec<String>) {
        match &self.condition {
            SqlFilter::Logical(f) => {
                let (sql, params) = f.generate_sql();
                return (format!("WHERE {}", sql), params);
            }
            SqlFilter::Conditional(f) => {
                let (sql, params) = f.generate_sql();
                return (format!("WHERE {}", sql), params);
            }
        }
    }
}

#[derive(Debug, Clone)]
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

    pub fn generate_sql(&self) -> (String, Vec<String>) {
        let mut join = format!(
            "{} {} ON {} = {}",
            self.join_type.to_string(),
            self.table.name,
            self.left_field.field_name,
            self.right_field.field_name
        );
        let mut params = vec![];

        if let Some(filter) = &self.sql_filter {
            let (filter_sql, filter_params) = match filter {
                SqlFilter::Logical(f) => f.generate_sql(),
                SqlFilter::Conditional(f) => f.generate_sql(),
            };
            join += &format!(" AND {}", filter_sql);
            params.extend(filter_params);
        }

        return (join, params);
    }
}

#[derive(Debug, Clone)]
pub struct SqlGroupBy {
    pub fields: Vec<SqlTableField>,
    pub sql_filter: Option<SqlFilter>,
}

impl SqlGroupBy {
    pub fn new(fields: Vec<SqlTableField>, sql_filter: Option<SqlFilter>) -> Self {
        SqlGroupBy { fields, sql_filter }
    }

    pub fn generate_sql(&self) -> (String, Vec<String>) {
        let fields_sql = self
            .fields
            .iter()
            .map(|f| {
                format!(
                    "{}{}",
                    f.table_name
                        .clone()
                        .map_or("".to_string(), |tn| format!("{}.", tn)),
                    f.field_name
                )
            })
            .collect::<Vec<_>>()
            .join(", ");
        let mut group_by = format!("GROUP BY {}", fields_sql);
        let mut params = vec![];

        if let Some(filter) = &self.sql_filter {
            let (filter_sql, filter_params) = match filter {
                SqlFilter::Logical(f) => f.generate_sql(),
                SqlFilter::Conditional(f) => f.generate_sql(),
            };
            group_by += &format!(" HAVING {}", filter_sql);
            params.extend(filter_params);
        }

        return (group_by, params);
    }
}

#[derive(Debug, Clone)]
pub struct SqlHaving {
    pub filters: Vec<SqlFilter>,
}

impl SqlHaving {
    pub fn new(filters: Vec<SqlFilter>) -> Self {
        SqlHaving { filters }
    }

    pub fn generate_sql(&self) -> (String, Vec<String>) {
        let mut sql_parts = vec![];
        let mut params = vec![];

        for f in &self.filters {
            let (sql, p) = match f {
                SqlFilter::Logical(f) => f.generate_sql(),
                SqlFilter::Conditional(f) => f.generate_sql(),
            };
            sql_parts.push(sql);
            params.extend(p);
        }

        return (format!("HAVING {}", sql_parts.join(" AND ")), params);
    }
}

#[derive(Debug, Clone)]
pub struct SqlOrderBy {
    pub orderings: Vec<(SqlTableField, bool)>,
}

impl SqlOrderBy {
    pub fn new(orderings: Vec<(SqlTableField, bool)>) -> Self {
        SqlOrderBy { orderings }
    }

    pub fn generate_sql(&self) -> String {
        let orderings_sql = self
            .orderings
            .iter()
            .map(|(f, asc)| {
                format!(
                    "{}{} {}",
                    f.table_name
                        .clone()
                        .map_or("".to_string(), |tn| format!("{}.", tn)),
                    f.field_name,
                    if *asc { "ASC" } else { "DESC" }
                )
            })
            .collect::<Vec<_>>()
            .join(", ");
        return format!("ORDER BY {}", orderings_sql);
    }
}

#[derive(Debug, Clone)]
pub struct SqlLimit {
    pub limit: i32,
}

impl SqlLimit {
    pub fn new(limit: i32) -> Self {
        SqlLimit { limit }
    }

    pub fn generate_sql(&self) -> String {
        return format!("LIMIT {}", self.limit);
    }
}

#[derive(Debug, Clone)]
pub struct SqlOffset {
    pub offset: i32,
}

impl SqlOffset {
    pub fn new(offset: i32) -> Self {
        SqlOffset { offset }
    }

    pub fn generate_sql(&self) -> String {
        return format!("OFFSET {}", self.offset);
    }
}

#[derive(Debug, Clone)]
pub struct SqlDistinct {
    pub distinct: bool,
}

impl SqlDistinct {
    pub fn new(distinct: bool) -> Self {
        SqlDistinct { distinct }
    }
}

#[derive(Debug, Clone)]
pub struct SqlUpdatePair {
    pub field: SqlTableField,
    pub value: SqlValue,
}

impl SqlUpdatePair {
    pub fn new(field: SqlTableField, value: SqlValue) -> Self {
        SqlUpdatePair { field, value }
    }
}

pub trait SqlStatement {
    fn generate_query(&self) -> (String, Vec<String>);
}

#[derive(Debug, Clone)]
pub struct SelectStatement {
    pub from_table: SqlTable,
    pub projection: Option<Vec<SqlTableField>>,
    pub where_clause: Option<SqlWhere>,
    pub join: Option<Vec<SqlJoin>>,
    pub groupby: Option<SqlGroupBy>,
    pub having: Option<SqlHaving>,
    pub orderby: Option<SqlOrderBy>,
    pub limit: Option<SqlLimit>,
    pub offset: Option<SqlOffset>,
    pub distinct: Option<SqlDistinct>,
}

impl SelectStatement {
    pub fn new(
        from_table: SqlTable,
        projection: Option<Vec<SqlTableField>>,
        where_clause: Option<SqlWhere>,
        join: Option<Vec<SqlJoin>>,
        groupby: Option<SqlGroupBy>,
        having: Option<SqlHaving>,
        orderby: Option<SqlOrderBy>,
        limit: Option<SqlLimit>,
        offset: Option<SqlOffset>,
        distinct: Option<SqlDistinct>,
    ) -> Self {
        SelectStatement {
            from_table,
            projection,
            where_clause,
            join,
            groupby,
            having,
            orderby,
            limit,
            offset,
            distinct,
        }
    }

    pub fn generate_query(&self) -> (String, Vec<String>) {
        let mut query = "SELECT ".to_string();
        let mut params = vec![];

        if let Some(distinct) = &self.distinct {
            if distinct.distinct {
                query += "DISTINCT ";
            }
        }

        if let Some(projection) = &self.projection {
            let projection_sql = projection
                .iter()
                .map(|p| {
                    format!(
                        "{}{}",
                        p.table_name
                            .clone()
                            .map_or("".to_string(), |tn| format!("{}.", tn)),
                        p.field_name
                    )
                })
                .collect::<Vec<_>>()
                .join(", ");
            query += &projection_sql;
        } else {
            query += "*";
        }

        query += &format!(" FROM {}", self.from_table.name);

        if let Some(join) = &self.join {
            for j in join {
                let (join_sql, join_params) = j.generate_sql();
                query += &format!(" {}", join_sql);
                params.extend(join_params);
            }
        }

        if let Some(where_clause) = &self.where_clause {
            let (where_sql, where_params) = where_clause.generate_sql();
            query += &format!(" {}", where_sql);
            params.extend(where_params);
        }

        if let Some(groupby) = &self.groupby {
            let (groupby_sql, groupby_params) = groupby.generate_sql();
            query += &format!(" {}", groupby_sql);
            params.extend(groupby_params);
        }

        if let Some(having) = &self.having {
            let (having_sql, having_params) = having.generate_sql();
            query += &format!(" {}", having_sql);
            params.extend(having_params);
        }

        if let Some(orderby) = &self.orderby {
            let orderby_sql = orderby.generate_sql();
            query += &format!(" {}", orderby_sql);
        }

        if let Some(limit) = &self.limit {
            let limit_sql = limit.generate_sql();
            query += &format!(" {}", limit_sql);
        }

        if let Some(offset) = &self.offset {
            let offset_sql = offset.generate_sql();
            query += &format!(" {}", offset_sql);
        }

        return (query, params);
    }
}
