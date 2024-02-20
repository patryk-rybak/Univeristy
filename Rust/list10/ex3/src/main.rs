fn comp(a: Vec<i64>, b: Vec<i64>) -> bool {
    let mut sorted_a = a.clone();
    let mut sorted_b = b.clone();

    sorted_a.sort();
    sorted_b.sort();

    sorted_a == sorted_b.iter().map(|&x| (x as f64).sqrt() as i64).collect::<Vec<i64>>()
}


fn testing(a: Vec<i64>, b: Vec<i64>, exp: bool) -> () {
    assert_eq!(comp(a, b), exp)
}

#[test]
fn test1() {
    let a1 = vec![121, 144, 19, 161, 19, 144, 19, 11];
    let a2 = vec![11*21, 121*121, 144*144, 19*19, 161*161, 19*19, 144*144, 19*19];
    testing(a1, a2, false);
}

#[test]
fn test2() {
    let a1 = vec![2, 2, 2];
    let a2 = vec![2*2, 2*2, 2*2];
    testing(a1, a2, true);
}

#[test]
fn test3() {
    let a1 = vec![121, 144, 19, 161, 19, 144, 19, 11];
    let a2 = vec![11*11, 121*121, 144*144, 19*19, 161*161, 19*19, 144*144, 19*19];
    testing(a1, a2, true);
}

#[test]
fn test4() {
    let a1 = vec![1, 2, 3];
    let a2 = vec![1, 2*2, 3*3];
    testing(a1, a2, true);
}

#[test]
fn test5() {
    let a1 = vec![];
    let a2 = vec![];
    testing(a1, a2, true);
}
