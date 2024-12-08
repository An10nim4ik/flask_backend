import sqlite3
import base64
from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS for cross-origin resource sharing

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the GitHub Pages frontend
CORS(app, origins=["https://an10nim4ik.github.io"])  # Replace with your GitHub Pages URL

# Route to get all media
@app.route('/get_media', methods=['GET'])
def get_media():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect("NewDbForProject.db")  # Ensure the database is uploaded to your host
        cursor = connection.cursor()

        # Fetch all media from the Media table
        cursor.execute("SELECT filename, media FROM Media")
        media_files = cursor.fetchall()

        # Prepare the response
        media_list = [
            {
                'filename': media[0],
                'media': base64.b64encode(media[1]).decode('utf-8')  # Encode BLOB to Base64
            }
            for media in media_files
        ]

        # Close the database connection
        cursor.close()
        connection.close()

        return jsonify(media_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error if something goes wrong

if __name__ == "__main__":
    app.run(debug=True)
