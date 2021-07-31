package ca.utoronto.utm.mcs.api;

import ca.utoronto.utm.mcs.Neo4jMethodHandler;

import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;
import org.neo4j.driver.v1.types.Node;

public class HasRelationshipApi extends AbstractNeo4jApi {

	public HasRelationshipApi(Neo4jMethodHandler handler) {
		super(handler);
	}
	@Override
	public String getAction(JSONObject deserialized) throws JSONException{
		
		String actorId = "";
        String movieId = "";
        	
        if (deserialized.has("movieId"))
            movieId = deserialized.getString("movieId");

        if (deserialized.has("actorId"))
            actorId = deserialized.getString("actorId");
        
        boolean result = handler.checkRelationship(actorId, movieId);

        String responseBody = "{\n";
        responseBody += "\t" + "\"actorId\": \"" + actorId + "\",\n";
        responseBody += "\t" + "\"movieId\": \"" + movieId + "\",\n";
        responseBody += "\t" + "\"hasRelationship\": " + Boolean.toString(result) + "\n";
        responseBody += "}";
        
		return responseBody;
	}

	protected int getResponseBody(JSONObject deserialized) {
	    
		try {
			if (!(deserialized.has("movieId") && deserialized.has("actorId"))) {
				return 400;
			} 
			
			Node movieNode = handler.findNodeById(deserialized.getString("movieId"));
			Node actorNode = handler.findNodeById(deserialized.getString("actorId"));
			
			if (movieNode == null || actorNode == null) {
				return 404;
			}
			
		} catch (Exception e) {
			return 500;
		}
		return 200;	
	}
}
