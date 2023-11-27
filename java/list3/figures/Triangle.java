package figures;
import java.util.Objects;

public class Triangle {

	private Point p1;
	private Point p2;
	private Point p3;

	public Triangle() { this(new Point(0, 0), new Point(0, 1), new Point(1, 0)); }

	public Triangle(Point p1, Point p2, Point p3) {
		if ((new StraightLine(p1, p2)).containsPoint(p3)) { throw new IllegalArgumentException("..."); } 
		this.p1 = p1;
		this.p2 = p2;
		this.p3 = p3;
	}

	public void move(Vector v) {
		p1.move(v);
		p2.move(v);
		p3.move(v);
	}

	public void rotate(Point p, double angle) {
		p1.rotate(p, angle);	
		p2.rotate(p, angle);	
		p3.rotate(p, angle);	
	}

	public void reflect(StraightLine l) {
		p1.reflect(l);
		p2.reflect(l);
		p3.reflect(l);
	}

	@Override
	public String toString() {
		return "((" + p1.getX() + ", " + p1.getY() + "), (" + p2.getX() + ", " + p2.getY() + "), (" + p3.getX() + ", " + p3.getY() + "))";
	}


}
