### Esw server - Rust
Repository is located here: https://github.com/japawBlob/sem-esw-rust

This is basic server build on tokio (https://tokio.rs/), which uses dashSet for storing words.

For building and running use following commands:

`cargo build` <br/>
and <br/>
`cargo run`<br/>

or 

`cargo build --release` <br/>
and <br/>
`cargo run --release` <br/>
for optimized version.

The server listens to port 8123 by default, but can accept one argument in form of <br/>
`cargo run [..]:<<port>>` <br/>
which will specify the port if <<port>> would be replaced with desired number.

For running on ritchie I used nix-os using nixpkgs (https://nixos.wiki/wiki/Rust) with unstable build.
I wasn't able to achieve satisfactory result on ESW server tester, since last few days ritchie stood at 100% usage and 
my results were all over the place. 
EDIT: On monday morning 30.5. ritchie was without load. I tested my program. Added optimazion flags and program runs as expected.

Sources: <br/>
For basics of dashSet: https://docs.rs/dashmap/latest/dashmap/struct.DashSet.html <br/>
Basic tokio skeleton for project: https://medium.com/go-rust/rust-day-7-tokio-simple-tcp-server-32c40f12e79b <br/>
Tokio runtime: https://docs.rs/tokio/1.4.0/tokio/runtime/struct.Builder.html <br/>
Decoding gzip message: https://docs.rs/flate2/1.0.22/flate2/read/struct.GzDecoder.html <br/>
Hashing entries: https://doc.rust-lang.org/std/hash/index.html
