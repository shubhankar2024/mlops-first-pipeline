#Import TestClient to send simulated HTTP requests
from fastapi.testclient import TestClient
# import the application object defined in main.py
from main import app 
# Create a resuable test client for all test fucntions
client=TestClient(app)

def test_health_endpoint():
    """
    Verify that the application is running and respond to a health-check request
    """
    response=client.get("/health")
    # A successful HTTP reqeust should return status code 200
    assert response.status_code == 200

    assert response.json()=={"status":"healthy"}

def test_valid_iris_prediction():
    """
        Verify that valid flower measurements produce a prediction
    """
    payload={
        "sepal_length":4.7,
        "sepal_width":2.0,
        "petal_length":3.4,
        "petal_width":0.4
    }
    response=client.post("/predict",json=payload)
    assert response.status_code==200
    #convert the json response into a python dictionary
    result=response.json()
    #Check the response contract: both fields must exists
    assert "prediction" in result
    assert "class_name" in result

    #the predicted class must be one of the three iris classes

    assert result ["class_name"] in ["setosa","versicolor","vriginica"]
    assert result["prediction"] in [0,1,2]

def test_invalid_iris_input():
    payload={
            "sepal_length":-4.7,
            "sepal_width":2.0,
            "petal_length":3.4,
            "petal_width":0.4
        }
    response=client.post("/predict",json=payload)
    #Fast api normally returns HTTP 422 for validation error
    assert response.status_code==422
