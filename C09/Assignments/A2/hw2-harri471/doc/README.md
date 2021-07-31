# The Web Gallery REST API Documentation

## Image API

### Create

* Note: All curl requests are based off of a Windows OS.

- description: create a new image
- request: `POST /api/image/`
    - content-type: `application/json`
    - body: object
      - title: (string) The title of the image
      - author: (string) the authors name
	- picture: (file)The image to post
- response: 200
    - content-type: `application/json`
    - body: object
      - _id: (string) the image id
	  - title: (string) The title of the image
      - author: (string) the authors name
	  - date: (Date) the date the image was posted
	  - picture: (file) the image file posted
- response: 400
	- body: Body missing data
	
```
> curl -X POST 
	-F "picture=@[absolute file path to image]" -F "title=hello world" -F "author=me" 
	http://localhost:3000/api/image/
```

### Read

- description: get an image file
- request: `GET /api/image/:_id/`
- response: 200
	- content-type: `application/json`
	- body: (file) the image file posted
- response: 404
	- body: Image id: [id] does not exist
	
```
> curl http://localhost:3000/api/image/LThxBCkmtgpLOcY8
```
	
- description: get the most recently posted image
- request:`GET /api/image/first/`
- response: 200
    - content-type: `application/json`
    - body: object
      - _id: (string) the image id
	  - title: (string) The title of the image
      - author: (string) the authors name
	  - date: (Date) the date the image was posted
	  - picture: (file) the image file posted
	 
```
> curl http://localhost:3000/api/image/first
```
- description: get the image posted before the image with the given id
- request:`GET /api/image/next/:_id`
- response: 200
    - content-type: `application/json`
    - body: object
      - _id: (string) the image id
	  - title: (string) The title of the image
      - author: (string) the authors name
	  - date: (Date) the date the image was posted
	  - picture: (file) the image file posted
- response: 404
	- body: Image id: [id] does not exist

```
> curl http://localhost:3000/api/image/next/LThxBCkmtgpLOcY8
```

- description: get the image posted after the image with the given id
- request:`GET /api/image/previous/:_id`
- response: 200
    - content-type: `application/json`
    - body: object
      - _id: (string) the image id
	  - title: (string) The title of the image
      - author: (string) the authors name
	  - date: (Date) the date the image was posted
	  - picture: (file) the image file posted
- response: 404
	- body: Image id: [id] does not exist
	
```
> curl http://localhost:3000/api/image/previous/LThxBCkmtgpLOcY8
```
	
- description: checks if the image exists in the database
- request `GET /api/image/imageDeleted/:_id`
- response: 200
	- content-type: `application/json`
	- body: (boolean) if the image does not exist in the database
	
```
> curl http://localhost:3000/api/image/imageDeleted/LThxBCkmtgpLOcY8
```
  
### Delete

- description: delete an image from the database
- request: `DELETE /api/image/:_id`
- response: 200
	- body: (empty)
- response: 404
	- body: Image id: [id] does not exist
	
```
> curl -X DELETE http://localhost:3000/api/image/LThxBCkmtgpLOcY8
```

## Comment API

### Create

- description: create a new comment
- request: `POST /api/comment/`
    - content-type: `application/json`
    - body: object
      - imageId: (string) The id of the image the comment belongs to
      - author: (string) the commnt authors name
	  - content: (string) the content of the comment
- response: 200
    - content-type: `application/json`
    - body: object
      - _id: (string) the comment id
	  - imageId: (string) The id of the image the comment belongs to
	  - author: (string) the commnt authors name
	  - content: (string) the content of the comment
	  - date: (Date) the date the image was posted
- response: 400
	- body: Body missing data
- response: 404
	- body: Image id: [id] does not exist
	
```
 > curl -X POST 
	-H "Content-Type: application/json" 
	-d "{\"content\":\"hello world\",\"author\":\"me\",\"imageId\":\"tXQd24JdVUDeiH0f\"}" 
	http://localhost:3000/api/comment/
```

### Read

- description: get comments on an image
- request: `GET /api/comment/:_id/[?page=0]`
- response: 200
	- content-type: `application/json`
	- body: array
		- elements: (Comment)
			- _id: (string) the comment id
			- imageId: (string) The id of the image the comment belongs to
			- author: (string) the commnt authors name
			- content: (string) the content of the comment
			- date: (Date) the date the image was posted
- response: 404
	body: Image id: [id] does not exist
	
```
> curl http://localhost:3000/api/comment/tXQd24JdVUDeiH0f
```
			
### Delete
  
- description: delete comment from an image
- request: `DELETE /api/comment/:commentId`
- response: 200
	- body: object
		- _id: (string) the comment id
		- imageId: (string) The id of the image the comment belongs to
		- author: (string) the commnt authors name
		- content: (string) the content of the comment
		- date: (Date) the date the image was posted
response: 404
	- body: Comment id: [commentId] does not exist

```
> curl -X DELETE http://localhost:3000/api/comment/flWWzv7WRfdQh27C
```
	