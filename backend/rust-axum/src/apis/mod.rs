use std::collections::HashMap;

pub mod user;
pub mod utils;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize, Debug, PartialEq)]
pub struct ListPageQuery {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub projection: Option<Vec<String>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub filter: Option<HashMap<String, String>>,
    pub sort: Option<HashMap<String, String>>,
    pub limit: Option<u64>,
    pub page: Option<u64>,
}
