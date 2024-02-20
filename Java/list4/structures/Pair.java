package structures;

public class Pair implements Cloneable, Comparable<Pair> {
	public final String key;
	private double value;

	public Pair(String key, double value) {
		if (key == null || key.length() == 0 || ! isLowerCase(key)) { throw new IllegalArgumentException("..."); }
		this.key = key;
		this.value = value;
	}

	public double get_value() {
		return value;
	}

	public void set_value(double value) {
		this.value = value;
	}

	private boolean isLowerCase(String s) {
		return s.equals(s.toLowerCase());
	}

	@Override
	public String toString() {
		return "(" + key + ", " + value + ")";
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj) { return true; }
		else if (obj == null) { return false; }
		if (getClass() != obj.getClass()) { return false; }
		Pair other = (Pair) obj;
		if (key.equals(other.key)) { return true; }
		return false;
	}

	@Override
	public Object clone() throws CloneNotSupportedException {
		return (Pair) super.clone(); 
	}

	@Override
	public int compareTo(Pair other) {
		return key.compareTo(other.key);
	}
}
