package ca.utoronto.utm.mcs.api;

import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;
import org.neo4j.driver.v1.types.Node;

import ca.utoronto.utm.mcs.Neo4jMethodHandler;

public class GetMovieApi extends AbstractNeo4jApi {

	public GetMovieApi(Neo4jMethodHandler handler) {
		super(handler);
	}
	
	@Override
	public String getAction(JSONObject deserialized) throws JSONException {
		
        String id = "";
        	
        if (deserialized.has("movieId"))
            id = deserialized.getString("movieId");

        Node node = handler.findNodeById(id);
        Map<String, Object> nodeProperties = node.asMap();
        
        String responseBody = "{\n";
        
        responseBody += "\"movieId\":\"" + nodeProperties.get("id") + "\"\n";
        responseBody += "\"name\":\"" + nodeProperties.get("name") + "\"\n";
               
        java.util.List<Node> relationships = handler.findNodeRelationships(id);
        
        String actorIds = "[";
        for(int i = 0; i < relationships.size(); i ++) {
        	actorIds += "\"" + relationships.get(i).asMap().get("id") + "\"";
        	if (i < relationships.size() - 1) {
        		actorIds += ",";
        	}
        }
        actorIds += "]";
        
        responseBody += "\"actors\": " + actorIds + "\n";
        responseBody += "}";
		return responseBody;
		
	}

}
