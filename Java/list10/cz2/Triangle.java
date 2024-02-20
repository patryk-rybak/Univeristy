public class Triangle {

    private double side1;
    private double side2;
    private double side3;
    private double e = 0.0001;

    public Triangle(double side1, double side2, double side3) {
        if (isValidTriangle(side1, side2, side3)) {
            this.side1 = side1;
            this.side2 = side2;
            this.side3 = side3;
        } else {
		throw new IllegalArgumentException("invalid triangle");
        }
    }

    private boolean isValidTriangle(double side1, double side2, double side3) {
        return (side1 + side2 > side3) && (side1 + side3 > side2) && (side2 + side3 > side1);
    }
    
    public double calculatePerimeter() {
	    return side1 + side2 + side3;
    }

    public boolean isRightTriangle() {
	    double sMax = Math.max(Math.max(side1, side2), side3);
	    return Math.abs(Math.pow(side1, 2) + Math.pow(side2, 2) + Math.pow(side3, 2) - 2 * Math.pow(sMax, 2)) <= e;
    }

    public boolean isEquilateral() {
	    return Math.abs(side1 - side2) < e && Math.abs(side2 - side3) < e && Math.abs(side3 - side1) < e;
    }

    public double calculateArea() {
	    double p = (side1 + side2 + side3)/2;
	    return Math.sqrt(p*(p - side1)*(p - side2)*(p - side3));
    }

    @Override
    public String toString() {
	    return "(" + side1 + ", " + side2 + ", " + side3 + ")";
    }

    public static void main(String[] args) {
        Triangle Triangle1 = new Triangle(3.0, 4.0, 5.0);
	System.out.println(Triangle1.calculatePerimeter());
        Triangle Triangle2 = new Triangle(1.0, 1.0, 3.0);
    }
}

