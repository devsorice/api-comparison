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
        match val {
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
}
