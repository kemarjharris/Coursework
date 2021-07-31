package ca.utoronto.utm.mcs.api;
import org.json.*;


import ca.utoronto.utm.mcs.Neo4jMethodHandler;
import ca.utoronto.utm.mcs.entities.Actor;

public class AddActorApi extends AbstractNeo4jApi {
	
	public AddActorApi(Neo4jMethodHandler neo4jMethodHandler) {
		super(neo4jMethodHandler);
	}

	protected String putAction(JSONObject deserialized) throws JSONException {
		
		String name = "";
        String id = "";
        	
        if (deserialized.has("name"))
            name = deserialized.getString("name");

        if (deserialized.has("actorId"))
            id = deserialized.getString("actorId");
		
		Actor actor = new Actor(id, name);
		handler.MergeNode(actor);
		
		return "";
	}
	
    protected int getResponseNumber(JSONObject deserialized) {
    	try {
    	if (!(deserialized.has("name") && deserialized.has("actorId")))  {
    		// inproperly formatted
    		return 400;
        } 
    	} catch (Exception e) {
    		return 500;
    	}
    	return 200;
    }

}
