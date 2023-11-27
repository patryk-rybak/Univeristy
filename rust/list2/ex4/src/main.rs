fn count_bits(n: i64) -> u32 {
    n.count_ones()
}

#[test]
fn my_tests1() {
    assert_eq!(count_bits(0), 0);
}

#[test]
fn my_tests2() {
    assert_eq!(count_bits(4), 1);
}

#[test]
fn my_tests3() {
    assert_eq!(count_bits(7), 3);
}

#[test]
fn my_tests4() {
    assert_eq!(count_bits(9), 2);
}

#[test]
fn my_tests5() {
    assert_eq!(count_bits(10), 2);
}

