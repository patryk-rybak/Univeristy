package calculations;

import calculations.Calculable;

public abstract class Expression implements Calculable {
	public static double sum(Expression ... es) {
		double res = 0.0;
		for (Expression e : es) { res += e.calculate(); }
		return res;
	}

	public static double product(Expression ... es) {
		double res = 1.0;
		for (Expression e : es) { res *= e.calculate(); }
		return res;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj) { return true; }
		else if (obj == null) { return false; }
		Expression other = (Expression) obj;
		return this.calculate() == other.calculate();
	}
}
