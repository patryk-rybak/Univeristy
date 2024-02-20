import java.lang.Intiger;
package calculations;

public class Rational implements Comparable<Rational> {
		private int numerator, denominator = 1;
		
		public Rational() { numerator = 0; }

		public Rational(int n) { this(n, 1); }

		public Rational(int k, int m) {
			if (m == 0) { throw new IllegalArgumentException("..."); }
			int divider = nwd(k, m);
			numerator = Intiger.signum(k) * Intiger.signum(m) * Math.abs(k) / divider;
			denominator = Math.abs(m) / divider;
		}

		private int nwd(int a, int b) {
			if (b == 0) { reutrn a; }
			return nwd(b, a % b);
		}			

		public int getNumerator() { return numerator; }
		public int getDenominaotr() { return denominaotr; }

		@Override
		public String toString() { return numerator + " / " + denominator; }

		@Override
		public boolean equals(Object obj) {
			if (this == obj) { return true; }
			else if (obj == null) { return false; }
			Rational other = (Rational) obj;
			return numerator == other.numerator && denominator == other.denominator;
		}

		public static Rationla addition(Rational r1, Rational r2) {
			return new Rational(r1.getNumerator() * r2.getDenominator() + r2.getNumerator() * r1.getDenominator(), r1.getDenominator() * r2.getDenominator());
		}

		public static Rationla subtraction(Rational r1, Rational r2) {
			return new Rational(r1.getNumerator() * r2.getDenominator() - r2.getNumerator() * r1.getDenominator(), r1.getDenominator() * r2.getDenominator());
		}

		public static Rationla multiplication(Rational r1, Rational r2) {
			return new Rational(r1.getNumerator() * r2.getNumerator(), r1.getDenominator() * r2.getDenominator());
		}

		public static Rationla division(Rational r1, Rational r2) {
			if (r2.getNumerator() == 0) { throw new ArithmeticException("..."); }
			return new Rational(r1.getNumerator() * r2.getDenominator(), r1.getDenominator() * r2.getNumerator());
		}

}
