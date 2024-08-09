use crate::database::sql::{
    query_builder::{ConditionalFilter, FilterInput, SimpleFilter},
    values::SqlValue,
};
use serde_json::{json, Map, Value};
use std::collections::HashMap;

pub struct QueryStringParser;

impl QueryStringParser {
    pub fn parse_value(value: &str) -> SqlValue {
        if let Ok(int_val) = value.parse::<i32>() {
            SqlValue::Integer(int_val)
        } else if let Ok(float_val) = value.parse::<f64>() {
            SqlValue::Float(float_val)
        } else {
            SqlValue::String(value.to_owned())
        }
    }

    pub fn parse_filter(key: &str, value: &str) -> FilterInput {
        let parts: Vec<&str> = key.split("___").collect();
        let field = parts[0].to_string();
        let operator = parts[1].to_string();
        let sql_value = Self::parse_value(value);
        FilterInput::Simple(SimpleFilter {
            field,
            table: None,
            operator,
            value: sql_value,
        })
    }

    pub fn transform_input_filter(input: &Map<String, Value>) -> FilterInput {
        let mut filters = vec![];
        for (key, value) in input {
            match value {
                Value::String(s) => {
                    filters.push(Self::parse_filter(key, &s));
                }
                Value::Object(map) => {
                    filters.push(Self::transform_input_filter(&map));
                }
                Value::Array(arr) => {
                    let sub_filters = arr
                        .iter()
                        .map(|v| {
                            if let Value::Object(obj) = v {
                                Self::transform_input_filter(obj)
                            } else {
                                panic!("Invalid format in array!")
                            }
                        })
                        .collect();
                    filters.push(FilterInput::Conditional(ConditionalFilter {
                        operator: key.to_owned(),
                        filters: sub_filters,
                    }));
                }
                _ => panic!("Unhandled value type in input!"),
            }
        }
        FilterInput::Conditional(ConditionalFilter {
            operator: "and".to_string(), // Default logical operator, adjust as necessary
            filters,
        })
    }

    pub fn parse_nested_query_string(params: &HashMap<String, String>) -> Value {
        let mut root = Map::new();

        for (key, value) in params {
            let mut current_map = &mut root;
            let trimmed_key = key.trim_matches(|c| c == '[' || c == ']');
            let parts: Vec<&str> = trimmed_key.split(']').collect();

            for (i, part) in parts.iter().enumerate() {
                if i == parts.len() - 1 {
                    // Last part, assign the value
                    if let Some(inner_part) = part.split('[').next() {
                        current_map.insert(inner_part.to_string(), Value::String(value.clone()));
                    }
                } else {
                    // Not last part, navigate or create map
                    let inner_key = part.split('[').next().unwrap();
                    current_map = current_map
                        .entry(inner_key.to_string())
                        .or_insert_with(|| Value::Object(Map::new()))
                        .as_object_mut()
                        .unwrap();
                }
            }
        }

        Value::Object(root)
    }

    pub fn test() {
        // Test setup for TEST 1
        let input1 = json!({
            "or": {
                "a___eq": "5",
                "b___eq": "9",
                "and": {
                    "c___eq": "2",
                    "or": {
                        "d___eq": "3",
                        "e___eq": "4"
                    }
                }
            }
        });
        let mut query_map1 = HashMap::new();
        query_map1.insert("filter[or][a___eq]".to_string(), "5".to_string());
        query_map1.insert("filter[or][b___eq]".to_string(), "9".to_string());
        query_map1.insert("filter[or][and][c___eq]".to_string(), "2".to_string());
        query_map1.insert("filter[or][and][or][d___eq]".to_string(), "3".to_string());
        query_map1.insert("filter[or][and][or][e___eq]".to_string(), "4".to_string());

        let parsed_value1 = Self::parse_nested_query_string(&query_map1);
        println!("TEST 1 Parsed Nested: {:#?}", parsed_value1);
        let transformed1 = Self::transform_input_filter(input1.as_object().unwrap());
        println!("TEST 1 Transformed Output: {:#?}", transformed1);

        // Test setup for TEST 2
        let input2 = json!({
            "and": [
                {"b___eq": "5", "d___eq": "6"},
                {"c___eq": "7"}
            ]
        });
        let mut query_map2 = HashMap::new();
        query_map2.insert("filter[and][0][b___eq]".to_string(), "5".to_string());
        query_map2.insert("filter[and][0][d___eq]".to_string(), "6".to_string());
        query_map2.insert("filter[and][1][c___eq]".to_string(), "7".to_string());

        let parsed_value2 = Self::parse_nested_query_string(&query_map2);
        println!("TEST 2 Parsed Nested: {:#?}", parsed_value2);
        let transformed2 = Self::transform_input_filter(input2.as_object().unwrap());
        println!("TEST 2 Transformed Output: {:#?}", transformed2);

        // Additional tests can be set up similarly
    }
}
