mod solution {
    //use std::ops::IndexMut;

    pub fn range_extraction(a: &[i32]) -> String {
        let mut res: Vec<String> = Vec::new();
        let mut start_index = 0;
        let mut end_index = 0;
        loop {
            while end_index < a.len() - 1 && (a[end_index] - a[end_index + 1]).abs() == 1 { end_index += 1; }

            if end_index - start_index >= 1 {
                res.push(format!("{}{}{}", a[start_index], if end_index - start_index == 1 {","} else {"-"} , a[end_index]))
            } else {
                res.push(format!("{}", a[start_index]))
            }

            if end_index == a.len() - 1 { break; }
            start_index = end_index + 1;
            end_index += 1;
        }
        if end_index == a.len() && start_index == a.len() - 1 { res.push(a[start_index].to_string()); }
        res.join(",")
    }
}

#[test]
fn example1() {
    assert_eq!(solution::range_extraction(&[-6,-3,-2,-1,0,1,3,4,5,7,8,9,10,11,14,15,17,18,19,20]), "-6,-3-1,3-5,7-11,14,15,17-20");	
}

#[test]
fn example2() {
    assert_eq!(solution::range_extraction(&[-3,-2,-1,2,10,15,16,18,19,20]), "-3--1,2,10,15,16,18-20");
}

#[test]
fn example3() {
    assert_eq!(solution::range_extraction(&[1]), "1");
}

#[test]
fn example4() {
    assert_eq!(solution::range_extraction(&[1, 3, 5]), "1,3,5");
}

#[test]
fn example5() {
    assert_eq!(solution::range_extraction(&[-5,-4,-3,-2,-1,0,1,2,3,4,5]), "-5-5");
}
