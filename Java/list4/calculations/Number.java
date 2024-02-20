package calculations;
import calculations.Expression;

public class Number extends Expression {
	double value;
	public Number(double value) { this.value = value; }

	@Override
	public double calculate() { return value; }

	@Override
	public String toString() { return Double.toString(value); }
}
