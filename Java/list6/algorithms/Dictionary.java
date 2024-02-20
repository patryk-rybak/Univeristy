package algorithms;

public interface Dictionary<T extends Comparable<T>> {
	public boolean search(T x);
	public boolean insert(T x);
	public boolean remove(T x);
	public T min();
	public T max();
}
