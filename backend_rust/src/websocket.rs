
use std::collections::HashMap;
use tokio::sync::RwLock;
use lazy_static::lazy_static;
use serde::Serialize;

lazy_static! {
    pub static ref LTP_STORE: RwLock<HashMap<String,f64>> = RwLock::new(HashMap::new());
}

#[derive(Serialize)]
pub struct LtpResponse {
    pub symbol: String,
    pub ltp: f64,
}

pub async fn update_ltp(symbol: &str, price: f64) {
    let mut store = LTP_STORE.write().await;
    store.insert(symbol.to_string(), price);
}

pub async fn get_ltp(symbol: &str) -> f64 {
    let store = LTP_STORE.read().await;
    *store.get(symbol).unwrap_or(&0.0)
}
