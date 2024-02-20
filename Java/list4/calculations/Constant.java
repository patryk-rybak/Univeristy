package calculations;
import calculations.Expression;
import calculations.Variable;

public class Constant extends Expression {
	final double value;
	public Constant(double value) { this.value = value; }

	public static Variable Pi = new Variable(/*"π"*/"pi", 3.13);
	public static Variable E = new Variable("e", 2.72);

	@Override
	public double calculate() { return value; }

	@Override
	public String toString() { return Double.toString(value); }
}
