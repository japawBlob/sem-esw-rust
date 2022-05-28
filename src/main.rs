mod esw_server;

use protobuf::Message;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpListener;

use std::env;
use std::error::Error;
use crate::esw_server::{Response, Response_Status};


//Basic server taken from: https://medium.com/go-rust/rust-day-7-tokio-simple-tcp-server-32c40f12e79b
#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let addr = env::args()
        .nth(1)
        .unwrap_or_else(|| "127.0.0.1:8123".to_string());
    let listener = TcpListener::bind(&addr).await?;
    println!("Listening on: {}", addr);

    loop {
        let (mut socket, _) = listener.accept().await?;
        tokio::spawn(async move {
            let mut buf = vec![0; 1024];
            loop {
                let size_bytes = socket.read_u32().await;
                if size_bytes.is_err() {
                    break;
                }
                let msg_size = size_bytes.unwrap();
                println!("Size: {}", msg_size);
                let mut buffer = vec![0u8; msg_size as usize];
                socket.read_exact(&mut buffer).await.expect("TODO: panic message");

                let requset = esw_server::Request::parse_from_bytes(&buffer).unwrap();

                let mut response = esw_server::Response::new();
                response.status = Response_Status::OK;

                let data = response.write_to_bytes().unwrap();
                socket.write_u32(data.len() as u32).await.expect("TODO: panic message");
                socket.write_all(&data).await.expect("TODO: panic message");
            }

        });
    }
}
