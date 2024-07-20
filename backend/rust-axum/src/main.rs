mod database;
mod apis;
mod services;

use axum::{extract::Extension, routing::get, Router, Server};
use log::info;
use apis::user::list_users;
use services::Services;
use tokio;

#[tokio::main]
async fn main() {
    // Initialize all services
    let services = Services::init().await;

    // Create the Axum router
    let app = Router::new()
        .route("/users", get(list_users))
        .layer(Extension(services.database_pool));

    // Run the Axum server
    Server::bind(&"0.0.0.0:5555".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
