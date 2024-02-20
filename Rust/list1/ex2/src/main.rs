fn main() {
  assert_eq!(count_red_beads(0), 0);
  assert_eq!(count_red_beads(1), 0);
  assert_eq!(count_red_beads(3), 4);
  assert_eq!(count_red_beads(5), 8);
  assert_eq!(count_red_beads(2), 2);
}

fn count_red_beads(n: u32) -> u32 {
    if n <= 0 {0} else {2 * (n - 1)}
}
