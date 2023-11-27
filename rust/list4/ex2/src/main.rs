use std::ops::{Add, Sub, Mul};

#[derive(Debug, Clone, Copy)]
struct Complex(f64, f64);

impl PartialEq for Complex {
    fn eq(&self, other: &Self) -> bool {
        self.0 == other.0 && self.1 == other.1
    }
}

impl Add for Complex {
	type Output = Self;
	
	fn add(self, other: Self) -> Self {
		Self(self.0 + other.0, self.1 + other.1)
	}
}

impl Sub for Complex {
	type Output = Self;

	fn sub(self, other: Self) -> Self {
		Self(self.0 - other.0, self.1 - other.1)
	}
}

impl Mul for Complex {
	type Output = Self;

	fn mul(self, other: Self) -> Self {
		Self(self.0 * other.0 - self.1 * other.1, self.0 * other.1 + self.1 * other.0)
	}
}

impl Complex {
    fn distance(&self) -> f64 {
        (self.0 * self.0 + self.1 + self.1).sqrt()
    }
}

#[test]
fn test_add() {
	let temp1 = Complex(1.0, 2.0);
	let temp2 = Complex(1.0, 2.0);
        let res = temp1 + temp2;
        assert_eq!(temp1, Complex(1.0, 2.0));
        assert_eq!(temp2, Complex(1.0, 2.0));
        assert_eq!(res, Complex(2.0, 4.0));
}

#[test]
fn test_sub() {
	let temp1 = Complex(1.0, 2.0);
	let temp2 = Complex(1.0, 2.0);
        let res = temp1 - temp2;
        assert_eq!(temp1, Complex(1.0, 2.0));
        assert_eq!(temp2, Complex(1.0, 2.0));
        assert_eq!(res, Complex(0.0, 0.0));
}

#[test]
fn test_mul() {
	let temp1 = Complex(1.0, 2.0);
	let temp2 = Complex(1.0, 2.0);
        let res = temp1 * temp2;
        assert_eq!(temp1, Complex(1.0, 2.0));
        assert_eq!(temp2, Complex(1.0, 2.0));
        assert_eq!(res, Complex(-3.0, 4.0));
}

#[test]
fn dest_distance() {
	let temp = Complex(1.0, 2.0);
        let res = temp.distance();
        assert_eq!((res * 100.0).round() / 100.0, 2.24);
}

