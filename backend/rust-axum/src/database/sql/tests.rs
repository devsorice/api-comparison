// [cfg(test)]
// mod tests {
//     use super::*; // Make sure all relevant SQL types and query builder functions are imported or defined in scope

//     struct TestSetup {
//         table: SqlTable,
//         field_name: SqlTableField,
//         field_age: SqlTableField,
//         field_salary: SqlTableField,
//         value_john: SqlValue,
//         value_age: SqlValue,
//         value_salary: SqlValue,
//         value_salary_update: SqlValue,
//     }

//     impl TestSetup {
//         fn new() -> Self {
//             Self {
//                 table: SqlTable::new("employees"),
//                 field_name: SqlTableField::new("name"),
//                 field_age: SqlTableField::new("age"),
//                 field_salary: SqlTableField::new("salary"),
//                 value_john: SqlValue::String("John Doe".to_string()),
//                 value_age: SqlValue::Int(30),
//                 value_salary: SqlValue::Int(50000),
//                 value_salary_update: SqlValue::Int(60000),
//             }
//         }
//     }

//     #[test]
//     fn test_build_select_statement_simple() {
//         let setup = TestSetup::new();
//         let params = SelectParams {
//             from_table: setup.table.name.clone(),
//             projection: vec!["name".to_string(), "age".to_string(), "salary".to_string()],
//             where_clause: Some(SqlFilter::Simple {
//                 field: "age".to_string(),
//                 operator: "gt".to_string(),
//                 value: setup.value_age,
//             }),
//             order_by: vec![OrderBy {
//                 field: "name".to_string(),
//                 ascending: true,
//             }],
//             limit: Some(10),
//             offset: Some(5),
//             distinct: true,
//         };
//         let select_statement = SQLQueryBuilder::build_select_statement(&params);
//         let (query, params) = select_statement.generate_query();
//         assert_eq!(
//             query,
//             "SELECT DISTINCT name, age, salary FROM employees WHERE age > ? ORDER BY name ASC LIMIT 10 OFFSET 5"
//         );
//         assert_eq!(params, vec![SqlParam::Int(30)]);
//     }

//     #[test]
//     fn test_build_insert_statement() {
//         let setup = TestSetup::new();
//         let params = InsertParams {
//             into_table: setup.table.name.clone(),
//             entity: vec![
//                 (setup.field_name.name.clone(), setup.value_john),
//                 (setup.field_age.name.clone(), setup.value_age),
//                 (setup.field_salary.name.clone(), setup.value_salary),
//             ],
//         };
//         let insert_statement = SQLQueryBuilder::build_insert_statement(&params);
//         assert_eq!(insert_statement.table.name, "employees");
//         assert_eq!(insert_statement.fields.len(), 3);
//         assert_eq!(insert_statement.fields[0].field_name, "name");
//         assert_eq!(
//             insert_statement.values[0],
//             SqlValue::String("John Doe".to_string())
//         );
//     }

//     #[test]
//     fn test_build_update_statement() {
//         let setup = TestSetup::new();
//         let params = UpdateParams {
//             table: setup.table.name.clone(),
//             updates: vec![
//                 (setup.field_salary.name.clone(), setup.value_salary_update),
//                 ("position".to_string(), SqlValue::String("Manager".to_string())),
//             ],
//             where_clause: Some(SqlFilter::Simple {
//                 field: "id".to_string(),
//                 operator: "eq".to_string(),
//                 value: SqlValue::Int(1),
//             }),
//         };
//         let update_statement = SQLQueryBuilder::build_update_statement(&params);
//         assert_eq!(update_statement.table.name, "employees");
//         assert_eq!(update_statement.updates.len(), 2);
//         assert_eq!(update_statement.updates[0].field.field_name, "salary");
//         assert_eq!(update_statement.updates[0].value, SqlValue::Int(60000));
//     }

//     #[test]
//     fn test_build_delete_statement() {
//         let setup = TestSetup::new();
//         let params = DeleteParams {
//             from_table: setup.table.name.clone(),
//             where_clause: Some(SqlFilter::Simple {
//                 field: "age".to_string(),
//                 operator: "lt".to_string(),
//                 value: SqlValue::Int(25),
//             }),
//         };
//         let delete_statement = SQLQueryBuilder::build_delete_statement(&params);
//         assert_eq!(delete_statement.from_table.name, "employees");
//         match delete_statement.where_clause.unwrap() {
//             SqlFilter::Simple { field, operator, value } => {
//                 assert_eq!(field, "age");
//                 assert_eq!(operator, "lt");
//                 assert_eq!(value, SqlValue::Int(25));
//             },
//             _ => panic!("Expected simple filter"),
//         }
//     }

//     #[test]
//     fn test_build_select_statement_with_joins() {
//         let setup = TestSetup::new();
//         let params = SelectParams {
//             from_table: setup.table.name.clone(),
//             projection: vec!["employees.name".to_string(), "departments.name".to_string()],
//             join: vec![SqlJoin {
//                 join_type: "inner".to_string(),
//                 table: "departments".to_string(),
//                 left_field: "dept_id".to_string(),
//                 right_field: "id".to_string(),
//                 condition: None,
//             }],
//             where_clause: Some(SqlFilter::Simple {
//                 field: "age".to_string(),
//                 operator: "gt".to_string(),
//                 value: SqlValue::Int(30),
//             }),
//             order_by: vec![OrderBy {
//                 field: "employees.name".to_string(),
//                 ascending: true,
//             }],
//             limit: Some(10),
//             offset: Some(5),
//             distinct: false,
//         };
//         let select_statement = SQLQueryBuilder::build_select_statement(&params);
//         let (query, params) = select_statement.generate_query();
//         assert_eq!(
//             query,
//             "SELECT employees.name, departments.name FROM employees INNER JOIN departments ON dept_id = id WHERE age > ? ORDER BY employees.name ASC LIMIT 10 OFFSET 5"
//         );
//         assert_eq!(params, vec![SqlParam::Int(30)]);
//     }

//     #[test]
//     fn test_build_select_statement_with_group_by_and_having() {
//         let setup = TestSetup::new();
//         let params = SelectParams {
//             from_table: setup.table.name.clone(),
//             projection: vec![
//                 "departments.name".to_string(),
//                 SelectProjection::AggregatedField {
//                     aggregation: "avg".to_string(),
//                     field: "salary".to_string(),
//                     table: Some("employees".to_string()),
//                 }
//             ],
//             join: vec![SqlJoin {
//                 join_type: "inner".to_string(),
//                 table: "departments".to_string(),
//                 left_field: "dept_id".to_string(),
//                 right_field: "id".to_string(),
//                 condition: None,
//             }],
//             group_by: Some(vec!["departments.name".to_string()]),
//             having: Some(SqlFilter::Simple {
//                 field: "avg_salary".to_string(),
//                 operator: "gt".to_string(),
//                 value: SqlValue::Int(50000),
//             }),
//             order_by: vec![OrderBy {
//                 field: "departments.name".to_string(),
//                 ascending: true,
//             }],
//             limit: None,
//             offset: None,
//             distinct: false,
//         };
//         let select_statement = SQLQueryBuilder::build_select_statement(&params);
//         let (query, params) = select_statement.generate_query();
//         assert_eq!(
//             query,
//             "SELECT departments.name, AVG(employees.salary) FROM employees INNER JOIN departments ON dept_id = id GROUP BY departments.name HAVING avg_salary > ? ORDER BY departments.name ASC"
//         );
//         assert_eq!(params, vec![SqlParam::Int(50000)]);
//     }

//     #[test]
//     fn test_build_select_statement_with_complex_filter() {
//         let setup = TestSetup::new();
//         let params = SelectParams {
//             from_table: setup.table.name.clone(),
//             projection: vec!["name".to_string(), "age".to_string(), "salary".to_string()],
//             where_clause: Some(SqlFilter::Complex {
//                 operator: "or".to_string(),
//                 filters: vec![
//                     SqlFilter::Simple { field: "age".to_string(), operator: "gt".to_string(), value: SqlValue::Int(30) },
//                     SqlFilter::Simple { field: "status".to_string(), operator: "eq".to_string(), value: SqlValue::String("active".to_string()) }
//                 ]
//             }),
//             order_by: vec![OrderBy { field: "name".to_string(), ascending: true }],
//             limit: None,
//             offset: None,
//             distinct: false,
//         };
//         let select_statement = SQLQueryBuilder::build_select_statement(&params);
//         let (query, params) = select_statement.generate_query();
//         assert_eq!(
//             query,
//             "SELECT name, age, salary FROM employees WHERE (age > ?) OR (status = ?) ORDER BY name ASC"
//         );
//         assert_eq!(params, vec![SqlParam::Int(30), SqlParam::String("active".to_string())]);
//     }

//     #[test]
//     fn test_build_select_statement_with_nested_or_and_short_syntax() {
//         let setup = TestSetup::new();
//         let params = SelectParams {
//             from_table: setup.table.name.clone(),
//             projection: vec!["name".to_string(), "age".to_string(), "salary".to_string()],
//             where_clause: Some(SqlFilter::Complex {
//                 operator: "or".to_string(),
//                 filters: vec![
//                     SqlFilter::Simple { field: "age".to_string(), operator: "gt".to_string(), value: SqlValue::Int(30) },
//                     SqlFilter::Complex {
//                         operator: "and".to_string(),
//                         filters: vec![
//                             SqlFilter::Simple { field: "status".to_string(), operator: "eq".to_string(), value: SqlValue::String("active".to_string()) },
//                             SqlFilter::Simple { field: "salary".to_string(), operator: "gt".to_string(), value: SqlValue::Int(200000) }
//                         ]
//                     }
//                 ]
//             }),
//             order_by: vec![],
//             limit: None,
//             offset: None,
//             distinct: false,
//         };
//         let select_statement = SQLQueryBuilder::build_select_statement(&params);
//         let (query, params) = select_statement.generate_query();
//         assert_eq!(
//             query,
//             "SELECT name, age, salary FROM employees WHERE (age > ?) OR ((status = ?) AND (salary > ?))"
//         );
//         assert_eq!(params, vec![SqlParam::Int(30), SqlParam::String("active".to_string()), SqlParam::Int(200000)]);
//     }

//     #[test]
//     fn test_build_select_statement_with_complex_filter_short_syntax_and() {
//         let setup = TestSetup::new();
//         let params = SelectParams {
//             from_table: setup.table.name.clone(),
//             projection: vec!["name".to_string(), "age".to_string(), "salary".to_string()],
//             where_clause: Some(SqlFilter::Complex {
//                 operator: "and".to_string(),
//                 filters: vec![
//                     SqlFilter::Simple { field: "age".to_string(), operator: "gt".to_string(), value: SqlValue::Int(30) },
//                     SqlFilter::Simple { field: "status".to_string(), operator: "eq".to_string(), value: SqlValue::String("active".to_string()) }
//                 ]
//             }),
//             order_by: vec![OrderBy { field: "name".to_string(), ascending: true }],
//             limit: None,
//             offset: None,
//             distinct: false,
//         };
//         let select_statement = SQLQueryBuilder::build_select_statement(&params);
//         let (query, params) = select_statement.generate_query();
//         assert_eq!(
//             query,
//             "SELECT name, age, salary FROM employees WHERE (age > ?) AND (status = ?) ORDER BY name ASC"
//         );
//         assert_eq!(params, vec![SqlParam::Int(30), SqlParam::String("active".to_string())]);
//     }

//     #[test]
//     fn test_build_select_statement_with_logical_operators() {
//         let setup = TestSetup::new();
//         let params = SelectParams {
//             from_table: setup.table.name.clone(),
//             projection: vec!["name".to_string(), "age".to_string(), "salary".to_string()],
//             where_clause: Some(SqlFilter::Complex {
//                 operator: "or".to_string(),
//                 filters: vec![
//                     SqlFilter::Simple { field: "status".to_string(), operator: "eq".to_string(), value: SqlValue::String("active".to_string()) },
//                     SqlFilter::Simple { field: "name".to_string(), operator: "ne".to_string(), value: SqlValue::String("John".to_string()) },
//                     SqlFilter::Simple { field: "age".to_string(), operator: "lt".to_string(), value: SqlValue::Int(25) },
//                     SqlFilter::Simple { field: "salary".to_string(), operator: "gt".to_string(), value: SqlValue::Int(300000) },
//                     SqlFilter::Simple { field: "savings".to_string(), operator: "lte".to_string(), value: SqlValue::Int(50000) },
//                     SqlFilter::Simple { field: "investments".to_string(), operator: "gte".to_string(), value: SqlValue::Int(5000000) },
//                     SqlFilter::Complex {
//                         operator: "in".to_string(),
//                         filters: vec![
//                             SqlFilter::Simple { field: "position".to_string(), operator: "in".to_string(), value: SqlValue::Array(vec!["senior", "executive", "sales"].into_iter().map(SqlValue::String).collect()) }
//                         ]
//                     },
//                     SqlFilter::Complex {
//                         operator: "not_in".to_string(),
//                         filters: vec![
//                             SqlFilter::Simple { field: "employment_status".to_string(), operator: "nin".to_string(), value: SqlValue::Array(vec!["fired", "new_entry"].into_iter().map(SqlValue::String).collect()) }
//                         ]
//                     },
//                     SqlFilter::Simple { field: "email".to_string(), operator: "contains".to_string(), value: SqlValue::String("@gmail.com".to_string()) },
//                     SqlFilter::Simple { field: "phone".to_string(), operator: "ncontains".to_string(), value: SqlValue::String("+39".to_string()) }
//                 ]
//             }),
//             order_by: vec![OrderBy { field: "name".to_string(), ascending: true }],
//             limit: None,
//             offset: None,
//             distinct: false,
//         };
//         let select_statement = SQLQueryBuilder::build_select_statement(&params);
//         let (query, params) = select_statement.generate_query();
//         assert_eq!(
//             query,
//             "SELECT name, age, salary FROM employees WHERE (status = ?) OR (name != ?) OR (age < ?) OR (salary > ?) OR \
//             (savings <= ?) OR (investments >= ?) OR (position IN (?, ?, ?)) OR (employment_status NOT IN (?, ?)) OR \
//             (email LIKE ?) OR (phone NOT LIKE ?) ORDER BY name ASC"
//         );
//         let expected_params = vec![
//             SqlParam::String("active".to_string()), SqlParam::String("John".to_string()), SqlParam::Int(25),
//             SqlParam::Int(300000), SqlParam::Int(50000), SqlParam::Int(5000000), SqlParam::String("senior".to_string()),
//             SqlParam::String("executive".to_string()), SqlParam::String("sales".to_string()), SqlParam::String("fired".to_string()),
//             SqlParam::String("new_entry".to_string()), SqlParam::String("%@gmail.com%".to_string()), SqlParam::String("%+39%".to_string())
//         ];
//         assert_eq!(params, expected_params);
//     }

//   }
