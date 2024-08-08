use sqlx::mysql::MySqlArguments;
use sqlx::postgres::PgArguments;
use sqlx::Arguments;

use super::values::SqlValue;

pub trait SqlValueConverter<DB> {
    fn convert(values: Vec<SqlValue>) -> DB;
}

impl SqlValueConverter<PgArguments> for PgArguments {
    fn convert(values: Vec<SqlValue>) -> PgArguments {
        let mut pg_args = PgArguments::default();
        for value in values {
            match value {
                SqlValue::Integer(i) => pg_args.add(i),
                SqlValue::Float(f) => pg_args.add(f),
                SqlValue::String(s) => pg_args.add(s),
                SqlValue::Boolean(b) => pg_args.add(b),
                SqlValue::Null => pg_args.add(None::<i32>), // Add None as a placeholder for NULL
            }
        }
        pg_args
    }
}

impl SqlValueConverter<MySqlArguments> for MySqlArguments {
    fn convert(values: Vec<SqlValue>) -> MySqlArguments {
        let mut mysql_args = MySqlArguments::default();
        for value in values {
            match value {
                SqlValue::Integer(i) => mysql_args.add(i),
                SqlValue::Float(f) => mysql_args.add(f),
                SqlValue::String(s) => mysql_args.add(s),
                SqlValue::Boolean(b) => mysql_args.add(b),
                SqlValue::Null => mysql_args.add(None::<i32>), // Add None as a placeholder for NULL
            }
        }
        mysql_args
    }
}
