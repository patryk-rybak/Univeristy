fn row_sum_odd_numbers(n:i64) -> i64 {
    /* let start = (n * n - ((n >> 1) * 2)) + (if n % 2 == 0 {1} else {0});
    (start..start + (n - 1) * 2 + 1).step_by(2).sum() */
    n * n * n
}

#[test]
fn test1() {
    assert_eq!(row_sum_odd_numbers(1), 1);
}

#[test]
fn test2() {
    assert_eq!(row_sum_odd_numbers(2), 8);
}

#[test]
fn test3() {
    assert_eq!(row_sum_odd_numbers(3), 27);
}

#[test]
fn test4() {
    assert_eq!(row_sum_odd_numbers(4), 64);
}

#[test]
fn test5() {
    assert_eq!(row_sum_odd_numbers(42), 74088);
}

