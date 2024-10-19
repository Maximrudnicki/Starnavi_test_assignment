# Test assignment for Starnavi by Maxim Rudnitskiy

## How to start

Make sure that you cloned the project: git clone https://github.com/Maximrudnicki/Starnavi_test_assignment.git
In order to start the app you need to enter the following command: cd Starnavi_test_assignment 
And then this one: docker-compose up -d
To stop the containers: docker-compose down

1. **Clone the Project**
    ```bash
    git clone https://github.com/Maximrudnicki/Starnavi_test_assignment.git
    cd Starnavi_test_assignment
    ```
2. **Running the App with Docker**

   Build and start the application using Docker:
    ```bash
    docker-compose up -d
    ```
3. **Running the App Locally and running the tests**

   Alternatively, you can run the application on your local machine.

   - Ensure Python and pip are installed:
     ```bash
     python --version
     pip --version
     ```

   - Install the necessary dependencies:
     ```bash
     pip install --no-cache-dir -r requirements.txt
     ```

   - Create a `.env` file in the root directory of the project and add the following fields:
     ```plaintext
     SECRET_KEY=4A1DB3D977D98AFFDC115327EB52A6B384C39FB71E6B859FDC3800E12B9E13DE
     ALLOWED_ORIGINS=*

     DB_HOST=
     DB_PORT=
     DB_NAME=
     DB_USER=
     DB_PASS=
    ```

   - Apply migrations and insert some data in database:
     ```bash
     alembic upgrade head
     python seed.py
     ```

    - Run tests:
     ```bash
     pytest tests/
     python seed.py
     ```
     **Note:** Unfortunately, the data from the db is simply droped after tests (even between test cases)

    - Start the app localy:
     ```bash
     uvicorn main:app --host 127.0.0.1 --port 8000
     ```
     **Note:** Unfortunately, there will be issues with celery and redis because I used docker to run redis/celery. But you can still use the app. Just keep in mind that in this case the auto reply will not work.
4. **Access the Application**

   Once everything is up and running, visit [http://localhost:8000](http://localhost:8000) in your web browser.

   Alternatively, you can test the API using Postman by visiting this collection: [SCA Postman Collection](https://www.postman.com/navigation-engineer-62741940/test-assignment-for-starnavi-by-maxym-rudnytskyi/overview)
4. **Stop the Application**
    If you need to stop the app, just press Ctrl+C or enter this for docker:
     ```bash
     docker-compose down
     ```

##### Once containers are up, just visit localhost:8000 or check the postman here: https://www.postman.com/navigation-engineer-62741940/test-assignment-for-starnavi-by-maxym-rudnytskyi/overview

Keep in mind that you need to be signed in in Postman and create a fork before using the application

### Additional Information

Also, I need to mention that you can check [comments daily breakdown](http://127.0.0.1:8000/api/v1/comments-daily-breakdown?date_from=2023-07-17&date_to=2024-11-19)

Of course there is a filter for unappropriate comments and posts. Posts are deleted and comment are banned and shadowed right after creation and checking (you cannot get banned comments using the API, you would need to make a request directly to the DB or use pgadmin to see unappropriate content). The feature was impemented using OpenAI API, you can check the code in `utils/filter.py`

There is no any of the unappropriate content (comment or post) but you can make sure that everything is implemented by your own.

### Auto-Reply Implementation

You can check how the auto reply is implemented using celery tasks here: `tasks/celery_tasks.py`. Also, the auto_reply function is called from the service layer

###  Technologies Used

I used following technologies to build the project: `FastAPI, SQLAlchemy, Alembic, Docker, PostgreSQL, Redis, Celery, OpenAI API`.