This is a small sample project building an API with MongoDB and FastAPI.

# How to deploy local environment and run the project:

Install the  `requirements`:
```shell
pip install -r requirements.txt
```

Configure the location of your MongoDB database.

Create a local .env file and declare a variable:
```shell
MONGODB_URL=mongodb+srv://<username>:<password>@cluster0.6qx8a.mongodb.net/?retryWrites=true&w=majority
```
Start the app:
```shell
python app/main.py
```
