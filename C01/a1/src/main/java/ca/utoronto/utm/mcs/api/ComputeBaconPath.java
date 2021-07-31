package ca.utoronto.utm.mcs.api;

import ca.utoronto.utm.mcs.Neo4jMethodHandler;

import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;
import org.neo4j.driver.v1.types.Node;

public class ComputeBaconPath extends AbstractNeo4jApi{
	public ComputeBaconPath(Neo4jMethodHandler handler) {
		super(handler);
	}
	
	@Override
	public String getAction(JSONObject deserialized) throws JSONException{
		String actorId = "";
		int baconNumber = 0;
		if (deserialized.has("actorId"))
            actorId = deserialized.getString("actorId");
		
		String responseBody = "{\n";
		return responseBody;
	}

}
