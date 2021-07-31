package ca.utoronto.utm.mcs.api;

import java.io.IOException;
import java.io.OutputStream;

import org.json.JSONException;
import org.json.JSONObject;
import ca.utoronto.utm.mcs.Neo4jMethodHandler;
import ca.utoronto.utm.mcs.entities.Movie;

public class AddMovieApi extends AbstractNeo4jApi {

	public AddMovieApi(Neo4jMethodHandler handler) {
		super(handler);
	}
	
	@Override
	protected String putAction(JSONObject deserialized) throws JSONException {
		String name = "";
        String id = "";
        	
        if (deserialized.has("name"))
            name = deserialized.getString("name");

        if (deserialized.has("movieId"))
            id = deserialized.getString("movieId");
		
		Movie movie = new Movie(id, name);
		
		handler.MergeNode(movie);

		String response = "";
		return response;
	}
	protected int getResponseNumber(JSONObject deserialized) {
		try {
    	if (!(deserialized.has("name") && deserialized.has("movieId")))  {
    		// inproperly formatted
    		return 400;
        } 
		} catch (Exception e) {
			return 500;
		}
    	return 200;
    }

}
