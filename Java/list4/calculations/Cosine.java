package calculations;
import calculations.Expression;

public class Cosine extends Expression {
	Expression e;

	public Cosine(Expression e) { this.e = e; }

	@Override
	public double calculate() { return Math.cos(Math.toRadians(e.calculate())); }

	@Override
	public String toString() { return "cos(" + e.toString() + ")"; }
}
