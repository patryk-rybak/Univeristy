fn encode(msg: String, n: i32) -> Vec<i32> {
    msg.chars().zip(n.to_string().chars().cycle()).map(|(c, k)| c as i32 - 96 - 48 + k as i32).collect()
}

#[test]
fn fixed_tests1() {
    assert_eq!(encode("aaaa".to_string(), 1939), vec![2, 10, 4, 10]);
}


#[test]
fn fixed_tests2() {
    assert_eq!(encode("".to_string(), 1939), vec![]);
}

#[test]
fn fixed_tests3() {
    assert_eq!(encode("bbbbbbbb".to_string(), 1939), vec![3, 11, 5, 11, 3, 11, 5, 11]);
}

#[test]
fn fixed_tests4() {
    assert_eq!(encode("scout".to_string(), 1939), vec![20, 12, 18, 30, 21]);
}


#[test]
fn fixed_tests5() {
    assert_eq!(encode("masterpiece".to_string(), 1939), vec![14, 10, 22, 29, 6, 27, 19, 18, 6, 12, 8]);
}
