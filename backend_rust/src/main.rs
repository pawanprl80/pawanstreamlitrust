use actix_web::{web, App, HttpServer, Responder};
mod websocket;
mod indicators;

async fn ltp_handler(symbol: web::Path<String>) -> impl Responder {
    let ltp = websocket::get_ltp(&symbol).await;
    web::Json(ltp)
}

async fn indicator_handler(symbol: web::Path<String>) -> impl Responder {
    let ltp = websocket::get_ltp(&symbol).await;
    let ind = indicators::calculate_indicators(ltp);
    web::Json(ind)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/ltp/{symbol}", web::get().to(ltp_handler))
            .route("/indicators/{symbol}", web::get().to(indicator_handler))
    })
    .bind(("0.0.0.0",8080))?
    .run()
    .await
}
