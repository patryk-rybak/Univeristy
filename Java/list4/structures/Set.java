package structures;

public interface Set {
	Pair find(String k);

	void insert(Pair p);

	void delete(String k);

	void clean();

	int howMany();
}
