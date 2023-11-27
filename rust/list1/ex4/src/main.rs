fn main() {
    assert_eq!(&printer_error("aaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbmmmmmmmmmmmmmmmmmmmxyz"), "3/56");
    assert_eq!(&printer_error("kkkwwwaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbmmmmmmmmmmmmmmmmmmmxyz"), "6/60");
    assert_eq!(&printer_error("kkkwwwaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbmmmmmmmmmmmmmmmmmmmxyzuuuuu"), "11/65");
    assert_eq!(&printer_error("abcdzzvv"), "4/8");
    assert_eq!(&printer_error("aaaaaaaaxx"), "2/10");
}

fn printer_error(s: &str) -> String {
    format!("{}/{}", (s.chars().filter(|c| c > 'm')).count(), s.len())
}
