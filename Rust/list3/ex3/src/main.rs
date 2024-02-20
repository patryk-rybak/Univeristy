struct Cipher {
    map1: Vec<u8>,
    map2: Vec<u8>,
}

impl Cipher {
    fn new(map1: &str, map2: &str) -> Cipher {
        Cipher {
            map1: map1.as_bytes().to_vec(),
            map2: map2.as_bytes().to_vec(),
        }
    }

    fn encode(&self, string: &str) -> String {
        string.chars().map(|c| self.map1.iter().position(|&f| f == c as u8).map_or(c, |p| self.map2[p] as char)).collect()
    }

    fn decode(&self, string: &str) -> String {
        string.chars().map(|c| self.map2.iter().position(|&f| f == c as u8).map_or(c, |p| self.map1[p] as char)).collect()
    }
}

#[test]
fn test1() {
    let map1 = "abcdefghijklmnopqrstuvwxyz";
    let map2 = "etaoinshrdlucmfwypvbgkjqxz";
    let cipher = Cipher::new(map1, map2);
    assert_eq!(cipher.encode("abc"), "eta");
}

#[test]
fn test2() {
    let map1 = "abcdefghijklmnopqrstuvwxyz";
    let map2 = "etaoinshrdlucmfwypvbgkjqxz";
    let cipher = Cipher::new(map1, map2);
    assert_eq!(cipher.encode("xyz"), "qxz");
}

#[test]
fn test3() {
    let map1 = "abcdefghijklmnopqrstuvwxyz";
    let map2 = "etaoinshrdlucmfwypvbgkjqxz";
    let cipher = Cipher::new(map1, map2);
    assert_eq!(cipher.encode("aeiou"), "eirfg");
}

#[test]
fn test4() {
    let map1 = "abcdefghijklmnopqrstuvwxyz";
    let map2 = "etaoinshrdlucmfwypvbgkjqxz";
    let cipher = Cipher::new(map1, map2);
    assert_eq!(cipher.decode("eta"), "abc");
}

#[test]
fn test5() {
    let map1 = "abcdefghijklmnopqrstuvwxyz";
    let map2 = "etaoinshrdlucmfwypvbgkjqxz";
    let cipher = Cipher::new(map1, map2);
    assert_eq!(cipher.decode("qxz"), "xyz");
}

#[test]
fn test6() {
    let map1 = "abcdefghijklmnopqrstuvwxyz";
    let map2 = "etaoinshrdlucmfwypvbgkjqxz";
    let cipher = Cipher::new(map1, map2);
    assert_eq!(cipher.decode("eirfg"), "aeiou");
}

