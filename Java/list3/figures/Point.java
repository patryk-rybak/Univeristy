package figures;
import java.lang.Math;

public class Point {

	private double x;
	private double y;

	public Point() { this(0, 0); }

	public Point(double x, double y) {
		this.x = x;
		this.y = y;
	}

	public double getX() { return x; }

	public double getY() { return y; }

	public void move(Vector v) {
		x = x + v.dx;
		y = y + v.dy;
	}

	public void rotate(Point p, double angle) {
		angle = Math.toRadians(angle);
		double temp = x;
		x = Math.cos(angle) * (temp - p.getX()) - Math.sin(angle) * (y - p.getY()) + p.getX();
		y = Math.sin(angle) * (temp - p.getX()) + Math.cos(angle) * (y - p.getY()) + p.getY();
	}

	public void reflect(StraightLine l) { 
		double temp =  x;
		x = (x * (l.getB() * l.getB() - l.getA() * l.getA()) - 2 * l.getA() * (l.getB() * y + l.getC())) / (l.getB() * l.getB() + l.getA() * l.getA());
		y = (y * (l.getA() * l.getA() - l.getB() * l.getB()) - 2 * l.getB() * (l.getA() * temp + l.getC())) / (l.getB() * l.getB() + l.getA() * l.getA());
	}

	@Override
	public String toString() {
		return "(" + x + ", " + y + ")";
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj) { return true; }
		else if (obj == null) { return false; }
		if (getClass() != obj.getClass()) { return false; }
		Point other = (Point) obj;
		if (x == other.x && y == other.y) { return true; } 
		return false;
	}
}
