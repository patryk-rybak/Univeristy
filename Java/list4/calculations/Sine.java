package calculations;
import calculations.Expression;

public class Sine extends Expression {
	Expression e;

	public Sine(Expression e) { this.e = e; }

	@Override
	public double calculate() { return Math.sin(Math.toRadians(e.calculate())); }

	@Override
	public String toString() { return "sin(" + e.toString() + ")"; }
}
