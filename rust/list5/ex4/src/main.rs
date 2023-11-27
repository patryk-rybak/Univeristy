fn expanded_form(n: u64) -> String {
    let mut res = Vec::new();
    for (i, digit) in n.to_string().chars().rev().enumerate() {
        if digit != '0' {
            res.push(format!("{}{}", digit, "0".repeat(i)));
        }
    }
    res.into_iter().rev().collect::<Vec<String>>().join(" + ")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn examples1() {
        assert_eq!(expanded_form(12), "10 + 2");
    }

    #[test]
    fn examples2() {
        assert_eq!(expanded_form(42), "40 + 2");
    }

    #[test]
    fn examples3() {
        assert_eq!(expanded_form(70304), "70000 + 300 + 4");
    }
	
	#[test]
    fn examples4() {
        assert_eq!(expanded_form(99999), "90000 + 9000 + 900 + 90 + 9");
    }

	#[test]
    fn examples5() {
        assert_eq!(expanded_form(1), "1");
    }
}
