package calculations;
import calculations.Expression;

public class Exponentiation extends Expression {
	Expression eL;
	Expression eR;

	public Exponentiation(Expression eL, Expression eR) { this.eL = eL; this.eR = eR; }

	@Override
	public double calculate() { return Math.pow(eL.calculate(), eR.calculate()); }

	@Override
	public String toString() { return "(" + eL.toString() + ")^(" + eR.toString() + ")"; }
}
