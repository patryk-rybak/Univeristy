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
fn basis_tests1() {
		dotest(vec!["cdIw", "tzIy", "xDu", "rThG"], 
						"(cdIw, tzIy xDu rThG)(cdIw tzIy, xDu rThG)(cdIw tzIy xDu, rThG)");
}

#[test]
fn basis_tests2() {
		dotest(vec!["I", "wish", "I", "hadn't", "come"],
						"(I, wish I hadn't come)(I wish, I hadn't come)(I wish I, hadn't come)(I wish I hadn't, come)");
}
