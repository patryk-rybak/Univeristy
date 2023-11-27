package figures;

public class Vector {

	public final double dx;
	public final double dy;

	public Vector() { this(0, 0); }

	public Vector(double dx, double dy) {
		this.dx = dx;
		this.dy = dy;
	}

	public static Vector add(Vector v1, Vector v2) {
		return new Vector(v1.dx + v2.dx, v1.dy + v2.dy);
	}

	@Override
	public String toString() {
		return "[" + dx + ", " + dy + "]";
	}
}
