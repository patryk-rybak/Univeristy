package figures;
import java.util.Objects;

public class StraightLine {

	private final double A;
	private final double B;
	private final double C;

	public StraightLine() { this(1, -1, 0); }

	public StraightLine(double A, double B, double C) {
		this.A = A;
		this.B = B;
		this.C = C;
	}

	public StraightLine(Point p1, Point p2) {
		if (Objects.equals(p1, p2)) { throw new IllegalArgumentException("..."); }
		this.A = p2.getY() - p1.getY();
		this.B = p1.getX() - p2.getX();
		this.C = p2.getX() * p1.getY() - p1.getX() * p2.getY();
	}

	public double getA() { return A; }

	public double getB() { return B; }

	public double getC() { return C; }

	public boolean containsPoint(Point p) { return A * p.getX() + B * p.getY() + C == 0; }

	public static StraightLine move(StraightLine l, Vector v) { return new StraightLine(l.getA(), l.getB(), l.getC() + l.getA() * v.dx + l.getB() * v.dy); }

	public static boolean areParallel(StraightLine l1, StraightLine l2) { return l1.A * l2.B - l2.A * l1.B == 0; }

	public static boolean arePerpendicular(StraightLine l1, StraightLine l2) { return l1.A * l2.A + l1.B * l2.B == 0; }

	public static Point intersectionPoint(StraightLine l1, StraightLine l2) {
		if (StraightLine.areParallel(l1, l2)) { throw new IllegalArgumentException("..."); }
		double temp = l1.getA() * l2.getB() - l2.getA() * l1.getB();
		return new Point((l1.getB() * l2.getC() - l2.getB() * l1.getC()) / temp, (l2.getA() * l1.getC() - l1.getA() * l2.getC()) / temp);
	}

	@Override
	public String toString() {
		return A + "x + " + B + "y + " + C + " = 0";
	}
}
