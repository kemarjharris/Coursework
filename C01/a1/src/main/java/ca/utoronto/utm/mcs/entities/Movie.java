package ca.utoronto.utm.mcs.entities;


public class Movie implements Neo4jEntity<Movie> {
	
	private String id;
	private String name;
	
	private Movie() {
		
	}

	public Movie(String id, String name) {
		super();
		this.id = id;
		this.name = name;
	}

	@Override
	public String nodeCreationString() {
		return "Movie:movie {name:\"" + name + "\", id:\"" + id + "\"}";
	}

	@Override
	public String nodeId() {
		return id;
	}

	@Override
	public String nodeName() {
		return name;
	}

	@Override
	public String label() {
		// TODO Auto-generated method stub
		return "movie";
	}
	
	
}
