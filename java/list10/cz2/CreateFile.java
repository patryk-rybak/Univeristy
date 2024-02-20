import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class CreateFile_1 {
	public static void main(String[] args) {
		String path = "data.txt";

		try (BufferedWriter bw = new BufferedWriter(new FileWriter(path))) {
			Random random = new Random();

			for (int i = 0; i < 30; i++) {
				double liczba1 = random.nextDouble();
				double liczba2 = random.nextDouble();
				double liczba3 = random.nextDouble();

				switch (i % 7) {
					case 0 -> {
						bw.write(String.format(" \t%f %f %f\t ", liczba1, liczba2, liczba3));
					}
					case 1 -> {
						// bw.write(String.format(" \t%f %f \t ", liczba1, liczba2, liczba3) + "// To jest komentarz 42");
						bw.write("");
					}
					case 2 -> {
						bw.write(String.format("%f %d %f", liczba1, 42, liczba3));
					}
					case 3 -> {
						// bw.write("\t ");
						// bw.write(Double.toString(liczba1));
						// bw.write(" \t");
						// bw.write("// To jest komentarz 42");
						bw.write("");
					}
					case 4 -> {
						bw.write("\t// To jest komentarz 42");
					}
					case 5 -> {
						bw.write(String.format("%f\t%d %f // %d", liczba1, 42, liczba3, 17));
					}
					case 6 -> {
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

