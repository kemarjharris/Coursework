package ca.utoronto.utm.mcs.api;

import ca.utoronto.utm.mcs.Neo4jMethodHandler;

import java.util.List;
import java.util.Map;

import org.json.JSONException;
import org.json.JSONObject;
import org.neo4j.driver.v1.types.Node;

public class ComputeBaconPathApi extends AbstractNeo4jApi{
	public ComputeBaconPathApi(Neo4jMethodHandler handler) {
		super(handler);
	}
	
	
	@Override
	public String getAction(JSONObject deserialized) throws JSONException{
		String actorId = "";
		if (deserialized.has("actorId"))
            actorId = deserialized.getString("actorId");
		
		int baconNumber = handler.getBaconNumer(actorId);
	    List<String> idList = handler.getBaconIdList(actorId);
		int i = 0;
	    String responseBody = "{\n";
		responseBody += "\t" + "\"baconNumber\":\"" + baconNumber + "\"\n";
		responseBody += "\t" + "\"baconPath\": [\n";
		responseBody += "\t" + "\t" + "{\n";
		for (i = 0; i < idList.size() - 1; i++) {
			if (i % 2 == 0) {
				responseBody += "\t" + "\t" + "\t" + "\"actorId:\" " + "\""  + idList.get(i) + "\""+ "\n";
			} else {
				responseBody += "\t" + "\t" + "\t" + "\"movieId:\" " + "\""  + idList.get(i) + "\""+ "\n";
				responseBody += "\t" + "\t" + "},\n";
			}
		}
		responseBody += "\t" + "\t" + "{\n";
		responseBody += "\t" + "\t" + "\t" + "\"actorId:\" " + "\""  + idList.get(i) + "\""+ "\n";
		responseBody += "\t" + "\t" + "}\n";
		
		responseBody += "\t]\n";
		responseBody += "}";
		
		return responseBody;
		
	}

}
