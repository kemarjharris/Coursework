package ca.utoronto.utm.mcs;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.stream.Collectors;

import javax.inject.Inject;

import com.sun.net.httpserver.HttpExchange;

import org.bson.Document;
import org.bson.types.ObjectId;
import org.json.JSONObject;

public class DeleteHandler implements ApiMethodHandler {

	DatabaseDAO dao;

	@Inject DeleteHandler(DatabaseDAO dao) {
		this.dao = dao;
	}
	
	@Override
	public HttpResponse handleApiMethod(JSONObject json) {

		Document req = Document.parse(json.toString());
		HttpResponse r = new HttpResponse();

		if (req.containsKey("_id")) {

			String id = null;
			try {
				id = req.getString("_id");
			} catch (ClassCastException e) {
				e.printStackTrace();
				r.setResponseNumber(400);
				return r;
			}

			if (!ObjectId.isValid(id)) {
				r.setResponseNumber(400);
				return r;
			}
			Document doc = dao.getDocumentById(id);

			if (doc == null) {
				// handles entries not existing in db
				r.setResponseNumber(404);
			} else {
				// successful delete
				dao.deleteById(id);
				r.setResponseNumber(200);
			}
		} else {
			// handles bad input
			r.setResponseNumber(400);
		}
		return r;
	}

}
