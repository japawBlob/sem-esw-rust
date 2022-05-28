extern crate protoc_rust;

fn main() {
    protobuf_codegen_pure::Codegen::new()
        .out_dir("src/")
        .inputs(&["proto/esw_server.proto"])
        .include("proto")
        .run()
        .expect("Codegen failed.");
}