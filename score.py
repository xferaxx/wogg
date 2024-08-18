import mysql.connector
import os


class ScoreDatabase:
    def __init__(self):
        # Connect to MySQL server
        self.connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password='',
        )
        self.cursor = self.connection.cursor()

        # Create the database if it doesn't exist
        self.create_database()

        # Connect to the specific database
        self.connection.database = os.getenv('MYSQL_DB', 'games')

        # Create the necessary tables if they don't exist
        self.create_users_table()
        self.create_scores_table()

    def create_database(self):
        database_name = os.getenv('MYSQL_DB', 'games')
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' checked/created successfully.")
        self.connection.commit()

    def create_users_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        ''')
        print("Table 'users' checked/created successfully.")
        self.connection.commit()

    def create_scores_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_scores (
                user_id INT NOT NULL,
                score INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        print("Table 'users_scores' checked/created successfully.")
        self.connection.commit()

    def get_current_score(self, user_id):
        self.cursor.execute('SELECT score FROM users_scores WHERE user_id = %s', (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_score(self, user_id, score):
        user_id = int(user_id)
        # Check if the user already has a score
        current_score = self.get_current_score(user_id)
        if current_score is None:
            # Insert a new score for the user
            self.cursor.execute('INSERT INTO users_scores (user_id, score) VALUES (%s, %s)', (user_id, score))
        else:
            # Optionally, you might want to update the existing score here
            new_score = current_score + score
            self.cursor.execute('UPDATE users_scores SET score = %s WHERE user_id = %s', (new_score, user_id))

        self.connection.commit()

    def create_user(self, username, password):
        self.cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        self.connection.commit()

    def authenticate_user(self, username, password):
        try:
            self.cursor.execute('SELECT id FROM users WHERE username = %s AND password = %s', (username, password))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def close(self):
        self.cursor.close()
        self.connection.close()
