/* fn zoom(n: i32) -> String {
    let drugi_bit = n & 3 == 2;
    let c = ('□', '■');
    let mut temp: String = String::new();
    for r in 0..(n >> 1) + 1 {
        if drugi_bit {
            for i in 0..r { if i % 2 == 0 {temp.push(c.1)} else {temp.push(c.0)} }
            for _i in r..n-r { if r % 2 == 0 {temp.push(c.1)} else {temp.push(c.0)} }
            for i in n-r..n { if i % 2 == 0 {temp.push(c.1)} else {temp.push(c.0)} }
        } else {
            for i in 0..r { if i % 2 == 0 {temp.push(c.0)} else {temp.push(c.1)} }
            for _i in r..n-r { if r % 2 == 0 {temp.push(c.0)} else {temp.push(c.1)} }
            for i in n-r..n { if i % 2 == 0 {temp.push(c.0)} else {temp.push(c.1)} }
        }
        temp.push('\n');
    }
    let reversed_chars: String = temp.chars().take(((n*n - n*2) as i32).try_into().unwrap()).collect::<String>();
    println!("\n\n{}\n\n", reversed_chars);
    let sec_part: String = reversed_chars.chars().rev().collect::<String>();
    println!("\n\n{}\n\n", sec_part);
    temp + &sec_part[n+2 .. sec_part.len()]
} */

fn zoom(n: i32) -> String{

    let res: Vec<String> = Vec::new();
    let start = if n & 3 == 2 { '■' } else { '□' };
    let temp: String = String::new();
    res.push(if sec_bit {std::iter::repeat(start).take(n).collect::<String>()});

    for r in 1..n {
       res.push((&res.last().unwrap()[0..r]).map(|c| if c == '■' {'□'} else {'■'}).collect::<String>()
           +    (&res.last().unwrap()[r..n-r]).map(|c| if c == '■' {'□'} else {'■'}).collect::<&str>()
           +    (&res.last().unwrap()[n-r..n]).map(|c| if c == '■' {'□'} else {'■'}).collect::<&str>())
    }

   res.join('\n')    
}

fn main() {
    println!("{}", zoom(7));
}
