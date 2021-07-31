package ca.utoronto.utm.mcs;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.stream.Collectors;

import javax.inject.Inject;

import org.bson.Document;
import org.bson.types.ObjectId;
import org.json.JSONObject;

import com.mongodb.client.FindIterable;
import com.sun.net.httpserver.HttpExchange;
import java.util.List;

public class GetHandler implements ApiMethodHandler {
	
	@Inject DatabaseDAO dao;

	@Inject GetHandler(DatabaseDAO dao) {
		this.dao = dao;
	}

	@Override
	public HttpResponse handleApiMethod(JSONObject json) {
		
		HttpResponse response =new HttpResponse();
		Document document = Document.parse(json.toString());
		
		if (document.containsKey("_id")) {
			
			String id = null;
			try {
				id = document.getString("_id");
			} catch (ClassCastException e) {
				e.printStackTrace();
				response.setResponseNumber(400);
				return response;
			}

			if (!ObjectId.isValid(id)) {
				response.setResponseNumber(400);
				return response;
			}

			Document resultDocument = dao.getDocumentById(id);
			
			if (resultDocument == null) {
				response.setResponseNumber(404);
			} else {
				String docString =  resultDocument.toJson();
				response.setResponseNumber(200);
				response.setResponseBody("{\"posts\":["+docString+"]}");
			}
			
		} else if (document.containsKey("title")) {
			String title = null;
			try {
			    title = document.getString("title");
			} catch (ClassCastException e) {
				e.printStackTrace();
				response.setResponseNumber(400);
				return response;
			}

			FindIterable<Document> resultDocuments = dao.getDocumentsWhereTitleContainsValue(title);
			
			java.util.List<String> s = new ArrayList<String>();
			for(Document doc : resultDocuments) { s.add(doc.toJson()); }
			String result = String.join(",", s);
			
			if (result.length() <= 0) {
				response.setResponseNumber(404);
			} else {
			
				response.setResponseNumber(200);
				response.setResponseBody("{\"posts\":["+result+"]}");
			}
			
		} else {
			response.setResponseNumber(400);
		}
		return response;
	}
}
