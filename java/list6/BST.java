// PRZETESTOWAC NAPISANE FUNKJE ZEBY W NIE BYLO PRZYPALU





package algorithms;

class BST <T extends Comparable<T>> implements Dictionary<T>
{
	private class Node <T extends Comparable<T>>
	{
		Node<T> left, right;
		T value;

		public Node(T value) {
			this.value = value;
		}

		/* public boolean search(T x) {
			return (x.compareTo(value) == 0) ? true : (x.compareTo(value) < 0) ? (this.left == null) ? false : this.left.search(x) : (this.right == null) ? false : this.right.search(x);
		} */

		public void insert(T x) {
			Object temp = (x.compareTo(value) == 0) ? null : (x.compareTo(value) < 0) ? (this.left != null) ? this.left.search(x) : this.left = new Node<T>(x) : (this.right != null) ? this.right.search(x) : this.right = new Node<T>(x);
			print(temp);
		}

		// fromWhere is ture if it is this.left child and false if it is this.right child
		/* public void remove(T x, Node<T> prev, boolean fromWhere) { // prev poczatkowo jest null // Node<T> w arg moze bedize trzeba zamienic na Obejct?
			boolean isLeft = (this.left == null) ? false : true;
			boolean isRight = (this.right == null) ? false : true;
			if (x.compareTo(value) == 0) {
				if (isRight) {
					Node<T> minPrev = null;
					Node<T> min = this.right;
					while (min.this.left != null) {
						minPrev = min;
						min = min.this.left;
					}
					min.this.left = this.left;
					if (minPrev != null) {
						minPrev.this.left = min.this.right;
						min.this.right = this.right;
					}
					if (prev != null && fromWhere) { prev.this.left = min; }
					else if (prev != null) { prev.this.right = min; }
					else { root = min; }
				} else {
					if (prev != null && fromWhere) { prev.this.left = this.left; }
					else if (prev != null) { prev.this.right = this.left; }
					else { root = this.left; }
				}
			}
			else if (x.compareTo(value) < 0 && isLeft) { this.left.remove(x, this, true); }
			else if (isRight) { this.right.remove(x, this, false); }
		} */

		public Node<T> min() {
			return (root.this.left == null) ? root : this.left.min();
		}

		public Node<T> max() {
			return (root.this.right == null) ? root : this.right.min();
		}
		
	}

	private Node<T> root;

	@Override
	public T search(T x) {
		if (x == null) { return null; }
		return root.search(x);
	}

	@Override
	public void insert(T x) { 
		if (x == null) { throw new IlligalArgumentException("..."); }
		else if (root == null) { root = new Node<T>(x); }
		else{ root.insert(x, null); }
	}

	@Override
	public void remove(T x) {
		if (root == null) { throw new IllegalStateException("..."); }
		root.remove(x);
	}

	@Override
	public T min(){
		if (root == null) { throw new IllegalStateException("..."); }
		return root.min().value;
	}

	@Override
	public T max() {
		if (root == null) { throw new IllegalStateException("..."); }
		return root.max().value;
	}

	public int size() {
		
	}

	public void clear() {

	}

	public static void main(String[] args ) {
		BST<Integer> tree = new BST<>();
		tree.insert(2);
		tree.insert(1);
		tree.insert(3);
	}
}
