use serde::Serialize;

#[derive(Serialize)]
pub struct Indicators {
    pub supertrend: bool,
    pub macd: bool,
    pub macd_line_positive: bool,
    pub rsi_over70: bool,
    pub upperband_rising: bool,
    pub midband_cross: bool,
    pub squeeze_slope: bool,
    pub spot_atm: bool,
    pub diamond: bool,
}

pub fn calculate_indicators(ltp: f64) -> Indicators {
    let supertrend=true;
    let macd=true;
    let macd_line_positive=true;
    let rsi_over70=true;
    let upperband_rising=true;
    let midband_cross=true;
    let squeeze_slope=true;
    let spot_atm=true;
    let diamond = supertrend && macd && macd_line_positive && rsi_over70 &&
                  upperband_rising && midband_cross && squeeze_slope && spot_atm;

    Indicators {supertrend, macd, macd_line_positive, rsi_over70, upperband_rising, midband_cross, squeeze_slope, spot_atm, diamond}
}
