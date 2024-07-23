use crate::database::crud::{CrudModel, CrudService};
use async_trait::async_trait;
use axum::{extract::Path, http::StatusCode, response::IntoResponse, Extension, Json};
use serde::{Deserialize, Serialize};
use sqlx::{query::Query, PgPool, Postgres};

#[derive(Serialize, Deserialize)]
pub struct User {
    pub id: i32, // Updated to i32
    pub name: String,
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
}

// Converter function
fn convert_json<T>(json: Json<T>) -> T {
    json.0
}

pub async fn get_user_handler(
    Path(id): Path<i32>, // Updated to i32
    Extension(pool): Extension<PgPool>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.get(id).await {
        Ok(user) => (StatusCode::OK, user).into_response(),
        Err(status) => (status, "Error retrieving user").into_response(),
    }
}

pub async fn create_user_handler(
    Json(input): Json<User>,
    Extension(pool): Extension<PgPool>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.create(convert_json(Json(input))).await {
        Ok(id) => (StatusCode::CREATED, id).into_response(),
        Err(status) => (status, "Error creating user").into_response(),
    }
}

pub async fn create_users_handler(
    Json(inputs): Json<Vec<User>>,
    Extension(pool): Extension<PgPool>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.create_many(convert_json(Json(inputs))).await {
        Ok(ids) => (StatusCode::CREATED, ids).into_response(),
        Err(status) => (status, "Error creating users").into_response(),
    }
}

pub async fn list_users_handler(Extension(pool): Extension<PgPool>) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.list().await {
        Ok(users) => (StatusCode::OK, users).into_response(),
        Err(status) => (status, "Error listing users").into_response(),
    }
}

pub async fn delete_user_handler(
    Path(id): Path<i32>, // Updated to i32
    Extension(pool): Extension<PgPool>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.delete(id).await {
        Ok(_) => (StatusCode::OK, "User deleted successfully").into_response(),
        Err(status) => (status, "Error deleting user").into_response(),
    }
}

pub async fn update_user_handler(
    Path(id): Path<i32>, // Updated to i32
    Json(input): Json<User>,
    Extension(pool): Extension<PgPool>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.update(id, convert_json(Json(input))).await {
        Ok(_) => (StatusCode::OK, "User updated successfully").into_response(),
        Err(status) => (status, "Error updating user").into_response(),
    }
}

pub async fn update_users_handler(
    Json(inputs): Json<Vec<(i32, User)>>, // Updated to i32
    Extension(pool): Extension<PgPool>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.update_many(convert_json(Json(inputs))).await {
        Ok(_) => (StatusCode::OK, "Users updated successfully").into_response(),
        Err(status) => (status, "Error updating users").into_response(),
    }
}

pub async fn duplicate_user_handler(
    Path(id): Path<i32>, // Updated to i32
    Extension(pool): Extension<PgPool>,
) -> impl IntoResponse {
    let service = CrudService::<User>::new(pool);
    match service.duplicate(id).await {
        Ok(new_id) => (StatusCode::CREATED, new_id).into_response(),
        Err(status) => (status, "Error duplicating user").into_response(),
    }
}
