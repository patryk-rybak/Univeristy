fn matrix_mul(arr: &mut [u16]) {
    let temp = arr.iter().sum::<u16>();
    arr[0] = arr[1];
    arr[1] = arr[2];
    arr[2] = arr[3];
    arr[3] = arr[4];
    arr[4] = temp % 2;
}
fn count_odd_pentafib(n: u16) -> u16 {
    if n == 0 { 0 }
    else if n > 0 && n < 5 { 1 }
    else {
        let mut v = [0, 1, 1, 0, 0];
        let mut res: u16 = 1;
        for _ in 5..n+1 {
            matrix_mul(&mut v);
            res += v[4] % 2;
        }
        res
    }
}

#[cfg(test)]
mod tests {
    use super::count_odd_pentafib;

    #[test]
    fn basic_tests1() {
        assert_eq!(count_odd_pentafib(5), 1);
    }

    #[test]
    fn basic_tests2() {
        assert_eq!(count_odd_pentafib(10), 3);
    }

    #[test]
    fn basic_tests3() {
        assert_eq!(count_odd_pentafib(15), 5);
    }

    #[test]
    fn basic_tests4() {
        assert_eq!(count_odd_pentafib(45), 15);
    }

    #[test]
    fn basic_tests5() {
        assert_eq!(count_odd_pentafib(68), 23);
    }

    #[test]
    fn edge_cases1() {
        assert_eq!(count_odd_pentafib(0), 0);
    }
    
    #[test]
    fn edge_cases2() {
        assert_eq!(count_odd_pentafib(1), 1);
    }

    #[test]
    fn edge_cases3() {
        assert_eq!(count_odd_pentafib(2), 1);
    }
}

