
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Comparator;
import java.util.List;
import java.util.LinkedList;
import java.util.stream.Collectors;

class FileCheck {

	LinkedList<Triangle> trianglesList;

	int comments;
	int emptyLines;
	int triangles;
	String path; 

	Pattern commentPattern;
	Pattern notallowedCharsPattern;
	Pattern exactlyThreeNumbersPattern;

	Matcher matcher;

	FileCheck(String path) {
		trianglesList = new LinkedList<>();
		comments = 0;
		emptyLines = 0;
		triangles = 0;
		this.path = path; 
		commentPattern = Pattern.compile("//.*");
		notallowedCharsPattern = Pattern.compile("[^\\d.\\s]");
		exactlyThreeNumbersPattern = Pattern.compile("\\b\\s?(\\d+(\\.\\d+)?)\\s+(\\d+(\\.\\d+)?)\\s+(\\d+(\\.\\d+)?)(\\s+(\\d+))?\\b");
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
					if (line.replaceAll("\\s+", "").isEmpty()) { continue; }
				}
				matcher = notallowedCharsPattern.matcher(line);
				if (matcher.find()) {
					throw new Exception("Niedozwolone znaki poza komentarzem");
				}
				matcher = exactlyThreeNumbersPattern.matcher(line);
				if (matcher.find() && matcher.group(7) == null){
					try {
						double side1 = Double.parseDouble(matcher.group(1));
						double side2 = Double.parseDouble(matcher.group(3));
						double side3 = Double.parseDouble(matcher.group(5));

						Triangle t = new Triangle(side1, side2, side3);
						trianglesList.add(t);
					} catch (IllegalArgumentException e) {
						System.out.println(e.getMessage());
					}
				} else {
					if (matcher.find()) {System.out.println(matcher.group(0));}
					throw new Exception("Linia nie zawiera dokładnie trzech liczb");
				}
				triangles += 1;
			}

			if (comments == 0 || emptyLines == 0 || triangles < 10) {
				throw new Exception("Niespelniony warunek: comments > 1 && emptyLines > 1 && triangles >= 10");
			}

		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

	public LinkedList<Triangle> getContent() {
		return trianglesList;
	}

	public static void main(String[] args) {
		FileCheck fc = new FileCheck("data.txt");
		fc.check();
		LinkedList<Triangle> content = fc.getContent();

		// 1. wypisz trójkąty z kolekcji uporządkowane od najmniejszego do największego obwodu
		System.out.println();
		content.stream()
			.sorted(Comparator.comparingDouble(Triangle::calculatePerimeter))
			.forEach(triangle -> System.out.println(triangle.calculatePerimeter() + ", " + triangle));

		// 2. wypisz te trójkąty z kolekcji, które są trójkątami prostokątnymi
		System.out.println();
		content.stream()
			.filter(Triangle::isRightTriangle)
			.forEach(triangle -> System.out.println(triangle));

		// 3. wypisz ile spośród wszystkich trójkątów w kolekcji jest równobocznych
		System.out.println();
		long countEquilateral = content.stream()
			.filter(Triangle::isEquilateral)
			.count();
		System.out.println(countEquilateral);

		// 4. wypisz dwa trójkąty z kolekcji, których pola są odpowiednio najmniejsze i największe
		System.out.println();
		Triangle smallestAreaTriangle = content.stream()
			.min(Comparator.comparingDouble(Triangle::calculateArea))
			.orElse(null);
		Triangle largestAreaTriangle = content.stream()
			.max(Comparator.comparingDouble(Triangle::calculateArea))
			.orElse(null);

		System.out.println("smallest area triangle: " + smallestAreaTriangle.calculateArea() + ", " + smallestAreaTriangle);
		System.out.println("largest area triangle: " + largestAreaTriangle.calculateArea() + ", " + largestAreaTriangle);



	}
}

