fn print(n: i32) -> Option<String> {
    if n % 2 == 0 || n < 0 {
        return None;
    }

    Some((0..n).map(|i| {
                format!(
                    "{}{}\n",
                    " ".repeat(if i < n/2 {(-i + n/2) as usize} else {(i + n/2 - n + 1) as usize}),
                    "*".repeat(if i < n/2 {(2*i + 1) as usize} else {(-2*i + 2*n - 1) as usize})
                )
            })
            .collect::<Vec<String>>()
            .join(""),
    )
}

#[test]
fn basic_test1() {
    assert_eq!(print(3), Some(" *\n***\n *\n".to_string()) );
}

#[test]
fn basic_test2() {
    assert_eq!(print(5), Some("  *\n ***\n*****\n ***\n  *\n".to_string()) );
}

#[test]
fn basic_test3() {
    assert_eq!(print(-3),None);
}

#[test]
fn basic_test4() {
    assert_eq!(print(2),None);
}

#[test]
fn basic_test5() {
    assert_eq!(print(0),None);
}

#[test]
fn basic_test6() {
    assert_eq!(print(1), Some("*\n".to_string()) );
}
