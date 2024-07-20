use log::{debug, error, log_enabled, info, Level};
use axum::{
  body::Body,
  http::StatusCode,
  response::{IntoResponse, Response},
  routing::{get, post},
  Json, Router,
  extract::{Path, Query}
};
use serde::Serialize;

#[derive(Serialize)]
pub struct User {
    id: u64,
    name: String,
    email: String,
}

// A handler /user/:id
pub async fn get_user(Path(id): Path<u32>) -> String {
  format!("User {}", id)
}


// Handler for /create-user
pub async fn create_user() -> impl IntoResponse {
    Response::builder()
        .status(StatusCode::CREATED)
        .body(Body::from("User created successfully"))
        .unwrap()
}
// Handler for /users
pub async fn list_users() -> Json<Vec<User>> {
    info!("Listing Users");
    let users = vec![
        User {
            id: 1,
            name: "Elijah".to_string(),
            email: "elijah@example.com".to_string(),
        },
        User {
            id: 2,
            name: "John".to_string(),
            email: "john@doe.com".to_string(),
        },
    ];
    Json(users)
}
