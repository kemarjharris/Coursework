package ca.utoronto.utm.mcs.entities;

import java.util.Set;
import java.util.Collections;
import java.util.HashSet;
import java.util.Optional;
import java.util.stream.Collectors;

import org.json.*;




// This class is what gets used in the database for a node.
// Neo4jEntity<Actor> and Neo4jRelationship<Movie> are more for compatibility
// with the neo4jMethodHandler.
public class Actor implements Neo4jEntity<Actor>, Neo4jRelationship<Movie> {

	// These are the paramters that will show up in a neo4j Node.
	private String id;
	private String name;
	
	private Actor() {
		// Neo4j needs a blank constructor in the class
	}
	
	public Actor(String id, String name) {
		this.id = id;
		this.name = name;
	}
	
	

	// This keeps track of the relationships the actor has. Basically what neo4j uses
	// to keep track of edges. Any data structure is fine (i think?) but
	// the tutorial used sets so i followed suit.
	public Set<Movie> actedIn;

	// The rest of the functions in the class are for compatibility with the 
	// Neo4jMethodHandler.
	@Override
	public String nodeCreationString() {
		return "Actor:actor {name:\"" + name + "\", id:\"" + id + "\"}";
	}

	@Override
	public String relationshipString() {
		return "ACTED_IN";
	}

	@Override
	public String nodeId() {
		return id;
	}
@Override
	public String label() {
		// TODO Auto-generated method stub
		return "actor";
	}

	@Override
	public String nodeName() {
		return name;
	}
	
	// If you dont understand something i've done so far, nows the time to text me.
	// The next part is the complicated part. Open up Neo4jMethodHandler.java.
}
