use itertools::Itertools;

fn logest(a1: &str, a2: &str) -> String {
    format!("{}{}", a1, a2).chars().sorted().dedup().collect()
}

#[test]
fn my_tests1() {
    assert_eq!(logest("aretheyhere", "yestheyarehere"), "aehrsty");
}

#[test]
fn my_tests2() {
    assert_eq!(logest("loopingisfunbutdangerous", "lessdangerousthancoding"), "abcdefghilnoprstu");
}

#[test]
fn my_tests3() {
    assert_eq!(logest("", ""), "");
}

#[test]
fn my_tests4() {
    assert_eq!(logest("", "bbaab"), "ab");
}

#[test]
fn my_tests5() {
    assert_eq!(logest("987654321", "0"), "0123456789");
}
