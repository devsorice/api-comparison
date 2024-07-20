pub struct PostgresConfiguration {
    username: String,
    password: String,
    hostname: String,
    port: u16,
    database_name: String,
}

impl PostgresConfiguration {
    pub fn new(
        username: &str,
        password: &str,
        hostname: &str,
        port: u16,
        database_name: &str,
    ) -> Self {
        Self {
            username: username.to_string(),
            password: password.to_string(),
            hostname: hostname.to_string(),
            port,
            database_name: database_name.to_string(),
        }
    }

    pub fn connection_url(&self) -> String {
        format!(
            "postgres://{}:{}@{}:{}/{}",
            self.username, self.password, self.hostname, self.port, self.database_name
        )
    }
}
