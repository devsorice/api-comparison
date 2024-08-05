#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
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
            "SUM" => Some(Self::Sum),
            "AVG" => Some(Self::Avg),
            "MAX" => Some(Self::Max),
            "MIN" => Some(Self::Min),
            "COUNT" => Some(Self::Count),
            "DISTINCT" => Some(Self::Distinct),
            _ => None,
        }
    }
    pub fn to_string(&self) -> &str {
        match self {
            Self::Sum => "SUM",
            Self::Avg => "AVG",
            Self::Max => "MAX",
            Self::Min => "MIN",
            Self::Count => "COUNT",
            Self::Distinct => "DISTINCT",
            _ => "",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
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
            "INNER JOIN" => Some(Self::InnerJoin),
            "LEFT JOIN" => Some(Self::LeftJoin),
            "RIGHT JOIN" => Some(Self::RightJoin),
            "FULL JOIN" => Some(Self::FullJoin),
            "CROSS JOIN" => Some(Self::CrossJoin),
            "NATURAL JOIN" => Some(Self::NaturalJoin),
            "LEFT OUTER JOIN" => Some(Self::LeftOuterJoin),
            "RIGHT OUTER JOIN" => Some(Self::RightOuterJoin),
            "FULL OUTER JOIN" => Some(Self::FullOuterJoin),
            _ => None,
        }
    }
    pub fn to_string(&self) -> &str {
        match self {
            Self::InnerJoin => "INNER JOIN",
            Self::LeftJoin => "LEFT JOIN",
            Self::RightJoin => "RIGHT JOIN",
            Self::FullJoin => "FULL JOIN",
            Self::CrossJoin => "CROSS JOIN",
            Self::NaturalJoin => "NATURAL JOIN",
            Self::LeftOuterJoin => "LEFT OUTER JOIN",
            Self::RightOuterJoin => "RIGHT OUTER JOIN",
            Self::FullOuterJoin => "FULL OUTER JOIN",
            _ => "",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum LogicalOperator {
    Equal,
    NotEqual,
    LessThan,
    GreaterThan,
    LessThanOrEqual,
    GreaterThanOrEqual,
    In,
    NotIn,
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
        match val {
            "eq" => Some(Self::Equal),
            "ne" => Some(Self::NotEqual),
            "lt" => Some(Self::LessThan),
            "gt" => Some(Self::GreaterThan),
            "lte" => Some(Self::LessThanOrEqual),
            "gte" => Some(Self::GreaterThanOrEqual),
            "in" => Some(Self::In),
            "nin" => Some(Self::NotIn),
            "contains" => Some(Self::Contains),
            "ncontains" => Some(Self::NotContains),
            "containss" => Some(Self::ContainsCaseSensitive),
            "ncontainss" => Some(Self::NotContainsCaseSensitive),
            "between" => Some(Self::Between),
            "nbetween" => Some(Self::NotBetween),
            "null" => Some(Self::IsNull),
            "nnull" => Some(Self::IsNotNull),
            "startswith" => Some(Self::StartsWith),
            "nstartswith" => Some(Self::NotStartsWith),
            "startswiths" => Some(Self::StartsWithCaseSensitive),
            "nstartswiths" => Some(Self::NotStartsWithCaseSensitive),
            "endswith" => Some(Self::EndsWith),
            "nendswith" => Some(Self::NotEndsWith),
            "endswiths" => Some(Self::EndsWithCaseSensitive),
            "nendswiths" => Some(Self::NotEndsWithCaseSensitive),
            "or" => Some(Self::Or),
            "and" => Some(Self::And),
            _ => None,
        }
    }

    pub fn to_string(&self) -> &str {
        match self {
            Self::Equal => "eq",
            Self::NotEqual => "ne",
            Self::LessThan => "lt",
            Self::GreaterThan => "gt",
            Self::LessThanOrEqual => "lte",
            Self::GreaterThanOrEqual => "gte",
            Self::In => "in",
            Self::NotIn => "nin",
            Self::Contains => "contains",
            Self::NotContains => "ncontains",
            Self::ContainsCaseSensitive => "containss",
            Self::NotContainsCaseSensitive => "ncontainss",
            Self::Between => "between",
            Self::NotBetween => "nbetween",
            Self::IsNull => "null",
            Self::IsNotNull => "nnull",
            Self::StartsWith => "startswith",
            Self::NotStartsWith => "nstartswith",
            Self::StartsWithCaseSensitive => "startswiths",
            Self::NotStartsWithCaseSensitive => "nstartswiths",
            Self::EndsWith => "endswith",
            Self::NotEndsWith => "nendswith",
            Self::EndsWithCaseSensitive => "endswiths",
            Self::NotEndsWithCaseSensitive => "nendswiths",
            Self::Or => "or",
            Self::And => "and",
            _ => "",
        }
    }

    pub fn to_sql(&self) -> &str {
        match self {
            Self::Equal => "=",
            Self::NotEqual => "!=",
            Self::LessThan => "<",
            Self::GreaterThan => ">",
            Self::LessThanOrEqual => "<=",
            Self::GreaterThanOrEqual => ">=",
            Self::In => "IN",
            Self::NotIn => "NOT IN",
            Self::Contains => "LIKE",
            Self::NotContains => "NOT LIKE",
            Self::ContainsCaseSensitive => "LIKE BINARY",
            Self::NotContainsCaseSensitive => "NOT LIKE BINARY",
            Self::Between => "BETWEEN",
            Self::NotBetween => "NOT BETWEEN",
            Self::IsNull => "IS NULL",
            Self::IsNotNull => "IS NOT NULL",
            Self::StartsWith => "LIKE",
            Self::NotStartsWith => "NOT LIKE",
            Self::StartsWithCaseSensitive => "LIKE BINARY",
            Self::NotStartsWithCaseSensitive => "NOT LIKE BINARY",
            Self::EndsWith => "LIKE",
            Self::NotEndsWith => "NOT LIKE",
            Self::EndsWithCaseSensitive => "LIKE BINARY",
            Self::NotEndsWithCaseSensitive => "NOT LIKE BINARY",
            Self::Or => "OR",
            Self::And => "AND",
            _ => "",
        }
    }
}
