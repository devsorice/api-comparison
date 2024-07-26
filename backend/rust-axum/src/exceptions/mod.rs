use axum::{http::StatusCode, response::IntoResponse, Json};
use serde_json::json;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Database error -> {0}")]
    DatabaseError(#[from] sqlx::Error),
    #[error("Deserialization error -> {0}")]
    DeserializationError(String),
}

impl IntoResponse for AppError {
    fn into_response(self) -> axum::response::Response {
        let error_message = format!("{}", self);
        let error_json = json!({
            "status": "error",
            "error": true,
            "message": error_message,
        });
        (StatusCode::INTERNAL_SERVER_ERROR, Json(error_json)).into_response()
    }
}
