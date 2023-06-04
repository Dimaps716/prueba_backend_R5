# REST API for R5

## Features
The backend allows users to:

Register in the application by providing an email address and a password.

Create, read, update, and delete information for each of the models: users, library.
### Instalación 🔧

In the terminal located in the folder where you want to save this project, execute the following.
```
git clone https://github.com/Dimaps716/backend_prueba_tecnica
```
move to developer branch.
```
git checkout developer
```
run project dependencies.

_the project is configured to run migrations and upload information to the database_
```
To create the database, execute the SQL file located in the "utils" folder.
```
this will activate the servers
```
pip install -r requirements.txt

uvicorn main:app --reload
```
check the documentation

_in this other you will see the API documentation_
```
http://localhost:8000/docs
```
_create a user_
```
http://localhost:8000/registry/create
```
_Search for a book_
```
http://localhost:8000/library/{book}/searching
```

## Built with 🛠️

* [sqlalchemy] (https://www.sqlalchemy.org/)
* [fastapi] (https://fastapi.tiangolo.com/)
* [python] (https://www.python.org/)


## Authors ✒️


* ** Dimanso perez ** - * Initial Work * - [Dimaps716] (https://github.com/Dimaps716)


## License 📄

This project is under the License (Your License) - see the  (LICENSE.md) file for details

## Expressions of Gratitude 🎁

* Tell others about this project 📢
* Invite a beer 🍺 or a coffee ☕ to someone on the team.
* Give thanks publicly 🤓.




---
⌨️ with ❤️ by [Dimaps716] (https://github.com/Dimaps716) 😊