package figures;

import java.util.Objects;

public class LineSegment {

	private Point p1;
	private Point p2;

	public LineSegment() { this(new Point(0, 0), new Point(0, 1)); }

	public LineSegment(Point p1, Point p2) {
		if (Objects.equals(p1, p2)) { throw new IllegalArgumentException("..."); }
		this.p1 = p1;
		this.p2 = p2;
	}

	public void move(Vector v) {
		p1.move(v);
		p2.move(v);
	}

	public void rotate(Point p, double angle) {
		p1.rotate(p, angle);	
		p2.rotate(p, angle);	
	}

	public void reflect(StraightLine l) {
		p1.reflect(l);
		p2.reflect(l);
	}

	@Override
	public String toString() {
		return "((" + p1.getX() + ", " + p1.getY() + "), (" + p2.getX() + ", " + p2.getY() + "))";
	}
}

