package structures;
import structures.Set;
import structures.Pair;

public class ArraySet implements Set, Cloneable {
	private Pair[] set;
	private int size;
	private int capacity;

	public ArraySet(int initialSize) {
		if (initialSize <= 0) { throw new IllegalArgumentException("..."); }
		set = new Pair[initialSize];
		size = 0;
		capacity = initialSize;
	}


	@Override
	public Pair find(String k) {
		for (Pair p : set) {
			if (p != null && p.key.equals(k)) { return p; } // zwroci chyba wskaznik na Pair w setcie ??
		}
		return null;
	}

	@Override
	public void insert(Pair p) {
		if (size == capacity) { throw new IllegalStateException("..."); }
		boolean flag = true;
		int firstNullIndex = 0;
		for (int i = 0; i < capacity; i++) {
			if (set[i] == null && flag) {
				flag = false;
				firstNullIndex = i;
			} else if (set[i] != null && set[i].key.equals(p.key)) {
				set[i].set_value(p.get_value());
				return;
			}
		}
		set[firstNullIndex] = p;
		size += 1;
	}

	@Override
	public void delete(String k) {
		for (int i = 0; i < capacity; i++) {
			if (set[i] != null && set[i].key.equals(k)) {
				set[i] = null;
				size -= 1;
				return;
			}
		}
	}

	@Override
	public void clean() {
		for (int i = 0; i < capacity; i++) { set[i] = null; }
		size = 0;
	}

	@Override
	public int howMany() { return size; }

	@Override
	public ArraySet clone() {
		try {
			ArraySet clonedSet = (ArraySet) super.clone();
			clonedSet.set = new Pair[this.capacity];
			for (int i = 0; i < this.capacity; i++) {
				if (this.set[i] != null) {
					clonedSet.set[i] = new Pair(this.set[i].key, this.set[i].get_value());
				}
			}
			return clonedSet;
		} catch (CloneNotSupportedException e) {
			return null;
		}
	}


}
