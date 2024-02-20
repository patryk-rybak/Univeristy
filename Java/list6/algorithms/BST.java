package algorithms;

public class BST <T extends Comparable<T>> implements Dictionary<T>
{

	private int size;
	private Node root;

	public class Node
	{
		private Node left, right;
		private T value;

		Node(T value) { this.value = value; }

		public Node getLeft() { return left; }

		public Node getRight() { return right; }

		public T getValue() { return value; }


		/* boolean search(T x) {
			return switch (x.compareTo(value)) {
				case 1 -> (right != null) ? right.search(x) : false;
				case 0 -> true;
				case -1 -> (left != null) ? left.search(x) : false;
				default -> false;
			};} */

		boolean search(T x) {
			if (x.compareTo(value) == 0) { return true; }
			else if (x.compareTo(value) < 0 && left != null) { return left.search(x); }
			else if (x.compareTo(value) > 0 && right != null) { return right.search(x); }
			else { return false; }
		}

		Node remove(T x) {
			if (x.compareTo(value) < 0 && left != null) {
				left = left.remove(x);
				return this;
			}
			else if (x.compareTo(value) > 0 && right != null) {
				right = right.remove(x);
				return this;
			}

			if (x.compareTo(value) != 0) { return this; }

			if (left == null) { return right; }
			if (right == null) { return left; }

			Node tempParent = this;
			Node temp = right;
			while (temp.left != null) {
				tempParent = temp;
				temp = temp.left;
			}

			if (tempParent != this) { tempParent.left = temp.right; }
			else { tempParent.right = temp.right; }

			value = temp.getValue();
			
			return this;
		}

		boolean insert(T x) {
			if (x.compareTo(value) == 0) { return false; }
			else if (x.compareTo(value) < 0) {
				if (left != null) { return left.insert(x); }
				else {
					left = new Node(x);
					return true;
				}
			} else {
				if (right != null) { return right.insert(x); }
				else {
					right = new Node(x);
					return true;
				}
			}
		}

		Node min() { return (left == null) ? this : left.min(); }

		Node max() { return (right == null) ? this : right.max(); }
	}
	

	public Node getRoot() { return root; }

	@Override
	public boolean search(T x) {
		if (x == null || root == null) return false;
		return root.search(x);
	}

	@Override
	public boolean insert(T x) { 
		if (x == null) throw new IllegalArgumentException("bst insert");
		if (search(x)) { return false; }
		else if (root == null) {
			root = new Node(x);
			size += 1;
		}
		else if (root.insert(x)) { size += 1; }
		return true;
	}

	@Override
	public boolean remove(T x) {
		if (root == null) { throw new IllegalStateException("bst remove"); }
		if (search(x)) {
			root = root.remove(x);
			size -= 1;
			return true;
		}
		return false;
	}

	@Override
	public T min(){
		if (root == null) { throw new IllegalStateException("bst min"); }
		return root.min().value;
	}

	@Override
	public T max() {
		if (root == null) { throw new IllegalStateException("bst max"); }
		return root.max().value;
	}

	public int size() { return size; }

	public void clear() { root = null; System.gc(); }

	public static void main(String[] args) {

		// przyklad z pracowni
	
		BST<String> bst = new BST<>();
		
		System.out.println("\ninserting");
		System.out.println("1 " + bst.insert("1"));
		System.out.println("2 " + bst.insert("2"));
		System.out.println("3 " + bst.insert("3"));
		System.out.println("4 " + bst.insert("4"));
		System.out.println("25 " + bst.insert("25"));
/*
 * 		1
 * 		 \
 * 	          2
 * 	           \
 * 	            3
 * 	           / \
 * 	         25  4
*/

		System.out.println("\nsearching");
		System.out.println("1 " + bst.search("1"));
		System.out.println("2 " + bst.search("2"));
		System.out.println("3 " + bst.search("3"));
		System.out.println("4 " + bst.search("4"));
		System.out.println("25 " + bst.search("25"));

		System.out.println("\nremoving 3");
		System.out.println(bst.remove("3"));
/*
 * 		1
 * 		 \
 * 	          2
 * 	           \
 * 	            4
 * 	           /  
 * 	         25   
*/

		System.out.println("\nsearching");
		System.out.println("1 " + bst.search("1"));
		System.out.println("2 " + bst.search("2"));
		System.out.println("3 " + bst.search("3"));
		System.out.println("4 " + bst.search("4"));
		System.out.println("25 " + bst.search("25"));

		System.out.println("\nremoving 2");
		System.out.println(bst.remove("2"));

/*
 * 		1
 * 		 \
 * 	          4
 * 	         /  
 * 	        25      
 * 	            
*/
		System.out.println("\nsearching");
		System.out.println("1 " + bst.search("1"));
		System.out.println("2 " + bst.search("2"));
		System.out.println("3 " + bst.search("3"));
		System.out.println("4 " + bst.search("4"));
		System.out.println("25 " + bst.search("25"));
	}
}
