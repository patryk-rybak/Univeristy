package algorithms;

public interface Dictionary<T extends Comparable<T>> {
	public boolean search(T x);
	public void insert(T x);
	public void remove(T x);
	public T min();
	public T max();
}
