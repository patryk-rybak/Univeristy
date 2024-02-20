fn summy(strng: &str) -> i32 {
    strng.split(' ').map(|num| num.parse().unwrap_or(0)).sum()
}

#[test]
fn my_tests1() {
    assert_eq!(summy("1 2 3"), 6);
}

#[test]
fn my_tests2() {
    assert_eq!(summy("1 2 3 4"), 10);
}

#[test]
fn my_tests3() {
    assert_eq!(summy("1 2 3 4 5"), 15);
}

#[test]
fn my_tests4() {
    assert_eq!(summy("10 10"), 20);
}

#[test]
fn my_tests5() {
    assert_eq!(summy("0 0"), 0);
}
