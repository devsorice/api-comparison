mod apis;
mod database;
mod services;

use apis::user::list_users;
use axum::{extract::Extension, routing::get, Router, Server};
use log::{error, info};
use services::services::Services;
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    // Initialize all services
    let services = Services::init().await;

    info!("Starting Crud Api - version: {}", services.version);

    // Create the Axum router
    let app = Router::new()
        .route("/users", get(list_users))
        .layer(Extension(services.database.get_pool()));

    let server_address: SocketAddr = "0.0.0.0:5555".parse().expect("Invalid address");

    // Log the server address
    info!("Creating server at {}", server_address);

    // Separate the binding step
    let server = match Server::try_bind(&server_address) {
        Ok(server) => server,
        Err(e) => {
            error!("Couldn't create server: {}", e);
            return;
        }
    };

    // Run the Axum server
    if let Err(e) = server.serve(app.into_make_service()).await {
        error!("Server error: {}", e);
    }
}
