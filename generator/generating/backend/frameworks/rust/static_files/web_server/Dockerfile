FROM rust:1.80.1-alpine3.20 as builder

WORKDIR /app

# ## Install build dependencies
RUN apk add upx

## Copy source code
COPY Cargo.toml Cargo.lock ./
COPY src ./src

## Build release binary
RUN cargo build --release --target x86_64-unknown-linux-musl
## Pack release binary with UPX (optional)
RUN upx --best --lzma /app/target/x86_64-unknown-linux-musl/release/crud-api

# Runtime
FROM scratch as server

## Copy release binary from builder
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/crud-api /app

ENTRYPOINT ["/app"]
