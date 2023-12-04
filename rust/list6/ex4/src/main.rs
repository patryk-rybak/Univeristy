fn capitalize(s: &str) -> Vec<String> {
    vec![
        s.chars().enumerate().map(|(index, c)| if index % 2 == 0 { c.to_uppercase().to_string() } else { c.to_lowercase().to_string() }).collect(),
        s.chars().enumerate().map(|(index, c)| if index % 2 == 1 { c.to_uppercase().to_string() } else { c.to_lowercase().to_string() }).collect(),
    ]

}

#[test]
fn example_tests1() {
    assert_eq!(capitalize("abcdef"),["AbCdEf", "aBcDeF"]);
}

#[test]
fn example_tests2() {
    assert_eq!(capitalize("codewars"),["CoDeWaRs", "cOdEwArS"]);
}

#[test]
fn example_tests3() {
    assert_eq!(capitalize("abracadabra"),["AbRaCaDaBrA", "aBrAcAdAbRa"]);
}

#[test]
fn example_tests4() {
    assert_eq!(capitalize("a"),["A", "a"]);
}

#[test]
fn example_tests5() {
    assert_eq!(capitalize("bbbbbbbbbb"),["BbBbBbBbBb", "bBbBbBbBbB"]);
}
