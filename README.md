This is a small sample project demonstrating how to build an API with MongoDB and FastAPI.

How to deploy local environment and run the project:

# Install the requirements:
pip install -r requirements.txt

# Configure the location of your MongoDB database:
Create a local .env file and declare a variable MONGODB_URL=mongodb+srv://<username>:<password>@cluster0.6qx8a.mongodb.net/?retryWrites=true&w=majority

# Start the service:
python app/main.py
