fn main() {
    assert_eq!(string_to_number("1234"), 1234);
    assert_eq!(string_to_number("605"), 605);
    assert_eq!(string_to_number("1405"), 1405);
    assert_eq!(string_to_number("-7"), -7);
    assert_eq!(string_to_number("47"), 47);
}

fn string_to_number(s: &str) -> i32 {
    s.parse().expect("Not a number!")
}
