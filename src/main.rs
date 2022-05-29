extern crate core;

mod esw_server;

use protobuf::Message;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpListener;

use flate2::read::GzDecoder;
use std::io::Read;
use std::env;
use std::error::Error;
use crate::esw_server::{Response, Response_Status};

use std::sync::{Arc};
use dashmap::DashSet;
use std::hash::{Hash, Hasher};
use std::collections::hash_map::{DefaultHasher, RandomState};
use tokio::runtime::Builder;


//Basic server structure taken from: https://medium.com/go-rust/rust-day-7-tokio-simple-tcp-server-32c40f12e79b
#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let addr = env::args()
        .nth(1)
        .unwrap_or_else(|| "[..]:8123".to_string());
    let listener = TcpListener::bind(&addr).await?;
    println!("Listening on: {}", addr);
    let runtime = Builder::new_multi_thread()
        .worker_threads(num_cpus::get())
        .build()
        .unwrap();
    let random = RandomState::new();
    let words: Arc<DashSet<u64>> = Arc::new(DashSet::with_capacity_and_hasher(5000000, random));
    loop {
        let (mut socket, _) = listener.accept().await?;
        let w = words.clone();
        runtime.spawn(async move {
            loop {
                let size_bytes = socket.read_u32().await;
                if size_bytes.is_err() {
                    break;
                }
                let msg_size = size_bytes.unwrap();
                let mut buffer = vec![0u8; msg_size as usize];
                socket.read_exact(&mut buffer).await.expect("Error receiving request datagram");
                let mut request = esw_server::Request::parse_from_bytes(&buffer).unwrap();
                let mut response;
                if request.has_getCount() {
                    response = handle_get_count(&w);
                } else if request.has_postWords() {
                    response = handle_post_words(&w, request.take_postWords().data);
                } else {
                    response = Response::new();
                    response.set_status(Response_Status::ERROR);
                }
                let data = response.write_to_bytes().unwrap();
                socket.write_i32(data.len() as i32).await.expect("Error sending response size");
                socket.write_all(&data).await.expect("Error sending response datagram");
            }
        });
    }
}

fn handle_get_count(words: &DashSet<u64>) -> Response {
    let mut response = esw_server::Response::new();
    response.status = Response_Status::OK;
    response.counter = words.len() as i32;
    words.clear();
    return response;
}

fn handle_post_words(words : &DashSet<u64> , buffer : Vec<u8>) -> Response {
    let mut decoder = GzDecoder::new(&buffer[..]);
    let mut buf = String::new();
    decoder.read_to_string(&mut buf).expect("Decoder did not manage to read incoming data");

    for word in buf.split_whitespace(){
        let mut s = DefaultHasher::new();
        word.hash(&mut s);
        words.insert(s.finish());
    }
    let mut response = esw_server::Response::new();
    response.set_status(Response_Status::OK);
    return response;
}