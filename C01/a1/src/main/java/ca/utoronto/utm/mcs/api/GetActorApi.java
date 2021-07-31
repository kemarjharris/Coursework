package ca.utoronto.utm.mcs.api;

import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;
import org.neo4j.driver.v1.types.Node;



import ca.utoronto.utm.mcs.Neo4jMethodHandler;

public class GetActorApi extends AbstractNeo4jApi {

	public GetActorApi(Neo4jMethodHandler handler) {
		super(handler);
	}
	
	@Override
	public String getAction(JSONObject deserialized) throws JSONException {
		
        String id = "";
        	
        if (deserialized.has("actorId"))
            id = deserialized.getString("actorId");

        // Get node using handler
        Node node = handler.findNodeById(id);
        // Here's the important part. See this .asMap() function?
        // This returns all nodes properties as a Map (think of it like
        // a python dictionary) of key value pairs, with the keys being
        // node attributes (id, name, etc.) and the values being the
        // value of those attributes.
        Map<String, Object> nodeProperties = node.asMap();
        
        String responseBody = "{\n";
        // Add the actorId and id value from the map.
        // Repeat the same logic with name.
        // also note how I used \"? That escapes the quote, and is very important.
        // Its the difference between sending '{a:b}' and '{"a":"b"}'
        responseBody += "\"actorId\":\"" + nodeProperties.get("id") + "\"\n";
        responseBody += "\"name\":\"" + nodeProperties.get("name") + "\"\n";
               
        java.util.List<Node> relationships = handler.findNodeRelationships(id);
        
        // a DUTTY toString for the nodeId list. there may be a better way to do this
        // but idk what it is.
        String movieIds = "[";
        // iterate through thelist of nodes, convert them to their map representations, and
        // add their ids to the response body
        for(int i = 0; i < relationships.size(); i ++) {
        	movieIds += "\"" + relationships.get(i).asMap().get("id") + "\"";
        	if (i < relationships.size() - 1) {
        		movieIds += ",\n";
        	}
        }
        movieIds += "\n]";
        
        responseBody += "\"movies\": " + movieIds + "\n";
        responseBody += "}";
        // Remember the template pattern! This value is returned to the handleGet()
        // function in the parent class!
		return responseBody;
		
	}
	@Override
	protected int getResponseNumber(JSONObject deserialized) {
		try {
			if (!(deserialized.has("actorId"))) {
				return 400;
			} else if (handler.findNodeById(deserialized.getString("actorId")) == null) {
				return 404;
			}
		} catch (Exception e) {
			return 500;
		}
		
		return 200;
	}
}

	// I think thats about it. If you need any clarification on anything that I've done,
	// text me. I highly recommend commenting AddMovieApi and GetMovieApi so you know what you're
	// doing.
	

