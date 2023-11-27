package calculations;
import calculations.Expression;

public class Reciprocal extends Expression {
	Expression e;

	public Reciprocal(Expression e) { this.e = e; }

	@Override
	public double calculate() { return 1 / e.calculate(); }

	@Override
	public String toString() { return "(1 / " + e.toString() + ")"; }
}
