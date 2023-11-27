package calculations;
import calculations.Expression;

public class Negation extends Expression {
	Expression e;

	public Negation(Expression e) { this.e = e; }

	@Override
	public double calculate() { return -e.calculate(); }

	@Override
	public String toString() { return "~ " + e.toString(); }
}
