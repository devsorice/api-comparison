pub mod logger;
pub mod database;

use log::error;
use sqlx::PgPool;
use std::env;
use self::database::Database;

pub struct Services {
    pub database_pool: PgPool,
    pub version: String
}

impl Services {
    pub async fn init() -> Self {
        // Initialize logger
        logger::Logger::init();

        let version = env!("CARGO_PKG_VERSION");
        info!("Starting Crud Api - version: {}", version);

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

        let port: u16 = env::var("POSTGRES_PORT").unwrap_or_else(|e| {
            error!("POSTGRES_PORT not set: {}", e);
            panic!("POSTGRES_PORT not set");
        }).parse().unwrap_or_else(|e| {
            error!("POSTGRES_PORT must be a number: {}", e);
            panic!("POSTGRES_PORT must be a number");
        });

        let database_name = env::var("POSTGRES_DB").unwrap_or_else(|e| {
            error!("POSTGRES_DB not set: {}", e);
            panic!("POSTGRES_DB not set");
        });

        // Initialize database pool
        let database_pool = Database::init_pool(&username, &password, &hostname, port, &database_name).await;

        Services { version, database_pool }
    }
}
