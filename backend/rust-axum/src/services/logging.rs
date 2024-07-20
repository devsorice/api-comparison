use env_logger::{Builder, Env};
use log::LevelFilter;
use std::io::Write; // Import the Write trait

pub struct Logger;

impl Logger {
    pub fn init() {
        Builder::from_env(Env::default().default_filter_or("info"))
            .format(|buf, record| {
                writeln!(
                    buf,
                    "{} [{}] {}:{} - {}",
                    chrono::Local::now().format("%Y-%m-%d %H:%M:%S"),
                    record.level(),
                    record.file().unwrap_or("unknown"),
                    record.line().unwrap_or(0),
                    record.args()
                )
            })
            .filter(None, LevelFilter::Info)
            .init();
    }
}
