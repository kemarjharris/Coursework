package ca.utoronto.utm.mcs;

import javax.inject.Inject;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import org.bson.types.ObjectId;
import org.json.JSONObject;

import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONArray;

import com.mongodb.client.model.Filters;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoClient;
import com.mongodb.client.model.InsertOneOptions;

public class DatabaseDAO {

	public MongoCollection<Document> posts;
	
	@Inject
	public DatabaseDAO(MongoClient client) {
		posts = client.getDatabase("csc301a2").getCollection("posts");
	}
	
	public FindIterable<Document> getDocumentsWhereTitleContainsValue(String value) {
		return posts.find(Filters.regex("title", value));
	}
	
	public Document getDocumentById(String id) {
		return posts.find(Filters.eq("_id", new ObjectId(id))).first();
	}
	
	public Document deleteById(String id) {
		return posts.findOneAndDelete(new Document("_id", new ObjectId(id)));
	}
	
	public ObjectId putDocument(JSONObject json) {
		Document document = Document.parse(json.toString());
		posts.insertOne(document);
		return document.getObjectId("_id");
	}
	
}
