use std::io::prelude::*;
use std::net::{TcpListener, TcpStream};
use std::thread;

fn main() -> std::io::Result<()> {
    // Bind the server to localhost on port 5555
    let listener = TcpListener::bind("0.0.0.0:5555")?;

    println!("Server running on http://0.0.0.0:5555/");

    // Loop over incoming connections
    for stream in listener.incoming() {
        let stream = stream?;

        // Handle each connection in a new thread
        thread::spawn(|| {
            handle_connection(stream).unwrap_or_else(|error| eprintln!("{:?}", error));
        });
    }

    Ok(())
}

fn handle_connection(mut stream: TcpStream) -> std::io::Result<()> {
    // Buffer for reading incoming data
    let mut buffer = [0; 1024];

    // Read the data from the stream
    stream.read(&mut buffer)?;

    // Simple HTTP response with "Hello, World!" message
    let response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, World!";

    // Write the response back to the stream
    stream.write(response.as_bytes())?;
    stream.flush()?;

    Ok(())
}
