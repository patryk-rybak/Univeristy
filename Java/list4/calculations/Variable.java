package calculations;

import calculations.Expression;
import structures.*;

public class Variable extends Expression {
	String key;
	public Variable(String key, double value) {
		this.key = key;
		Variable.variables.insert(new Pair(key, value));
	}

	@Override
	public double calculate() { return variables.find(key).get_value(); }

	@Override
	public String toString() { return key; }

	static final ArraySet variables = new ArraySet(100);


}

