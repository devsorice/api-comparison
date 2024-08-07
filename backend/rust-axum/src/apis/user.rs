use crate::database::crud::{CrudModel, CrudService};
use crate::exceptions::AppError;
use async_trait::async_trait;
use axum::{
    extract::Json, extract::Path, http::StatusCode, response::IntoResponse, Extension, Query,
};
use serde::{Deserialize, Serialize};
use serde_json::json;
use serde_qs::from_str;
use sqlx::{postgres::PgRow, query::Query, PgPool, Postgres, Row};

#[derive(Serialize, Deserialize)]
pub struct User {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub id: Option<i32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub name: Option<String>,
    pub email: String,
}

#[async_trait]
impl CrudModel for User {
    fn table_name() -> &'static str {
        "users"
    }

    fn id_field() -> &'static str {
        "id"
    }

    fn fields() -> &'static [&'static str] {
        &["name", "email"]
    }

    fn list_fields() -> &'static [&'static str] {
        &["id", "name", "email"]
    }

    fn bind_create<'q>(
        mut query: Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments>,
        model: &'q Self,
    ) -> Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments> {
        query = query.bind(&model.name).bind(&model.email);
        query
    }

    fn bind_update<'q>(
        mut query: Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments>,
        model: &'q Self,
    ) -> Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments> {
        query = query.bind(&model.name).bind(&model.email);
        query
    }
    fn from_row(row: &PgRow) -> Result<Self, AppError> {
        let id: Option<i32> = row
            .try_get("id")
            .map_err(|e| AppError::DeserializationError(e.to_string()))?;
        let name: Option<String> = row
            .try_get("name")
            .map_err(|e| AppError::DeserializationError(e.to_string()))?;
        let email: String = row
            .try_get("email")
            .map_err(|e| AppError::DeserializationError(e.to_string()))?;
        Ok(User { id, name, email })
    }
}

fn convert_json<T>(json: Json<T>) -> T {
    json.0
}

fn response<T>(
    status: &str,
    error: bool,
    data: Option<axum::Json<T>>,
    message: Option<&str>,
) -> Json<serde_json::Value>
where
    T: Serialize,
{
    let data = data.map(|d| json!(d.0));
    Json(json!({
        "status": status,
        "error": error,
        "data": data,
        "message":message
    }))
}

pub async fn get_user_handler(
    Path(id): Path<i32>,
    Extension(pool): Extension<PgPool>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.get(id).await {
        Ok(user) => (StatusCode::OK, response("success", false, Some(user), None)).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            response::<User>(
                "error",
                true,
                None,
                Some(&format!("Failed to get user -> {}", e)),
            ),
        )
            .into_response(),
    }
}

pub async fn create_user_handler(
    Extension(pool): Extension<PgPool>,
    axum::extract::Json(input): axum::extract::Json<User>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    let input = convert_json(Json(input));
    match service.create(input).await {
        Ok(id) => (
            StatusCode::CREATED,
            response("success", false, Some(id), None),
        )
            .into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            response::<i64>(
                "error",
                true,
                None,
                Some(&format!("Failed to create user -> {}", e)),
            ),
        )
            .into_response(),
    }
}

pub async fn create_users_handler(
    Extension(pool): Extension<PgPool>,
    Json(inputs): Json<Vec<User>>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    let inputs = convert_json(Json(inputs));
    match service.create_many(inputs).await {
        Ok(ids) => (
            StatusCode::CREATED,
            response("success", false, Some(ids), None),
        )
            .into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            response::<Vec<i64>>(
                "error",
                true,
                None,
                Some(&format!("Failed to create users -> {}", e)),
            ),
        )
            .into_response(),
    }
}

pub async fn list_users_handler(Extension(pool): Extension<PgPool>) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);

    match service.list(None, None, None, None, None).await {
        Ok(users) => (
            StatusCode::OK,
            response("success", false, Some(users), None),
        )
            .into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            response::<Vec<User>>(
                "error",
                true,
                None,
                Some(&format!("Failed to list users -> {}", e)),
            ),
        )
            .into_response(),
    }
}

pub async fn delete_user_handler(
    Path(id): Path<i32>,
    Extension(pool): Extension<PgPool>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.delete(id).await {
        Ok(_) => (StatusCode::OK, response::<()>("success", false, None, None)).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            response::<()>(
                "error",
                true,
                None,
                Some(&format!("Failed to delete user -> {}", e)),
            ),
        )
            .into_response(),
    }
}

pub async fn update_user_handler(
    Path(id): Path<i32>,
    Extension(pool): Extension<PgPool>,
    Json(input): Json<User>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    let input = convert_json(Json(input));
    match service.update(id, input).await {
        Ok(_) => (StatusCode::OK, response::<()>("success", false, None, None)).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            response::<()>(
                "error",
                true,
                None,
                Some(&format!("Failed to update user -> {}", e)),
            ),
        )
            .into_response(),
    }
}

pub async fn update_users_handler(
    Extension(pool): Extension<PgPool>,
    Json(inputs): Json<Vec<(i32, User)>>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    let inputs = convert_json(Json(inputs));
    match service.update_many(inputs).await {
        Ok(_) => (StatusCode::OK, response::<()>("success", false, None, None)).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            response::<()>(
                "error",
                true,
                None,
                Some(&format!("Failed to update users -> {}", e)),
            ),
        )
            .into_response(),
    }
}

pub async fn duplicate_user_handler(
    Path(id): Path<i32>,
    Extension(pool): Extension<PgPool>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.duplicate(id).await {
        Ok(new_id) => (
            StatusCode::CREATED,
            response("success", false, Some(new_id), None),
        )
            .into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            response::<i64>(
                "error",
                true,
                None,
                Some(&format!("Failed to duplicate user -> {}", e)),
            ),
        )
            .into_response(),
    }
}
