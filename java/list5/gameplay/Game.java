package gameplay;

public class Game {
	private int zakres;
	private Wymierna liczba;
	private int maksIlośćPrób;
	private int licznikPrób;

	public Game() {
		
	}

	public void start(int z) {
		if (z < 5 || z > 20) throw ...;
		zakres = z;
		//do {
		int licz = (int) (Math.random() * zakres) + 1;
		int mian = (int) (Math.random() * zakres) + 1;
		//} while (licz >= mian);
		assert (liczba.getNumerator() < liczba.getDenominator());
		liczba = new Wymierna(licz, mian);
		// inicjalizacja: maksIlośćPrób, licznikPrób, ...
	}
