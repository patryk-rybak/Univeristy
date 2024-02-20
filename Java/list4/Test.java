import structures.*;
import calculations.*;

public class Test {
	public static void main(String[] args) {

		Expression x = new Variable("x", 1.618);
		System.out.println("x = 1.618");


		Expression e1 = new Addition(
					new calculations.Number(7.0),
					new Subtraction(
						new Multiplication(
							new calculations.Number(5.0),
							new calculations.Number(3.0)),
						new calculations.Number(1.0)));
		System.out.println();
		System.out.println(e1.toString());
		System.out.println(e1.calculate());


		Expression e2 = new Negation(
					new Multiplication(
						new Subtraction(
							new calculations.Number(2.0),
							x),
						Constant.E));
		System.out.println();
		System.out.println(e2.toString());
		System.out.println(e2.calculate());


		Expression e3 = new Division(
					new Subtraction(
						new Multiplication(
							new calculations.Number(3.0),
							Constant.Pi),
						new calculations.Number(1.0)),
					new Addition(
						x,
						new calculations.Number(5.0)));
		System.out.println();
		System.out.println(e3.toString());
		System.out.println(e3.calculate());


		Expression e4 = new Sine(
					new Division(
						new Multiplication(
							new Addition(
								x,
								new calculations.Number(13.0)),
							Constant.Pi),
						new Subtraction(
							new calculations.Number(1.0),
							x)));
		System.out.println();
		System.out.println(e4.toString());
		System.out.println(e4.calculate());
		// System.out.println(Math.sin(Math.toRadians((1.618 + 13.0)*3.13/(1-1.618))));


		Expression e5 = new Multiplication(
					new Addition(
						new Exponentiation(
							Constant.E,
							new calculations.Number(5.0)),
						x),
					new Logarithm(x));
		System.out.println();
		System.out.println(e5.toString());
		System.out.println(e5.calculate());


		System.out.println();
		System.out.println("Creating set with capacity = 2...");
		ArraySet set = new ArraySet(2);
		System.out.println("Inserting Pair(x, 1.0)...");
		set.insert(new Pair("x", 1.0));
		System.out.println("Finding x...");
		Pair res = set.find("x");
		if (res == null) { System.out.println("Not found"); }
		else { System.out.println("Found: " + res); }
		System.out.println("Deleting x...");
		set.delete("x");
		System.out.println("Finding x...");
		res = set.find("x");
		if (res == null) { System.out.println("Not found"); }
		else { System.out.println("Found: " + res); }
		System.out.println("Inserting Pair(y, 2.0)...");
		set.insert(new Pair("y", 2.0));
		System.out.println("Finding y...");
		res = set.find("y");
		if (res == null) { System.out.println("Not found"); }
		else { System.out.println("Found: " + res); }


		System.out.println();
		System.out.println("Copying set...");
		ArraySet set2 = set.clone();
		System.out.println("Finding y in new set...");
		res = set2.find("y");
		if (res == null) { System.out.println("Not found"); }
		else { System.out.println("Found: " + res); }
		System.out.println("Cleaning new set...");
		set2.clean();
		System.out.println("Finding y in old set...");
		res = set.find("y");
		if (res == null) { System.out.println("Not found"); }
		else { System.out.println("Found: " + res); }
		System.out.println("Finding y in new set...");
		res = set2.find("y");
		if (res == null) { System.out.println("Not found"); }
		else { System.out.println("Found: " + res); }

		System.out.println();
		System.out.println(Expression.sum(new calculations.Number(5.0), new calculations.Number(6.0)));
		System.out.println(Expression.product(new calculations.Number(5.0), new calculations.Number(6.0)));
		
	}
}
