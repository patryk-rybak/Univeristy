import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class CreateFile_1 {
	public static void main(String[] args) {
		String path = "data_1.txt";

		try (BufferedWriter bw = new BufferedWriter(new FileWriter(path))) {
			Random random = new Random();

			for (int i = 0; i < 40; i++) {
				int number = random.nextInt((int) Math.pow(10, 9)) + 1;
				switch (i % 6) {
					case 0 -> {
						bw.write(Integer.toString(number));
					}
					case 1 -> {
						bw.write("\t ");
						bw.write(Integer.toString(number));
						bw.write(" \t");
					}
					case 2 -> {
						bw.write("// To jest komentarz 42");
					}
					case 3 -> {
						bw.write("\t ");
						bw.write(Integer.toString(number));
						bw.write(" \t");
						bw.write("// To jest komentarz 42");
					}
					case 4 -> {
						bw.write(Integer.toString(number));
						bw.write("\t");
						bw.write("// To jest komentarz 42");
					}
					case 5 -> {
					}
					default -> {
					} 
				}
				bw.newLine();
			}

			bw.newLine();
			System.out.println("Plik został utworzony.");

		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}

