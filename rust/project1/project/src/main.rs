use std::ops::{Add, Sub, Mul};

#[derive(Debug, Clone, Copy)]
pub struct Complex(pub f64, pub f64);

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
    pub fn distance(&self) -> f64 {
        (self.0 * self.0 + self.1 * self.1).sqrt()
    }
}


use std::fs::File;
use std::io::Write;

#[derive(Clone, Debug)]
pub struct Pixel {
    r: u8,
    g: u8,
    b: u8,
}

impl Pixel {
    pub fn new(r: u8, g: u8, b: u8) -> Self {
        Self { r, g, b }
    }
}

pub struct Image {
    width: usize,
    height: usize,
    pixels: Vec<Pixel>,
    magic_number: String,
}

impl Image {
    pub fn new(width: usize, height: usize) -> Self {
        Self {
            width: width,
            height: height,
            pixels: vec![Pixel::new(255, 255, 255); width * height],
            magic_number: String::from("P3"),
        }
    }

    pub fn set_pixel(&mut self, row: usize, column: usize, pixel: Pixel) {
        self.pixels[self.width * row + column] = pixel;
    }

    pub fn save_ppm(&self, file_name: &str) -> Result<(), std::io::Error> {
        let mut file = File::create(file_name)?;
        write!(file, "{}\n{} {}\n255\n", self.magic_number, self.width, self.height)?;
        for pixel in &self.pixels {
            write!(file, "{} {} {}\n", pixel.r, pixel.g, pixel.b)?;
        }
        Ok(())
    }
}

struct MandelbrotSet {
    lower_bound: Complex,
    upper_bound: Complex,
}

impl MandelbrotSet {

    fn new(lower_bound: Complex, upper_bound: Complex) -> Self {
        Self { lower_bound, upper_bound }
    }

    fn deafult() -> Self {
        Self { lower_bound: Complex(-2., -1.12), upper_bound: Complex(0.47, 1.12) }
    }

    fn count_iterations(constant: Complex, max_iteration: usize) -> usize {
        let mut z = Complex(0.0, 0.0);
        let mut iteration = 0;
        while z.distance() < 2.0 && iteration < max_iteration {
            z =  z * z + constant;
            iteration += 1;
        }
        iteration
    }

    fn map_to_color(iteration: usize, max_iteration: usize) -> Pixel {
        let intensity = (iteration as f64 / max_iteration as f64 * 255.0) as u8;
        Pixel::new(intensity, intensity, intensity)
    }

    fn render(&self, width: usize, height: usize, max_iteration: usize) -> Image {
        let mut img = Image::new(width, height);
        for y in 0..height {
            for x in 0..width {
                let r = (x as f64 / width as f64) * (self.upper_bound.0 - self.lower_bound.0) + self.lower_bound.0;
                let i = (y as f64 / height as f64) * (self.upper_bound.1 - self.lower_bound.1) + self.lower_bound.1;
                let c = Complex(r, i);
                let iterations = Self::count_iterations(c, max_iteration);
                let color = Self::map_to_color(iterations, max_iteration);

                img.set_pixel(y, x, color);
            }
        }
        img
    }
}

use std::f64::consts::E;

fn main() {
    let max_iter = 100;

    let fractal1 = MandelbrotSet::new(Complex(-0.76, 0.12), Complex(-0.78, 0.14));
    let image1 = fractal1.render(3840, 2160, max_iter);
    if let Err(err) = image1.save_ppm("mandelbrot1.ppm") {
        eprintln!("error saving image: {}", err);
    }

    let fractal2 = MandelbrotSet::deafult();
    let image2 = fractal2.render(3840, 2160, max_iter);

    if let Err(err) = image2.save_ppm("mandelbrot2.ppm") {
        eprintln!("Error saving image: {}", err);
    }

    let fractal1 = MandelbrotSet::new(Complex(-E/7.0 - 0.5, E/20.0 + 0.5), Complex(-E/7.0 + 0.5, E/20.0 + 0.5));
    let image1 = fractal1.render(3840, 2160, max_iter);
    if let Err(err) = image1.save_ppm("mandelbrot3.ppm") {
        eprintln!("error saving image: {}", err);
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
fn test_distance() {
	let temp = Complex(1.0, 2.0);
        let res = temp.distance();
        assert_eq!((res * 100.0).round() / 100.0, 2.24);
}

#[test]
fn test_eq() {
	let temp1 = Complex(1.0, 2.0);
	let temp2 = Complex(1.0, 2.0);
        assert_eq!(temp1 == temp2, true);
}

/* #[test]
fn test_render1() {
        
    let fractal = MandelbrotSet::deafult();
    let max_iter = 100;
    let image = fractal.render(1980, 1080, max_iter);

    if let Err(err) = image.save_ppm("mandelbrot1.ppm") {
        eprintln!("Error saving image: {}", err);
    }
}

#[test]
fn test_render2() {
        
    let fractal = MandelbrotSet::new(Complex(-0.80, 0.10), Complex(-0.70, 0.20));
    let max_iter = 100;
    let image = fractal.render(1980, 1080, max_iter);

    if let Err(err) = image.save_ppm("mandelbrot2.ppm") {
        eprintln!("error saving image: {}", err);
    }
}
*/
