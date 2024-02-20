fn dig_pow(n: i64, p: i32) -> i64 {
    let res: i64 = n.to_string().chars().enumerate().fold(0, |acc, (i, c)| acc + (c.to_digit(10).unwrap() as i64).pow((p + i as i32).try_into().unwrap()));
    if res % n == 0 { res / n } else { -1 }
}

fn dotest(n: i64, p: i32, exp: i64) -> () {
    println!(" n: {:?};", n);
    println!("p: {:?};", p);
    let ans = dig_pow(n, p);
    println!(" actual:\n{:?};", ans);
    println!("expect:\n{:?};", exp);
    println!(" {};", ans == exp);
    assert_eq!(ans, exp);
    println!("{};", "-");
}

#[test]
fn basic_test1() {
    dotest(92, 1, -1);
}

#[test]
fn basic_test2() {
    dotest(89, 1, 1);
}

#[test]
fn basic_test3() {
    dotest(46288, 3, 51);
}
