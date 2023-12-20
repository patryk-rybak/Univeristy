fn main() {
    let res: Vec<i32> = first_n_smallest(&[1,2,3,1,2], 3);
    println!("res   {:?}", res);
}

fn first_n_smallest(arr: &[i32], n: usize) -> Vec<i32> {
    if arr.len() <= n {
        return arr.to_vec();
    }
    
    // dlaczego nei into_inter() bez cloned() ?
    let mut indexed_array: Vec<(usize, i32)> = arr.iter().cloned().enumerate().collect();

    indexed_array.sort_by_key(|&(_, v)| v);

    let mut res: Vec<(usize, i32)> = indexed_array.into_iter().take(n).collect();
    res.sort_by_key(|&(i, _)| i);
    res.into_iter().map(|(_, v)| v).collect()
}

#[test]
fn test1() {
    assert_eq!(first_n_smallest(&[1,2,3,4,5],3), [1,2,3])
}

#[test]
fn test2() {
    assert_eq!(first_n_smallest(&[5,4,3,2,1],3), [3,2,1]);
}

#[test]
fn test3() {
    assert_eq!(first_n_smallest(&[1,2,3,1,2],3), [1,2,1]);
}

#[test]
fn test4() {
    assert_eq!(first_n_smallest(&[1,2,3,4,5],0), []);
}

#[test]
fn test5() {
    assert_eq!(first_n_smallest(&[1,2,3,4,5],5), [1,2,3,4,5]);
}

#[test]
fn test6() {
    assert_eq!(first_n_smallest(&[2,1,2,3,4,2],2), [2,1]);
}
