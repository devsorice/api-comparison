// src/services/database.rs

use log::{error, info};
use sqlx::PgPool;
use database::config::PostgresConfiguration;

pub struct Database;

impl Database {
    pub async fn init_pool(username: &str, password: &str, hostname: &str, port: u16, database_name: &str) -> PgPool {
        let config = PostgresConfiguration::new(&username, &password, &hostname, port, &database_name);
        let database_url = config.connection_url();
        info!("Connection URL: {}", database_url);
        PgPool::connect(&database_url).await.unwrap_or_else(|e| {
            error!("Could not connect to the database: {}", e);
            panic!("Could not connect to the database");
        })
    }
