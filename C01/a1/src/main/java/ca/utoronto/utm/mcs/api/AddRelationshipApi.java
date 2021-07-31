package ca.utoronto.utm.mcs.api;

import org.json.JSONException;
import org.json.JSONObject;
import org.neo4j.driver.v1.types.Node;

import ca.utoronto.utm.mcs.Neo4jMethodHandler;

public class AddRelationshipApi extends AbstractNeo4jApi {

	public AddRelationshipApi(Neo4jMethodHandler handler) {
		super(handler);
	}
	
	@Override
	protected String putAction(JSONObject deserialized) throws JSONException {
		
		String actorId = "";
        String movieId = "";
        	
        if (deserialized.has("movieId"))
            movieId = deserialized.getString("movieId");

        if (deserialized.has("actorId"))
            actorId = deserialized.getString("actorId");
		
		handler.CreateRelationship(actorId, "actor", "ACTED_IN", movieId, "movie");
		
		return "";
	}

@Override
	protected int getResponseNumber(JSONObject deserialized) {
		try {
			if (!(deserialized.has("movieId") && deserialized.has("actorId"))) {
				return 400;
			} 
			
			Node movieNode = handler.findNodeById(deserialized.getString("movieId"));
			Node actorNode = handler.findNodeById(deserialized.getString("actorId"));
			
			if (movieNode == null || actorNode == null) {
				return 404;
			}
			
			if (!movieNode.hasLabel("movie") || !actorNode.hasLabel("actor")) {
				return 400;
			}
		} catch (Exception e)
		{
			return 500;
		}
		return 200;
	}

}
