import  java.util.Scanner;

public class Main {

	public static String roman(int n) {
		String[] romanLetters = {"M", "CM", "D", "CD", "C","XC", "L", "XL", "X", "IX", "V", "IV", "I"};
		int[] values = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
		
		String res = "";
		int index = 0;
		while (n != 0) {
			while (n >= values[index]) {
				n -= values[index];
				res += romanLetters[index];
			}
			index += 1;	
		}
		return res;
	}

	public static String patrons(int n) {
		return switch (n % 12) {
			case 0 -> "małpa";
			case 1 -> "kurczak";
			case 2 -> "pies";
			case 3 -> "świnia";
			case 4 -> "szczur";
			case 5 -> "bawół";
			case 6 -> "tygrys";
			case 7 -> "królik";
			case 8 -> "smok";
			case 9 -> "wąż";
			case 10 -> "koń";
			case 11 -> "owca";
			default -> "error";
		};
	}	

	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);
		
		System.out.println("Enter your name: ");
		String name = scanner.nextLine();
		
		System.out.println("Enter your year of birth: ");
		int year = Integer.valueOf(scanner.nextLine());
		
		
		if ( year >= 4000 || year <= 0) {
			throw new IllegalArgumentException("liczba " + year + " spoza zakresu 1-3999");
		}

		String roman = roman(year);

		System.out.println("\nHello " + name + "!");
		System.out.println("Your year of birth is " + roman + ".");
		System.out.println("Your patron is " + patrons(year) + ".");
	}
}
