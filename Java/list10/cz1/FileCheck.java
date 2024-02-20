import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import java.util.List;
import java.util.stream.Collectors;


class FileCheck_1 {

	ArrayList<Integer> numbersList;

	int comments;
	int emptyLines;
	int numbers;
	String path; 

	Pattern commentPattern;
	Pattern lettersPattern;
	Pattern tooManyNumbers;

	Matcher matcher;

	FileCheck_1(String path) {

		numbersList = new ArrayList<>();
		comments = 0;
		emptyLines = 0;
		numbers = 0;
		this.path = path; 
		commentPattern = Pattern.compile("//.*");
		lettersPattern = Pattern.compile("^[0-9]");
		tooManyNumbers = Pattern.compile("\\b\\d+\\s+\\d+\\b");
	}

	public void check() {
	
		try (BufferedReader br = new BufferedReader(new FileReader(path))) {

			for (String line = br.readLine(); line != null; line = br.readLine()) {

				if (line.isEmpty()) {
					emptyLines += 1;
					continue;
				}
				matcher = commentPattern.matcher(line);
				if (matcher.find()) {
					comments += 1;
					line = matcher.replaceAll("");
					if (line.isEmpty()) { continue; }
				}
				matcher = lettersPattern.matcher(line);
				if (matcher.find()) {
					throw new Exception("Litery poza komentarzem");
				}
				matcher = tooManyNumbers.matcher(line);
				if (matcher.find()) {
					throw new Exception("Wiecej niz jedna liczba");
				}

				numbersList.add(Integer.parseInt(line.trim()));
				numbers += 1;
			}

			if (comments == 0 || emptyLines == 0 || numbers < 20) {
				throw new Exception("Niespelniony warunek: comments > 1 && emptyLines > 1 && numbers >= 20");
			}

		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

	public ArrayList<Integer> getContent() {
		return numbersList;
	}

	public static void main(String[] args) {
		FileCheck_1 fc = new FileCheck_1("data_1.txt");
		fc.check();
		ArrayList<Integer> content = fc.getContent();


		// 1. wypisz liczby z kolekcji uporządkowane od największej do najmniejszej wartości;
		List<Integer> posortowane = content.stream()
			.sorted((a, b) -> Integer.compare(b, a))
			.collect(Collectors.toList());
		System.out.println("\n1. Liczby posortowane: \n" + posortowane);


		// 2. wypisz te liczby z kolekcji, które są liczbami pierwszymi
		List<Integer> liczbyPierwsze = content.stream()
			.filter(x -> {
				if (x < 2) {
					return false;
				} else if ( x == 2) {
					return true;
				}
				for (int i = 2; i <= Math.sqrt(x); i++) {
					if (x % i == 0) {
						return false;
					}
				}
				return true;
			})
			.collect(Collectors.toList());
		System.out.println("\n2. Liczby pierwsze: \n" + liczbyPierwsze);


		// 3. wypisz sumę wszystkich liczb z kolekcji, które są < n
		int n = 186214366;
		long sumaMniejszeN = content.stream()
			.filter(x -> x < n)
			.mapToLong(Integer::intValue)
			.sum();
		System.out.println("\n3. Suma liczb < " + n + ": \n" + sumaMniejszeN);


		// 4. wypisz ile spośród wszystkich liczb w kolekcji jest podzielnych przez n (przykładowo dla n = 7)
		int dzielnik = 7;
		long podzielnePrzezN = content.stream()
			.filter(x -> x % dzielnik == 0)
			.count();
		System.out.println("\n4. Ilość liczb podzielnych przez " + dzielnik + ": " + podzielnePrzezN);

	}
}

