fn last_digit(str1: &str, str2: &str) -> i32 {
    if str1 == "0" { return 0; }
    if str2 == "0" { return 1; }

    let mod_4: u32 = str2.chars().fold(0, |acc, c| (acc * 10 + (c as u32) - 48) % 4);
    let exp: u32 = if mod_4 == 0 { 4 } else { mod_4 };
    let res = (str1.chars().last().unwrap() as i32 - 48).pow(exp);
    res % 10
}

#[test]
fn test1() {
    assert_eq!(last_digit("4", "1"), 4);
}

#[test]
fn test2() {
    assert_eq!(last_digit("4", "2"), 6);
}

#[test]
fn test3() {
    assert_eq!(last_digit("10", "10000000000"), 0);
}

#[test]
fn test4() {
    assert_eq!(last_digit("1606938044258990275541962092341162602522202993782792835301376","2037035976334486086268445688409378161051468393665936250636140449354381299763336706183397376"), 6);
}

#[test]
fn test5() {
    assert_eq!(last_digit("3715290469715693021198967285016729344580685479654510946723", "68819615221552997273737174557165657483427362207517952651"), 7);
}
