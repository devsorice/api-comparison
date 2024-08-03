from generating.model.model import Model
from generating.model.type import Type


class RustModel:
    def __init__(self, model:Model):
        self.model = model

    def get_rust_type(self, field_type):
        type_mapping = {
            Type.SHORT_TEXT_INPUT_TYPE_TEXT: "String",
            Type.EMAIL: "String",
            Type.INTEGER_INPUT_TYPE_NUMBER: "i32",
            Type.FLOAT_INPUT_TYPE_NUMBER: "f64",
            Type.LONG_TEXT_TEXTAREA_NEEDED: "String",
            Type.ADDRESS: "String",
            Type.URL: "String",
            Type.DATE: "chrono::NaiveDate",
            Type.DATETIME: "chrono::NaiveDateTime",
            Type.TIME: "chrono::NaiveTime",
            Type.OBJECT: "serde_json::Value",
            Type.ATTACHMENT_UPLOAD_NO_PREVIEW: "String",
            Type.PHOTO_UPLOAD_WITH_PREVIEW: "String",
            Type.NUMBER_INPUT_TYPE_NUMBER: "i64",
            Type.PHONE_NUMBER: "String",
            Type.SLUG: "String",
            Type.ARRAY: "Vec<serde_json::Value>",
            Type.PARAGRAPH_TITLE_AND_TEXT: "String",
            Type.JSON: "serde_json::Value",
            Type.HTML: "String",
            Type.UUID: "uuid::Uuid",
            Type.YES_NO_CHECKBOX: "bool",
            Type.ENABLE_DISABLE_TOGGLE: "bool",
            Type.COLOR: "String",
            Type.PASSWORD: "String",
            Type.ENUM_SINGLE_CHOICE_RADIO: "String",
            Type.ENUM_SINGLE_CHOICE_SELECT: "String",
            Type.ENUM_MULTIPLE_CHOICE_SELECT: "Vec<String>",
            Type.MONEY_AMOUNT: "f64",
        }
        return type_mapping.get(field_type, "String")

    def generate_field_definitions(self):
        rust_fields = []
        for field_name, field in self.model.fields.items():
            rust_field = f"pub {field_name}: Option<{self.get_rust_type(field.tp)}>,"
            rust_fields.append(rust_field)
        return "\n    ".join(rust_fields)



    def generate_bind_statements(self, fields):
        bind_statements = []
        for field_name in fields:
            bind_statements.append(f'query = query.bind(&model.{field_name});')
        return "\n        ".join(bind_statements)

    def generate_from_row_statements(self, fields):
        from_row_statements = []
        for field_name in fields:
            from_row_statements.append(f'let {field_name}: Option<{self.get_rust_type(self.model.fields[field_name].tp)}> = row.try_get("{field_name}").map_err(|e| AppError::DeserializationError(e.to_string()))?;')
        return "\n        ".join(from_row_statements)

    def generate_rust_code(self):
        field_definitions = self.generate_field_definitions()
        fields = [field_name for field_name, field in self.model.fields.items() if not field.required]
        bind_create = self.generate_bind_statements(fields)
        bind_update = self.generate_bind_statements(fields)
        from_row_statements = self.generate_from_row_statements(fields)

        rust_code = f"""
use crate::database::crud::{{CrudModel, CrudService}};
use crate::exceptions::AppError;
use async_trait::async_trait;
use axum::{{extract::Json, extract::Path, http::StatusCode, response::IntoResponse, Extension}};
use serde::{{Deserialize, Serialize}};
use serde_json::json;
use sqlx::{{postgres::PgRow, query::Query, PgPool, Postgres, Row}};

#[derive(Serialize, Deserialize)]
pub struct {self.model.slug_singular.capitalize()} {{
    {field_definitions}
}}

#[async_trait]
impl CrudModel for {self.model.slug_singular.capitalize()} {{
    fn table_name() -> &'static str {{
        "{self.model.table}"
    }}

    fn id_field() -> &'static str {{
        "id"
    }}

    fn fields() -> &'static [&'static str] {{
        &["{", ".join(fields)}"]
    }}

    fn list_fields() -> &'static [&'static str] {{
        &["id", "{", ".join(fields)}"]
    }}

    fn bind_create<'q>(
        mut query: Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments>,
        model: &'q Self,
    ) -> Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments> {{
        {bind_create}
        query
    }}

    fn bind_update<'q>(
        mut query: Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments>,
        model: &'q Self,
    ) -> Query<'q, Postgres, <Postgres as sqlx::database::HasArguments<'q>>::Arguments> {{
        {bind_update}
        query
    }}

    fn from_row(row: &PgRow) -> Result<Self, AppError> {{
        {from_row_statements}
        Ok({self.model.slug_singular.capitalize()} {{ {", ".join(fields)} }})
    }}
}}

fn convert_json<T>(json: Json<T>) -> T {{
    json.0
}}

fn response<T>(
    status: &str,
    error: bool,
    data: Option<axum::Json<T>>,
    message: Option<&str>,
) -> Json<serde_json::Value>
where
    T: Serialize,
{{
    let data = data.map(|d| json!(d.0));
    Json(json!({{
        "status": status,
        "error": error,
        "data": data,
        "message":message
    }}))
}}

// Handlers for CRUD operations go here...
"""
        return rust_code
