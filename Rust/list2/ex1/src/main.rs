fn get_count(string: &str) -> usize {
    string.chars().filter(|&c| "aeiouAEIOU".contains(c)).count()
}

#[test]
fn my_tests1() {
    assert_eq!(get_count("yyyYYY"), 0);
}

#[test]
fn my_tests2() {
    assert_eq!(get_count("abracadabra"), 5);
}

#[test]
fn my_tests3() {
    assert_eq!(get_count("aaa b"), 3);
}

#[test]
fn my_tests4() {
    assert_eq!(get_count("aeiouAEIOU"), 10);
}

#[test]
fn my_tests5() {
    assert_eq!(get_count(""), 0);
}

