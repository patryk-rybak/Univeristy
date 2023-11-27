package calculations;
import calculations.Expression;

public class Logarithm extends Expression {
	Expression e;

	public Logarithm(Expression e) { this.e = e; }

	@Override
	public double calculate() { return Math.log(e.calculate()); }

	@Override
	public String toString() { return "log(" + e.toString() + ")"; }
}
