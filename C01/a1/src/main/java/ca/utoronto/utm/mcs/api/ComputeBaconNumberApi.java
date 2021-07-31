package ca.utoronto.utm.mcs.api;

import ca.utoronto.utm.mcs.Neo4jMethodHandler;

import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;
import org.neo4j.driver.v1.types.Node;

public class ComputeBaconNumberApi extends AbstractNeo4jApi {
	public ComputeBaconNumberApi(Neo4jMethodHandler handler) {
		super(handler);
	}
	
	@Override
	public String getAction(JSONObject deserialized) throws JSONException{
		String actorId = "";
		if (deserialized.has("actorId"))
            actorId = deserialized.getString("actorId");
		
		int baconNumber = handler.getBaconNumer(actorId);
		
		String responseBody = "{\n";
		responseBody += "\t" + "\"baconNumber\": \"" + baconNumber + "\"\n";
		responseBody += "}";
		
		return responseBody;
	}

}
