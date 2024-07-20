use super::super::database::database::Database;
use super::logging::Logger;
use log::{error, info};
use std::env;

pub struct Services {
    pub version: String,
    pub database: Database,
}

impl Services {
    pub async fn init() -> Self {
        info!("--------- Initializing Services....");
        // Initialize logger
        Logger::init();

        let version = env!("CARGO_PKG_VERSION").to_string();

        // Read environment variables
        let username = env::var("POSTGRES_USER").unwrap_or_else(|e| {
            error!("POSTGRES_USER not set: {}", e);
            panic!("POSTGRES_USER not set");
        });

        let password = env::var("POSTGRES_PASSWORD").unwrap_or_else(|e| {
            error!("POSTGRES_PASSWORD not set: {}", e);
            panic!("POSTGRES_PASSWORD not set");
        });

        let hostname = env::var("POSTGRES_HOST").unwrap_or_else(|e| {
            error!("POSTGRES_HOST not set: {}", e);
            panic!("POSTGRES_HOST not set");
        });

        let port: u16 = env::var("POSTGRES_PORT")
            .unwrap_or_else(|e| {
                error!("POSTGRES_PORT not set: {}", e);
                panic!("POSTGRES_PORT not set");
            })
            .parse()
            .unwrap_or_else(|e| {
                error!("POSTGRES_PORT must be a number: {}", e);
                panic!("POSTGRES_PORT must be a number");
            });

        let database_name = env::var("POSTGRES_DB").unwrap_or_else(|e| {
            error!("POSTGRES_DB not set: {}", e);
            panic!("POSTGRES_DB not set");
        });

        // Initialize database pool
        let database = Database::init(&username, &password, &hostname, port, &database_name).await;

        Services { version, database }
    }
}
