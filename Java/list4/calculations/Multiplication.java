package calculations;
import calculations.Expression;

public class Multiplication extends Expression {
	Expression eL;
	Expression eR;

	public Multiplication(Expression eL, Expression eR) { this.eL = eL; this.eR = eR; }
	@Override
	public double calculate() { return eL.calculate() * eR.calculate(); }

	@Override
	public String toString() { return "(" + eL.toString() + " * " + eR.toString() + ")"; }
}
