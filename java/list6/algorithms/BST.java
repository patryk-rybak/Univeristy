package algorithms;

class BST <T extends Comparable<T>> implements Dictionary<T>
{
	private class Node
	{
		Node left, right;
		T value;

		public Node(T value) {
			this.value = value;
		}


		public boolean search(T x) {
			return (x.compareTo(value) == 0) ? true : (x.compareTo(value) < 0) ? (left == null) ? false : left.search(x) : (right == null) ? false : right.search(x);
		}

		// fromWhere is ture if it is this.left child and false if it is this.right child
		public boolean remove(T x, Node prev, boolean fromWhere) { 
			boolean isLeft = (left == null) ? false : true;
			boolean isRight = (right == null) ? false : true;
			if (x.compareTo(value) == 0) {
				if (isRight) {
					Node minPrev = null;
					Node min = right;
					while (min.left != null) {
						minPrev = min;
						min = min.left;
					}
					min.left = left;
					if (minPrev != null) {
						minPrev.left = min.right;
						min.right = right;
					}
					if (prev != null && fromWhere) prev.left = min;
					else if (prev != null) prev.right = min;
					else root = min;
					return true;
				} else {
					if (prev != null && fromWhere) prev.left = left;
					else if (prev != null) prev.right = left;
					else root = left;
					return true;
				}
			}
			else if (x.compareTo(value) < 0 && isLeft) return left.remove(x, this, true);
			else if (isRight) return right.remove(x, this, false);
			else return false;
		}


		/* public void insert(T x) {
			Object temp = (x.compareTo(value) == 0) ? null : (x.compareTo(value) < 0) ? (left == null) ? left = new Node(x) : left.insert(x) : (right == null) ? right = new Node(x) : right.insert(x);
		} */

		public boolean insert(T x) {
			if (x.compareTo(value) == 0) {
				return false;
			} else if (x.compareTo(value) < 0) {
				if (left != null) return left.insert(x);
				else {
					left = new Node(x);
					return true;
				}
			} else {
				if (right != null) return right.insert(x);
				else {
					right = new Node(x);
					return true;
				}
			}
		}

		public Node min() { return (left == null) ? this : left.min(); }

		public Node max() { return (right == null) ? this : right.min(); }
		
	}
	
	private int size;
	private Node root;

	@Override
	public boolean search(T x) {
		if (x == null || root == null) return false;
		return root.search(x);
	}

	@Override
	public void insert(T x) { 
		if (x == null) throw new IllegalArgumentException("...");
		else if (root == null) root = new Node(x);
		else if (root.insert(x)) size += 1;
	}

	@Override
	public void remove(T x) {
		if (root == null) throw new IllegalStateException("...");
		if (root.remove(x, null, false)) size -= 1;
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

	public int size() { return size; }

	public void clear() { root = null; System.gc(); }

	public static void main(String[] args ) {
		BST<Integer> tree = new BST<>();
		tree.insert(2);
		tree.insert(1);
		tree.insert(3);

		System.out.println("min: " + tree.min());
		System.out.println("max: " + tree.max());

		System.out.println(tree.search(1));
		System.out.println(tree.search(2));
		System.out.println(tree.search(3));

		tree.remove(1);
		tree.remove(2);

		System.out.println(tree.search(1));
		System.out.println(tree.search(2));
		System.out.println(tree.search(3));
	}
}
