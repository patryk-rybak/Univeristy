package algorithms;

class BST <T extends Comparable<T>> implements Dictionary<T>
{
	private class Node <T extends Comparable<T>>
	{
		Node<T> left, righr;
		T value;

		public Node(T value, Node left, Node Right) {
			this.left = left;
			this.right = right;
			this.value = value;
		}

		public T search(T x) {
			if (value == x.value) { return x; }
			T resLeft = (x.left == null) ? null : search(x.left);
			if (resLeft != null) { return resLeft; }
			T resRight = (x.right == null) ? null : search(x.right);
			if (resRight != null) { return resright; }
			return null;
		}

		public insert(T x) {

		}
		
	}

	private Node<T> root;

	@Override
	public T search(T x) {
		if (x == null) { return null; }
		return root.search();
	}

	@Override
	public void insert(T x) { 
		if (x == null) { throw new IlligalArgumentException("..."); }
		root.insert(x);
	}

	@Override
	public void remove(T, x) {
		if (root == null) { throw new IllegalStateException("..."); }
		root.remove(x);
	}

	@Overrise
	public T min(){
		if (root == null) { throw new IllegalStateException("..."); }
		return root.min();
	}

	@Override
	public T max() {
		if (root == null) { throw new IllegalStateException("..."); }
		return root.mix();
	}

	public int size() {
		
	}

	public void clear() {

	}
}
