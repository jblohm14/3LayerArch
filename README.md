# 1. Code Modifications

## 1.1 User Creation
The server provided by this assignment allows user profiles to be created by making a POST request to the HTTP endpoint `http://127.0.0.1:5000/user`. For this I used the REST Client VScode extension.   

Below is a single POST request where I created a user named John Lennon. 
```
POST http://127.0.0.1:5000/user  HTTP/1.1
content-type: application/json

{
    "user_name": "jlennon",
    "first_name": "John",
    "last_name": "Lennon"
}
```
Similarly, I added a user profile for each of The Beatles. These functions are stored in the file [create-users.rest](create-users.rest).  
The server also allows a way to query a single user's information by ID. For this I used a GET request to fetch the profile information for a user with the ID 1.

```
GET http://127.0.0.1:5000/user/1
```
This is the corresponding response from the server. 
```
HTTP/1.1 200 OK
Server: Werkzeug/2.2.3 Python/3.8.10
Date: Mon, 16 Mar 2026 22:59:34 GMT
Content-Type: application/json
Content-Length: 115
Connection: close

{
  "first_name": "John",
  "last_name": "Lennon",
  "role": "regular",
  "user_id": 1,
  "user_name": "jlennon"
}
```
## 1.2 Modifications
My goal for this assignment is to add functionality to support returning all users.
For this I needed to modify each of the layers to add this functionality.  

### Persistence
`storage.py`: added an abstract function definition
```
def get_all(self) -> [User]:
    raise NotImplementedError()
```
`inmemory_storage.py`: added a concrete function implementation that persists data in RAM
```
def get_all(self):
    users = []
    for i in range(0, len(self._data)):
        users.append(self.get(i))
    return users
```
`sqlite_storage.py`: added a concrete function implementation that persists data in a database
```
def get_all(self):
    cursor = self._connection.cursor()
    cursor.execute(self.GET_ALL_USERS_STATEMENT)
    rows = cursor.fetchall()
    cursor.close()
    self._connection.commit()

    return [self._row_to_user(row) for row in rows]
```

### Business
`user_handler.py`: added a function to get all users and format them correctly
```
def get_all_users(self):
    users = self.user_service.get_all()

    user_data = []
    for user in users:
        user_data.append(user.__dict__)

    return user_data
```
`user_service.py`: added a function to return all users
```
def get_all(self) -> []:
    users = self._user_storage.get_all()
    if len(users) is None:
        raise UserNotFoundException()
    return users
```

### Presentation

`controller.py`: added a function to create a new endpoint /users
```
@controller.route("/users")
def get_all_users():
    try:
        user_data = user_handler.get_all_users()
    except UserNotFoundException:
        return jsonify({"message": "User not found", "user_id": user_id}), 404
    return jsonify(user_data)
```

# 2. Layered Architecture Explanation
This assignment explores the use of a layered software architecture approach. To add a feature such as `get_all_users` I needed to modify each of the layers.
## 2.1 Persistence
The persistence layer is responsible for implementing how the data is persevered. The reference project supports two different storage methods. The first method keeps data in memory. This is useful for testing purposes. I used it to validate higher levels before I researched SQLite which is used in the second method. An abstract class `UserStorage` isolates the upper layers from how the storage method is implemented. This is important in software design. An upper layer need not care whether the data is kept in memory or written to a database. 
## 2.2 Business
The business layer encompasses the main logic of this server. It is responsible for implementing all the main functionality. In this example that includes handling external requests from the presentation layer and accessing the data from the persistence layer, and then validating the data returned. 
## 2.3 Presentation
The presentation, in this case, is the simplest of the layers. Its only responsibility is to create endpoints for an external client to interact with the business layer. The presentation layer gates the user from calling business logic directly. It contains only the functionality the developers wish to expose. 

# 3. Execution Proof
With the modifications above I ran the server again. This time I made a GET request to the newly created endpoint.
```
GET http://127.0.0.1:5000/users
```
Below is the corresponding response from the server. Notice now that the complete list of The Beatles was return as a list of Users.
```
HTTP/1.1 200 OK
Server: Werkzeug/2.2.3 Python/3.8.10
Date: Tue, 17 Mar 2026 00:06:19 GMT
Content-Type: application/json
Content-Length: 529
Connection: close

HTTP/1.1 200 OK
Server: Werkzeug/2.2.3 Python/3.8.10
Date: Tue, 17 Mar 2026 00:18:46 GMT
Content-Type: application/json
Content-Length: 529
Connection: close

[
  {
    "first_name": "John",
    "last_name": "Lennon",
    "role": "regular",
    "user_id": 1,
    "user_name": "jlennon"
  },
  {
    "first_name": "Paul",
    "last_name": "McCartney",
    "role": "regular",
    "user_id": 2,
    "user_name": "pmccart"
  },
  {
    "first_name": "George",
    "last_name": "Harrison",
    "role": "regular",
    "user_id": 3,
    "user_name": "gharris"
  },
  {
    "first_name": "Ringo",
    "last_name": "Starr",
    "role": "regular",
    "user_id": 4,
    "user_name": "rstarr"
  }
]
```