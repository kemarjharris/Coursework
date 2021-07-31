package ca.utoronto.utm.mcs;

import javax.inject.Inject;

import java.io.IOException;
import java.io.OutputStream;
import java.util.List;

import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONArray;
import org.bson.Document;
import org.bson.types.ObjectId;

import ca.utoronto.utm.mcs.JSONExchangeConverter;
import com.sun.net.httpserver.HttpExchange;
import ca.utoronto.utm.mcs.HttpResponse;
import ca.utoronto.utm.mcs.DatabaseDAO;

public class PutHandler implements ApiMethodHandler {


	DatabaseDAO dao;

	@Inject PutHandler(DatabaseDAO dao) {
		this.dao = dao;
	}

	@Override
	public HttpResponse handleApiMethod(JSONObject inJson) throws IOException, JSONException {
		JSONObject json = new JSONObject();
		JSONObject jsonResponse = new JSONObject();
		HttpResponse response = new HttpResponse();
		Document body = Document.parse(inJson.toString());

		try {

			if (body.containsKey("title") 
			&& body.containsKey("author") 
			&& body.containsKey("content") 
			&& body.containsKey("tags")) {
				
				String title = body.getString("title");
				String author = body.getString("author");
				String content = body.getString("content");
				
				List<String> tags = body.getList("tags", String.class);
				// print out the values for testing purposes
				// put everything into the json

				// push everything into the jsonbody
				json.put("title", title);
				json.put("author", author);
				json.put("content", content);
				json.put("tags", tags);
				// use the dao to add posts to database
				ObjectId JSONResponseId = dao.putDocument(json);
				jsonResponse.put("_id", JSONResponseId);
				response.setResponseNumber(200);
				response.setResponseBody(jsonResponse.toString());
			} else {
				response.setResponseNumber(400);
			}
		} catch (ClassCastException e) {
			e.printStackTrace();
			response.setResponseNumber(400);
		}
		return response;
	}
}
