fn gimme_the_letters(sp: &str) -> String {
    (sp.chars().nth(0).unwrap()..=sp.chars().nth(2).unwrap()).collect()
}

#[test]
fn my_tests1() {
    assert_eq!(gimme_the_letters("a-z"), "abcdefghijklmnopqrstuvwxyz");
}

#[test]
fn my_tests2() {
    assert_eq!(gimme_the_letters("h-o"), "hijklmno");
}

#[test]
fn my_tests3() {
    assert_eq!(gimme_the_letters("Q-Z"), "QRSTUVWXYZ");
}

#[test]
fn my_tests4() {
    assert_eq!(gimme_the_letters("J-J"), "J");
}

#[test]
fn my_tests5() {
    assert_eq!(gimme_the_letters("a-b"), "ab");
}

