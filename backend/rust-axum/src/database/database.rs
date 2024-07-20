// src/services/database.rs

use super::config::PostgresConfiguration;
use log::{error, info};
use sqlx::PgPool;

pub struct Database {
    pub pool: PgPool,
}

impl Database {
    pub async fn init(
        username: &str,
        password: &str,
        hostname: &str,
        port: u16,
        database_name: &str,
    ) -> Self {
        let config =
            PostgresConfiguration::new(&username, &password, &hostname, port, &database_name);
        let database_url = config.connection_url();
        info!("Connection URL: {}", database_url);
        let pool = PgPool::connect(&database_url).await.unwrap_or_else(|e| {
            error!("Could not connect to the database: {}", e);
            panic!("Could not connect to the database");
        });
        Self { pool }
    }
    pub fn get_pool(&self) -> PgPool {
        self.pool.clone()
    }
}
