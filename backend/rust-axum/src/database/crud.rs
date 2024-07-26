use crate::exceptions::AppError;
use async_trait::async_trait;
use axum::http::StatusCode;
use axum::Json;
use log::info;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use sqlx::Row;
use sqlx::{query::Query, PgPool, Postgres};
use std::marker::PhantomData;

#[async_trait]
pub trait CrudModel: Serialize + for<'de> Deserialize<'de> + Send + Sync + Unpin + 'static {
    fn table_name() -> &'static str;
    fn id_field() -> &'static str;
    fn fields() -> &'static [&'static str];
    fn bind_create<'q>(
        query: Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments>,
        model: &'q Self,
    ) -> Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments>;
    fn bind_update<'q>(
        query: Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments>,
        model: &'q Self,
    ) -> Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments>;
}

pub struct CrudService<T: CrudModel> {
    pool: PgPool,
    _marker: PhantomData<T>,
}

impl<T: CrudModel> CrudService<T> {
    pub fn new(pool: PgPool) -> Self {
        Self {
            pool,
            _marker: PhantomData,
        }
    }

    pub async fn get(&self, id: i32) -> Result<Json<T>, StatusCode> {
        let query = format!(
            "SELECT {} FROM {} WHERE {} = $1",
            T::fields().join(", "),
            T::table_name(),
            T::id_field()
        );
        info!("Executing query: {}", &query);
        let row = sqlx::query(&query)
            .bind(id)
            .fetch_one(&self.pool)
            .await
            .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

        let model: T = serde_json::from_value(row.try_get("json").unwrap())
            .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
        Ok(Json(model))
    }

    pub async fn create(&self, model: T) -> Result<Json<i64>, AppError> {
        let query = format!(
            "INSERT INTO {} ({}) VALUES ({}) RETURNING {}",
            T::table_name(),
            T::fields().join(", "),
            (1..=T::fields().len())
                .map(|i| format!("${}", i))
                .collect::<Vec<_>>()
                .join(", "),
            T::id_field()
        );
        info!("Executing query: {}", &query);
        let query = T::bind_create(sqlx::query(&query), &model);

        let row = query
            .fetch_one(&self.pool)
            .await
            .map_err(AppError::DatabaseError)?;

        let id: i64 = row.try_get("id").unwrap_or_default();
        Ok(Json(id))
    }

    pub async fn create_many(&self, models: Vec<T>) -> Result<Json<Vec<i64>>, StatusCode> {
        let mut ids = Vec::new();

        for model in models {
            let query = format!(
                "INSERT INTO {} ({}) VALUES ({}) RETURNING {}",
                T::table_name(),
                T::fields().join(", "),
                (1..=T::fields().len())
                    .map(|i| format!("${}", i))
                    .collect::<Vec<_>>()
                    .join(", "),
                T::id_field()
            );
            info!("Executing query: {}", &query);
            let query = T::bind_create(sqlx::query(&query), &model);

            let row = query
                .fetch_one(&self.pool)
                .await
                .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

            let id: i64 = row.try_get("id").unwrap_or_default();
            ids.push(id);
        }

        Ok(Json(ids))
    }

    pub async fn list(&self) -> Result<Json<Vec<T>>, StatusCode> {
        let query = format!("SELECT {} FROM {}", T::fields().join(", "), T::table_name());
        info!("Executing query: {}", &query);

        let rows = sqlx::query(&query)
            .fetch_all(&self.pool)
            .await
            .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

        let models: Vec<T> = rows
            .into_iter()
            .map(|row| serde_json::from_value(row.try_get("json").unwrap()).unwrap())
            .collect();

        Ok(Json(models))
    }

    pub async fn delete(&self, id: i32) -> Result<StatusCode, StatusCode> {
        let query = format!(
            "DELETE FROM {} WHERE {} = $1",
            T::table_name(),
            T::id_field()
        );
        info!("Executing query: {}", &query);

        let result = sqlx::query(&query)
            .bind(id)
            .execute(&self.pool)
            .await
            .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

        if result.rows_affected() == 0 {
            return Err(StatusCode::NOT_FOUND);
        }

        Ok(StatusCode::OK)
    }

    pub async fn update(&self, id: i32, model: T) -> Result<StatusCode, StatusCode> {
        let query = format!(
            "UPDATE {} SET {} WHERE {} = $3",
            T::table_name(),
            T::fields()
                .iter()
                .enumerate()
                .map(|(i, field)| format!("{} = ${}", field, i + 1))
                .collect::<Vec<_>>()
                .join(", "),
            T::id_field()
        );
        info!("Executing query: {}", &query);

        let query = T::bind_update(sqlx::query(&query), &model).bind(id);

        let result = query
            .execute(&self.pool)
            .await
            .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

        if result.rows_affected() == 0 {
            return Err(StatusCode::NOT_FOUND);
        }

        Ok(StatusCode::OK)
    }

    pub async fn update_many(&self, models: Vec<(i32, T)>) -> Result<StatusCode, StatusCode> {
        for (id, model) in models {
            let query = format!(
                "UPDATE {} SET {} WHERE {} = $3",
                T::table_name(),
                T::fields()
                    .iter()
                    .enumerate()
                    .map(|(i, field)| format!("{} = ${}", field, i + 1))
                    .collect::<Vec<_>>()
                    .join(", "),
                T::id_field()
            );
            info!("Executing query: {}", &query);
            let query = T::bind_update(sqlx::query(&query), &model).bind(id);

            let result = query
                .execute(&self.pool)
                .await
                .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

            if result.rows_affected() == 0 {
                return Err(StatusCode::NOT_FOUND);
            }
        }

        Ok(StatusCode::OK)
    }

    pub async fn duplicate(&self, id: i32) -> Result<Json<i64>, AppError> {
        let query = format!(
            "SELECT {} FROM {} WHERE {} = $1",
            T::fields().join(", "),
            T::table_name(),
            T::id_field()
        );
        info!("Executing query: {}", &query);

        let row = sqlx::query(&query)
            .bind(id)
            .fetch_one(&self.pool)
            .await
            .map_err(AppError::DatabaseError)?;

        let json_value: Value = row
            .try_get("json")
            .map_err(|e| AppError::DatabaseError(e.into()))?;

        let model: T = serde_json::from_value(json_value).map_err(|e| {
            AppError::DeserializationError(format!("Failed to deserialize JSON: {}", e))
        })?;

        self.create(model).await
    }
}
