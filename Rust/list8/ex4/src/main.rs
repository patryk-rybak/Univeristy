n j_n(n: i32) -> (Vec<i32>, Vec<i32>) {
    let mut j = vec![0];
    let mut a = vec![1];
    for i in 1..n {
			j.push(i - a[j[i as usize - 1] as usize]);
			a.push(i - j[a[i as usize - 1] as usize]);
    }
    (j, a)
}

fn john(n: i32) -> Vec<i32> {
	j_n(n).0
}

fn ann(n: i32) -> Vec<i32> {
	j_n(n).1
}

fn sum_john(n: i32) -> i32 {
	j_n(n).0.iter().sum()
}

fn sum_ann(n: i32) -> i32 {
	j_n(n).1.iter().sum()
}

#[test]
fn test_john() {
		assert_eq!(john(11), vec![0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6]);
		assert_eq!(john(14), vec![0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8]);
}
#[test]
fn test_ann() {
		assert_eq!(ann(6), vec![1, 1, 2, 2, 3, 3]);
		assert_eq!(ann(15), vec![1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 6, 7, 8, 8, 9]);
}
#[test]
fn test_sum_john() {
		assert_eq!(sum_john(75), 1720);
		assert_eq!(sum_john(78), 1861);
}
#[test]
fn test_sum_ann() {
		assert_eq!(sum_ann(115), 4070);
		assert_eq!(sum_ann(150), 6930);
}
#[test]
fn test_initial_john_ann() {
		assert_eq!(sum_ann(1), 1);
		assert_eq!(sum_john(1),0 );
}
