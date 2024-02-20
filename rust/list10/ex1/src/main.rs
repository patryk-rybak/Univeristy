// Rules for validation
//
//   1. Data structure dimension: NxN where N > 0 and √N == integer
//   2. Rows may only contain integers: 1..N (N included)
//   3. Columns may only contain integers: 1..N (N included)
//   4. 'Little squares' (3x3 in example above) may also only contain integers: 1..N (N included)

use itertools::Itertools;

struct Sudoku{
    data: Vec<Vec<u32>>,
}

impl Sudoku{
    fn is_valid(&self) -> bool {
        self.is_first_rule() && self.is_second_rule() && self.is_third_rule() && self.is_fourth_rule()
    }

    fn is_first_rule(&self) -> bool {
        (self.data.len() as f64).sqrt() == (self.data.len() as f64).sqrt().round()
         &&
        self.data.iter().all(|v| v.len() == self.data.len())
    }

    fn is_second_rule(&self) -> bool {
        self.data.iter().all(|v| v.iter().sorted().enumerate().all(|(i, &e)| (i as u32) + 1 == e))
    }

    // poeksperymentowac z iter i sorted i co robi ten move dokladnie
    fn is_third_rule(&self) -> bool {
       (0..self.data.len())
        .map(|col_idx| self.data.iter().map(move |row| row[col_idx]))
        .all(|col_iter| col_iter.collect::<Vec<_>>().iter().sorted().enumerate().all(|(i, &e)| (i as u32) + 1 == e))

    }

    fn is_fourth_rule(&self) -> bool {
        let block_size = (self.data.len() as f64).sqrt() as usize;

        let mut res: bool = true;
        for row_start in (0..self.data.len()).step_by(block_size) {
            for col_start in (0..self.data.len()).step_by(block_size) {
                res = res && self.data.iter().skip(row_start).take(block_size)
                                .flat_map(|row| row.iter().skip(col_start).take(block_size)).sorted().enumerate().all(|(i, &e)| (i as u32) + 1 == e);
            }
        }
        res
    }

}

#[test]
fn first_rule_test() {
    let bad_sudoku = Sudoku{
        data: vec![
            vec![1,2,3,4,5],
            vec![1,2,3,4],
            vec![1,2,3,4],
            vec![1],
        ]
    };
    assert!(!bad_sudoku.is_valid());
}

#[test]
fn second_rule_test() {
    let bad_sudoku = Sudoku{
        data: vec![
            vec![1,2,3, 4,5,6, 7,8,9],
            vec![1,2,3, 4,5,6, 7,8,9],
            vec![1,2,3, 4,5,6, 7,8,9],

            vec![1,2,3, 4,5,6, 7,8,9],
            vec![1,2,3, 4,5,6, 7,8,9],
            vec![1,2,3, 4,5,6, 7,8,9],

            vec![1,2,3, 4,5,6, 7,8,9],
            vec![1,2,3, 4,5,6, 7,8,9],
            vec![1,2,3, 4,5,6, 7,8,9],
        ]
    };

    assert!(!bad_sudoku.is_valid());
}

#[test]
fn third_rule_test() {
    let bad_sudoku = Sudoku{
        data: vec![
            vec![1,1,1, 1,1,1, 1,1,1],
            vec![2,2,2, 2,2,2, 2,2,2],
            vec![3,3,3, 3,3,3, 3,3,3],

            vec![4,4,4, 4,4,4, 4,4,4],
            vec![5,5,5, 5,5,5, 5,5,5],
            vec![6,6,6, 6,6,6, 6,6,6],

            vec![7,7,7, 7,7,7, 7,7,7],
            vec![8,8,8, 8,8,8, 8,8,8],
            vec![9,9,9, 9,9,9, 9,9,9],
        ]
    };

    assert!(!bad_sudoku.is_valid());
}

#[test]
fn fourth_rule_test() {
    let bad_sudoku = Sudoku{
        data: vec![
            vec![1,2,3, 4,5,6, 7,8,9], 
            vec![2,3,1, 5,6,4, 8,9,7],  
            vec![3,1,2, 6,4,5, 9,7,8], 

            vec![4,5,6, 7,8,9, 1,2,3], 
            vec![5,6,4, 8,9,7, 2,3,1], 
            vec![6,4,5, 9,7,8, 3,1,2], 

            vec![7,8,9, 1,2,3, 4,5,6], 
            vec![8,9,7, 2,3,1, 5,6,4], 
            vec![9,7,8, 3,1,2, 6,4,5]
        ]
    };
    assert!(!bad_sudoku.is_valid());
}

#[test]
fn good_sudoku_1() {
    let good_sudoku = Sudoku{
        data: vec![
            vec![7,8,4, 1,5,9, 3,2,6],
            vec![5,3,9, 6,7,2, 8,4,1],
            vec![6,1,2, 4,3,8, 7,5,9],

            vec![9,2,8, 7,1,5, 4,6,3],
            vec![3,5,7, 8,4,6, 1,9,2],
            vec![4,6,1, 9,2,3, 5,8,7],

            vec![8,7,6, 3,9,4, 2,1,5],
            vec![2,4,3, 5,6,1, 9,7,8],
            vec![1,9,5, 2,8,7, 6,3,4]
        ]
    };

    assert!(good_sudoku.is_valid());
}

#[test]
fn good_sudoku_2() {

    let good_sudoku = Sudoku{
        data: vec![
            vec![1, 4,  2, 3],
            vec![3, 2,  4, 1],

            vec![4, 1,  3, 2],
            vec![2, 3,  1, 4],
        ]
    };
    assert!(good_sudoku.is_valid());
}
