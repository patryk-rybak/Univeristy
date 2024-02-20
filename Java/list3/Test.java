import figures.*;

public class Test {

	public static void main(String[] args) {

		System.out.println("\n\nTesting Point class:\n");
		System.out.println("Creating Point instance...");
		Point p = new Point(1, 1);
		System.out.println(p);
		System.out.println();
		System.out.println("Moving point (1, 1) by the vector [2, 3]...");
		p.move(new Vector(2, 3));
		System.out.println(p);
		System.out.println();
		System.out.println("Rotating the point (3, 4) by the 180 degree angle about the (1, 2)...");
		p.rotate(new Point(1, 2), 180);
		System.out.println(p);
		System.out.println();
		System.out.println("Reflecting the point (-1, 4) over the x - y + 4 = 0...");
		Point temp = new Point(-1, 4);
		temp.reflect(new StraightLine(1, -1, 4));
		System.out.println(temp);
		System.out.println();

		System.out.println("\nTesting LineSegment class:\n");
		System.out.println("Creating LineSegment instance...");
		LineSegment ls = new LineSegment(new Point(1, 1), new Point(1, 2));
		System.out.println(ls);
		System.out.println();
		System.out.println("Moving line segment by the vector [2, 3]...");
		ls.move(new Vector(2, 3));
		System.out.println(ls);
		System.out.println();
		System.out.println("Rotating the line segmnet by the 90 degree angle about the (1, 2)...");
		ls.rotate(new Point(1, 2), 90);
		System.out.println(ls);
		System.out.println();
		System.out.println("Reflecting the line segment over the 2x + 2y + 1 = 0...");
		ls.reflect(new StraightLine(2, 2, 1));
		System.out.println(ls);
		System.out.println();

		System.out.println("\nTesting Triangle class:\n");
		System.out.println("Creating Triangle instance...");
		Triangle t = new Triangle();
		System.out.println(t);
		System.out.println();
		System.out.println("Moving triangle by the vector [1, 2]...");
		t.move(new Vector(1, 2));
		System.out.println(t);
		System.out.println();
		System.out.println("Rotating the triangle by the 90 degree angle about the (1, 2)...");
		t.rotate(new Point(1, 2), 90);
		System.out.println(t);
		System.out.println();
		System.out.println("Reflecting the triangle over the 2x + 2y + 1 = 0...");
		t.reflect(new StraightLine(2, 2, 1));
		System.out.println(t);
		System.out.println();

		System.out.println("\nTesting StraightLine class:\n");
		System.out.println("Creating StraightLine instance...");
		StraightLine sl = new StraightLine(2, 1, 2);
		System.out.println(sl);
		System.out.println();
		System.out.println("Moving straight line by the vector [1, 2]...");
		StraightLine sl2 = StraightLine.move(sl, new Vector(1, 2));
		System.out.println(sl2);
		System.out.println();
		System.out.println("Are " + sl + " and " + sl2 + " parallel...");
		System.out.println(StraightLine.areParallel(sl, sl2));
		System.out.println();
		System.out.println("Are " + sl + " and " + sl2 + " perpendicular...");
		System.out.println(StraightLine.arePerpendicular(sl, sl2));
		System.out.println();
		System.out.println("Finding intersection point of " + sl + " and 3x + 4y = 0...");
		System.out.println(StraightLine.intersectionPoint(sl, new StraightLine(3, 4, 0)));
		System.out.println();

		System.out.println("\nTesting Vector class:\n");
		System.out.println("Creating Vector instance...");
		Vector v = new Vector(2, 3);
		System.out.println(v);
		System.out.println();
		System.out.println("Creating Vector instance...");
		Vector v2 = new Vector(4, 5);
		System.out.println(v);
		System.out.println();
		System.out.println("Adding vectors " + v + " and " + v2 + " ...");
		System.out.println(Vector.add(v, v2));
		System.out.println();


		System.out.println("\nChecking the equality of points (1, 1) and (1, 1)...");
		Point p1 = new Point(1.0 / 3.0, 1.0 / 3.0);
		p1.move(new Vector(1.0 / 3.0, 1.0 / 3.0));
		p1.move(new Vector(1.0 / 3.0, 1.0 / 3.0));
		Point p2 = new Point(1, 1);
		System.out.println(p1.equals(p2));
	}

}

