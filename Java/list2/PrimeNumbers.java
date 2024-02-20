import java.util.ArrayList;
import java.util.List;
import java.util.Collections;
import java.util.Arrays;

public final class PrimeNumber {
	
	/* private final static int POWER2 = 21;
	private final static int[] primes = new int[1 << POWER2];

	static {
		
	} */

	private static ArrayList<Long> primes = new ArrayList<Long>(4);

	static {
		primes.add(2L);
		primes.add(3L);
		primes.add(5L);
		primes.add(7L);
	}

	private static long upperLimitIndex = primes.get(1) * primes.get(1); // Index of root of upper limit of the primes set

	private static void extend() {

		long p = primes.get((int)upperLimitIndex);
		long q = primes.get((int)upperLimitIndex + 1);
		long segmentMin = p * p;
		long segmentMax = q * q;
		long segmentLen = segmentMax - segmentMin - 1;
		boolean[] isPrimeArray = new boolean[(int)segmentLen];
		Arrays.fill(isPrimeArray, Boolean.TRUE);

		for (long i = 0; i <= upperLimitIndex; i++) {
			long kthPrime = primes.get((int)i);
			long start = theSmallestGreater(kthPrime, segmentMin);
			long isPrimeIndex = start - segmentMin - 1;
			while (isPrimeIndex < segmentLen) {
				isPrimeArray[(int)isPrimeIndex] = false;
				isPrimeIndex += kthPrime;
			}
		}

		upperLimitIndex += 1;
		for (long i = 0; i < segmentLen; i++) {
			if (isPrimeArray[(int)i]) {primes.add(i + segmentMin + 1);}
		}

		isPrimeArray = null;
		System.gc();
	}

	private static long theSmallestGreater(long x, long y) {
	   return y + (x - (y % x));
	}

	private static boolean millerRabin() {
		return true;
	}




// extend zamiast mleerarabina
	public static boolean isPrime(long x) {
		while (x > primes.get((int)upperLimitIndex) * primes.get((int)upperLimitIndex)) {return millerRabin();} 
		return (Collections.binarySearch(primes, x) >= 0);
	}

	public static void primeFactors(long x) {
		System.out.print(x + " =");
		
		ArrayList<Long> res = new ArrayList<Long>();
		int index = 0;
		while (true) {
			while (index < primes.size()) {
				long p = primes.get(index);
				while (x % p == 0) {
					res.add(p);
					x = x / p;
				}
				index += 1;
			}
			if (x != 1L) {
				index = primes.size();
				extend();
			} else {break;}
		}

		System.out.print(" " + res.get(0));
		for (int i = 1; i < res.size(); i++) {
			System.out.print(" * " + res.get(i));
		}
		System.out.println();
	}









	public static void main(String[] args) {
		primeFactors(2);
		for (long p : primes) {System.out.println(p);}


		primeFactors(Long.MAX_VALUE);
		for (long p : primes) {System.out.println(p);}
	}
}	
