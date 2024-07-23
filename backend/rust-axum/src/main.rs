mod apis;
mod database;
mod services;

use apis::user::{
    create_user_handler, create_users_handler, delete_user_handler, duplicate_user_handler,
    get_user_handler, list_users_handler, update_user_handler, update_users_handler,
};
use axum::{extract::Extension, routing::get, routing::post, Router, Server};
use log::{error, info};
use services::services::Services;
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    // Initialize all services
    let services = Services::init().await;

    info!("Starting Crud Api - version: {}", services.version);

    let app = Router::new()
        .route("/user/get/:id", get(get_user_handler))
        .route("/user/create-one", post(create_user_handler))
        .route("/user/create-many", post(create_users_handler))
        .route("/user/list", get(list_users_handler))
        .route("/user/delete/:id", post(delete_user_handler))
        .route("/user/update-one/:id", post(update_user_handler))
        .route("/user/update-many", post(update_users_handler))
        .route("/user/duplicate/:id", post(duplicate_user_handler))
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
