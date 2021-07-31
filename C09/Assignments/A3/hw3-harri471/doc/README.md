# The Web Gallery REST API Documentation
* Note: All curl requests are based off of a Windows OS.

## Navigation API

### Read

- description: get the html page for a profile
- request `GET /gallery/:profile
	- response: 302
	- content-type: `text/plain`
		- body: (.html document) [html login page]
	- response: 200
	- content-type: `text/plain`
		- body: (.html document) [gallery page]
	- response: 404
		- body: (string) 404: Profile '[profile]' not found
		
```
> curl -b cookie.txt http://localhost:3000/gallery/username
```

- description: get html file for directory page
- request: `GET /directory`
	- response: 302
	- content-type: `text/plain`
	    - body: (.html document) [login page]
	- response: 200
	- content-type: `text/plain`
		- body: (.html document) [directory page]
		
```
> curl -b cookie.txt http://localhost:3000/directory
```

## User API

### Create

- description: sign up as a new user
- request: `POST /signup/`
	- content-type: `application/json`
	- body: object
		- username: (string) the username to create
		- password: (string) the password to set
- response: 409
	- content-type: `application/json`
	- body: (string) username [username] already exists
- response: 200
	- content-type: `application/json`
	- body: (string) username [username] signed up
	
```
> curl -c cookie.txt -X POST 
	-H "Content-Type: application/json" 
	-d "{\"username\":\"nameOfUser\",\"password\":\"passwordForUser\"}" 
	http://localhost:3000/signup/ 
```

### Read

- description: get the name of the logged in user
- request: `GET /api/loggedIn`
- response: 200
	- content-type: `application/json`
	- body: (string) [name of logged in user]
		
```
> curl -b cookie.txt http://localhost:3000/api/loggedIn`
```

- description: get a set of users
- request: `GET /api/user/[?page=0]`
- response: 401
	- content-type: `application/json`
	- body: (string) Access Denied
- response: 200
	- content-type: `application/json`
	- body: (array)
		- elements: (User)
			- _id: the username of the user
			- hash: the password of the user in salted hash form

```
> curl -b cookie.txt http://localhost:3000/api/user
```

- description: signin as an existing user
- request: `POST /signin/`
	- content-type: `application/json`
	- body: object
		- username: (string) the username to create
		- password: (string) the password to set
- response: 401
	- content-type: `application/json`
	- body: (string) access denied
- response: 200
	- content-type: `application/json`
	- body: (string) user [username] signed in
	
```
> curl -c cookie.txt -X POST 
	-H "Content-Type: application/json" 
	-d "{\"username\":\"nameOfUser\",\"password\":\"passwordForUser\"}" 
	http://localhost:3000/signin/ 
```
	
- description: sign out of the application
- request: `GET /signout/`
- response: 200
	- body: (string) user [username] signed out
	
```
> curl -b cookie.txt http://localhost:3000/signout/
```


## Image API

### Create
	
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
> curl -b cookie.txt -X POST 
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
> curl -b cookie.txt http://localhost:3000/api/image/LThxBCkmtgpLOcY8
```
	
- description: get the most recently posted image
- request:`GET /api/image/:profile/first/`
- response: 200
    - content-type: `application/json`
    - body: object
      - _id: (string) the image id
	  - title: (string) The title of the image
      - author: (string) the authors name
	  - date: (Date) the date the image was posted
	  - picture: (file) the image file posted
	 
```
> curl -b cookie.txt http://localhost:3000/api/username/image/first
```
- description: get the image posted before the image with the given id
- request:`GET /api/image/:profile/next/:_id`
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
> curl -b cookie.txt http://localhost:3000/api/image/username/next/LThxBCkmtgpLOcY8
```

- description: get the image posted after the image with the given id
- request:`GET /api/image/:profile/previous/:_id`
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
> curl -b cookie.txt http://localhost:3000/api/image/profile/previous/LThxBCkmtgpLOcY8
```
	
- description: checks if the image exists in the database
- request `GET /api/image/imageDeleted/:_id`
- response: 200
	- content-type: `application/json`
	- body: (boolean) if the image does not exist in the database
	
```
> curl -b cookie.txt http://localhost:3000/api/image/imageDeleted/LThxBCkmtgpLOcY8
```
  
### Delete

- description: delete an image from the database
- request: `DELETE /api/image/:_id`
- response: 200
	- body: (empty)
- response: 404
	- body: Image id: [id] does not exist
	
```
> curl -b cookie.txt -X DELETE http://localhost:3000/api/image/LThxBCkmtgpLOcY8
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
 > curl -b cookie.txt -X POST 
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
> curl -b cookie.txt http://localhost:3000/api/comment/tXQd24JdVUDeiH0f
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
> curl -b cookie.txt -X DELETE http://localhost:3000/api/comment/flWWzv7WRfdQh27C
```
	