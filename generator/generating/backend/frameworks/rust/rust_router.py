from generating.generators.router import Route, Router, VariableComponent


class RustRouter:
    def __init__(self):
        self.router = Router()
        self.routes = []

    def add_model_routes(self, models):
        self.models = models
        for model in models:
            slug = model.slug_singular
            routes = [
                (Route([slug, "get", VariableComponent("id")]), f"get_{slug}_handler"),
                (Route([slug, "create-one"]), f"create_{slug}_handler"),
                (Route([slug, "create-many"]), f"create_{slug}s_handler"),
                (Route([slug, "list"]), f"list_{slug}s_handler"),
                (Route([slug, "delete", VariableComponent("id")]), f"delete_{slug}_handler"),
                (Route([slug, "update-one", VariableComponent("id")]), f"update_{slug}_handler"),
                (Route([slug, "update-many"]), f"update_{slug}s_handler"),
                (Route([slug, "duplicate", VariableComponent("id")]), f"duplicate_{slug}_handler"),
            ]
            for route, handler in routes:
                self.routes.append((route, handler))
                self.router.add_route(route, model)

    def generate_rust_router(self):
        routes_code = []
        imports_code = {}
        for route, handler in self.routes:
            slug = route.components[0]
            method = "get" if "get" in handler else "post"
            if slug not in imports_code:
                imports_code[slug] = []
            imports_code[slug].append(handler)
            routes_code.append(f'.route("/{str(route)}", {method}({handler}))')

        imports_code_str = "\n".join(
            [f"use apis::{slug}::{{ {', '.join(handlers)} }};" for slug, handlers in imports_code.items()]
        )
        routes_code_str = "\n    ".join(routes_code)

        rust_router_code = f"""
mod apis;
mod database;
mod exceptions;
mod services;

{imports_code_str}
use axum::{{extract::Extension, routing::get, routing::post, Router, Server}};
use log::{{error, info}};
use services::services::Services;
use std::net::SocketAddr;

#[tokio::main]
async fn main() {{
    // Initialize all services
    let services = Services::init().await;
    info!("Starting Crud Api - version: {{}}", services.version);

    let app = Router::new()
    {routes_code_str}
    .layer(Extension(services.database.get_pool()));

    let server_address: SocketAddr = "0.0.0.0:5555".parse().expect("Invalid address");

    // Log the server address
    info!("Creating server at {{}}", server_address);

    // Separate the binding step
    let server = match Server::try_bind(&server_address) {{
        Ok(server) => server,
        Err(e) => {{
            error!("Couldn't create server: {{}}", e);
            return;
        }}
    }};

    // Run the Axum server
    if let Err(e) = server.serve(app.into_make_service()).await {{
        error!("Server error: {{}}", e);
    }}
}}
"""
        return rust_router_code
