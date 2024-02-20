fn main() {
    returns_expected();
}

fn square_area_to_circle(size:f64) -> f64 {
    (size.sqrt() / 2.0).powi(2) * std::f64::consts::PI
}

fn assert_close(a:f64, b:f64, epsilon:f64) {
    assert!( (a-b).abs() < epsilon, "Expected: {}, got: {}",b,a);
}

fn returns_expected() {
    assert_close(square_area_to_circle(9.0), 7.0685834705770345, 1e-8);
    assert_close(square_area_to_circle(20.0), 15.70796326794897, 1e-8);
    assert_close(square_area_to_circle(4.0),  3.1415926535897932384626433832795028841971693993751058209749445923, 1e-8);
    assert_close(square_area_to_circle(64.0), 50.265482457, 1e-8);
    assert_close(square_area_to_circle(16.0), 12.566370614, 1e-8);
}
