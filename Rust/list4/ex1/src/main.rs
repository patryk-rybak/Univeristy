use std::fs::File;
use std::io::Write;

#[derive(Clone, Debug)]
struct Pixel {
			r: u8,
		   g: u8,
		   b: u8,
}

impl Pixel {
		fn new(r: u8, g: u8, b: u8) -> Self {
				Self { r, g, b }
		}
}

struct Image {
				width: usize,
			   height: usize,
			   pixels: Vec<Pixel>,
			   magic_number: String,
}

impl Image {
		fn new(width: usize, height: usize) -> Self {
				Self {
				width: width,
			   height: height,
			   pixels: vec![Pixel::new(255, 255, 255); width * height],
			   magic_number: String::from("P3"),
				}
		}

		fn set_pixel(&mut self, row: usize, column: usize, pixel: Pixel) {
				self.pixels[self.width * row + column] = pixel;
		}

		fn save_ppm(&self, file_name: &str) -> Result<(), std::io::Error> {
				let mut file = File::create(file_name)?;
				write!(file, "{}\n{} {}\n255\n", self.magic_number, self.width, self.height)?;
				for pixel in &self.pixels {
						write!(file, "{} {} {}\n", pixel.r, pixel.g, pixel.b)?;
				}
				Ok(())
		}
}

fn main() {
	let mut black_image = Image::new(255, 255);
	black_image.set_pixel(5, 5, Pixel::new(0, 0, 0));
	match black_image.save_ppm("dupa") {
	Err(err) => eprintln!("blad {}", err),
	Ok(_) => println!("git"),

}
}
