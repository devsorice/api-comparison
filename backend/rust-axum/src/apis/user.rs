use axum::extract::Extension;
use axum::{
    body::Body,
    extract::{Path, Query},
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use log::info;
use serde::Serialize;
use serde_json::json;
use sqlx::PgPool;
use sqlx::Row;

#[derive(Serialize)]
pub struct User {
    id: u64,
    name: String,
    email: String,
}

// A handler /user/:id
pub async fn get_user(Path(id): Path<u32>) -> String {
    info!("Getting user {}", id);
    return "".to_string();
}

// Handler for /create-user
pub async fn create_user() -> impl IntoResponse {
    Response::builder()
        .status(StatusCode::CREATED)
        .body(Body::from("User created successfully"))
        .unwrap()
}
// Handler for /users
pub async fn list_users(Extension(pool): Extension<PgPool>) -> impl IntoResponse {
    info!("Listing users:");
    let rows = match sqlx::query("SELECT id, name, email FROM users")
        .fetch_all(&pool)
        .await
    {
        Ok(rows) => {
            // Log the user count
            info!("Retrieved {} users", rows.len());
            rows
        }
        Err(e) => {
            log::error!("Error retrieving users: {:?}", e);
            return (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error").into_response();
        }
    };

    let users: Vec<serde_json::Value> = rows
        .into_iter()
        .map(|row| {
            json!({
                "id": row.try_get::<i32, _>("id").unwrap_or_default(),
                "name": row.try_get::<String, _>("name").unwrap_or_default(),
                "email": row.try_get::<String, _>("email").unwrap_or_default(),
            })
        })
        .collect();

    (StatusCode::OK, Json(users)).into_response()
}
