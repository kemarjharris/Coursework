package ca.utoronto.utm.mcs;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.neo4j.driver.v1.Driver;
import org.neo4j.driver.v1.Record;
import org.neo4j.driver.v1.Session;
import org.neo4j.driver.v1.StatementResult;
import org.neo4j.driver.v1.Transaction;
import org.neo4j.driver.v1.TransactionWork;
import org.neo4j.driver.v1.exceptions.NoSuchRecordException;
import org.neo4j.driver.v1.types.Node;

import ca.utoronto.utm.mcs.entities.Neo4jEntity;
import ca.utoronto.utm.mcs.entities.Neo4jRelationship;

// This is the class that handles all data interactions between the server and java.
// There may be a better way to do this so we might want to extract it to an interface later,
// but since Ilir didn't explain anything and driver is the only access point to the server
// given to us, i'll explain how everything here works.
public class Neo4jMethodHandler {
	
	// The driver that lets us connect to the server.
	Driver driver;

	public Neo4jMethodHandler(Driver driver) {
		this.driver = driver;
	}
	
	// This the function that lets us sent data to the server.
	// The StatementResult is what the server gives back.
	// cyperCommand is basically what you're supposed to type in the shell
	// at the top of the webpage when you connect to localhost:7474.
	private StatementResult runCypherCommand(String cypherCommand) {
		try (Session session = driver.session() ) {	
			StatementResult result = session.run(cypherCommand);
			return result;
		}
	}
	
	@SuppressWarnings("rawtypes")
	// Create a neo4jNode.
	// Need to handle the part where nodes can have more than one Id.
	public void CreateNode(Neo4jEntity entity) {
		runCypherCommand("CREATE (" + entity.nodeCreationString() + ")");
	}
	
	public void MergeNode(Neo4jEntity entity) {
		runCypherCommand("MERGE ( n:" +entity.label() + "{id:"+entity.nodeId()+"}) " +
	                     "SET n = {name: \"" +entity.nodeName() + "\", id: \"" + entity.nodeId() + "\"}" 
	                     );
	}
	
	// Create a neo4j relationship between two nodes.
	// Both have to be in the database or itll throw an error.
	public void CreateRelationship(String aId, String aLabel, String relationship, String bId, String bLabel) {
		/*
	    eg:
		MATCH (a:Person),(b:Person)
		WHERE a.name = 'A' AND b.name = 'B'
		CREATE (a)-[r:RELTYPE]->(b)
		RETURN type(r)
		*/
		
		runCypherCommand("MATCH(a:" + aLabel + "),(b:" + bLabel + ")"
				+ " WHERE a.id = \"" + aId + "\" AND b.id = \"" + bId + "\""
				+ " MERGE (a)-[:" + relationship + "]->(b)");
	}
	
	// Create a relationship between two ndoes, but with objects as parameters
	public <T> void CreateRelationship(Neo4jRelationship<T> a, String aLabel, Neo4jEntity<T> b, String bLabel) {
		CreateRelationship(a.nodeId(), aLabel, a.relationshipString(), b.nodeId(), bLabel);
	}
	
	// Find a node by it's id.
	public Node findNodeById(String nodeId) {
		//eg: MATCH (cloudAtlas {title: "Cloud Atlas"}) RETURN cloudAtlas
        try {
		StatementResult result = 
			runCypherCommand("MATCH (node { id: \"" + nodeId + "\"}) RETURN node");
		
		// This is where it gets tricky. The result is what we get back
		// from the query. .single() return the first thing in the query (the node we wanted),
		// .get(0) is from the Record given by single (i dont actually know what Record is)
		// .asNode() gives us a neo4jnode object. With this, we can access data from the node. More on how
		// to do this later.
		return result.single().get(0).asNode();
        } catch (NoSuchRecordException e) {
			return null;
		}
	}
	
	// Find and return a list of nodes containing all the relationships a node has.
	public List<Node> findNodeRelationships(String nodeId) {
		// eg:
		//MATCH (director { name: 'Oliver Stone' })--(movie)
		//RETURN movie.title
		//Returns all the movies directed by 'Oliver Stone'.
		 
		StatementResult result = 
			runCypherCommand("MATCH (node { id: \"" + nodeId + "\"}) --(connected) RETURN connected");
		
		// Create a blank list of nodes.
		List<Node> nodes = new ArrayList<>();
		// result.list() is all the records in the result.
		// use this to get each node from each record, and add each node to the list.
		for(Record record : result.list()) {
			nodes.add(record.get(0).asNode());
		}
		return nodes;
	}
	// function used to verify a relation between movie and actor
	public boolean checkRelationship(String actorId, String movieId) {
		// get a list of all movies related to the actor
		List<Node> relatedMovies = findNodeRelationships(actorId);
		// iterate through all of the movies to check if an id matches up
		for (int i = 0; i < relatedMovies.size(); i++) {
			if (relatedMovies.get(i).asMap().get("id").equals(movieId)){
				return true;
			}
		}
		return false;
	}
	
	// used to compute bacon number
	public int getBaconNumer(String actorId) {
		int baconNumber = 0;
		// find actor node via id
		Node actorNode = findNodeById(actorId);
		String potentialActor = (String) actorNode.asMap().get("name");
		System.out.println(potentialActor);
		// if the actor id belongs to Kevin Bacon, over and cancelled.
		if (potentialActor.equals("Kevin Bacon")) {
			baconNumber = 0;
		} else {
			// run a query to get the path from passed id to Kevin Bacon
			// assuming that Kevin Bacon is in the query
			StatementResult path = runCypherCommand("MATCH b=shortestPath((a:actor)-[*]-(bacon:actor)) WHERE a.name =\"" + potentialActor + "\" AND bacon.name = \"Kevin Bacon\" RETURN b");
			// a StatementResult is essentially a steam of "records," where records are
			// a form of an ordered map (key/value pairs), StatementResults also have a method
			// called list() which stores the entire result stream in a list, however this
			// can take quite a long time. However, if we've returned a query, we know that
			// the path is finite. So in this case, using the list() method works.
			List<Record> records = path.list();
			
			System.out.println(records.size());
			System.out.println(records.get(0).get(0).asPath().length());
			
			int pathLen = records.get(0).get(0).asPath().length();
			// when traversing the path, it follows the format of actor -> movie -> actor -> movie,
			// with the end actor being Kevin Bacon. Subtract one from the size to account for Kevin
			// Bacon, then divide by 2 to account for the removal of movie nodes.
			baconNumber = pathLen / 2;
		}
		
		return baconNumber;
	}
	// create a function to get actor and movie nodes within
	// the bacon path separately
	public List<String> getBaconIdList(String actorId){
		Node actorNode = findNodeById(actorId);
		String potentialActor = (String) actorNode.asMap().get("name");
		List<String> idList = new ArrayList<String>();
		// if the actor id belongs to Kevin Bacon, over and cancelled.
		if (potentialActor.equals("Kevin Bacon")) {
			// return empty bacon path
			;
		} else {
			// run the query for the path and get a list representation
			StatementResult path = runCypherCommand("MATCH b=shortestPath((a:actor)-[*]-(bacon:actor)) WHERE a.name =\"" + potentialActor + "\" AND bacon.name = \"Kevin Bacon\" RETURN b");
			List<Record> records = path.list();
			Iterable<Node> nodes = records.get(0).get(0).asPath().nodes();
			for(Node node : nodes) {
				idList.add((String) node.asMap().get("id"));
			}
			System.out.println(idList.toString());
		}
	    return idList;
	}
	
	
	// Next I'm gonna show you how to access data from a node. Open GetActorApi.java.
	
	
	
	
	
	
	
}
