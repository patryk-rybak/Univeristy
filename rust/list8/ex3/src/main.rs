fn part_list(arr: Vec<&str>) -> String {
    let mut res = String::new();
    for i in 1..arr.len() {
        let first: String = arr[0..i].join(" ");
        let second: String = arr[i..].join(" ");
        res.push_str(&format!("({}, {})", first, second));
    }
    res
}

fn dotest(arr: Vec<&str>, exp: &str) -> () {
    println!("arr: {:?}", arr);
    let ans = part_list(arr);
    println!("actual:\n{}", ans);
    println!("expect:\n{}", exp);
    println!("{}", ans == exp);
    assert_eq!(ans, exp);
    println!("{}", "-");
}

#[test]
fn test1() {
    dotest(vec!["cdIw", "tzIy", "xDu", "rThG"], 
        "(cdIw, tzIy xDu rThG)(cdIw tzIy, xDu rThG)(cdIw tzIy xDu, rThG)");
}

#[test]
fn test2() {
    dotest(vec!["I", "wish", "I", "hadn't", "come"],
        "(I, wish I hadn't come)(I wish, I hadn't come)(I wish I, hadn't come)(I wish I hadn't, come)");
}

#[test]
fn test3() {
    dotest(vec!["1", "2", "3", "4"], 
        "(1, 2 3 4)(1 2, 3 4)(1 2 3, 4)");
}

#[test]
fn test4() {
    dotest(vec!["1", "2"], 
        "(1, 2)");
}

#[test]
fn test5() {
    dotest(vec!["1", "2", "3"], 
        "(1, 2 3)(1 2, 3)");
}
