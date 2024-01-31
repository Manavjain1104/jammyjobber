from summariser import create_summary_and_embedding
from flask import Flask, request, jsonify

app = Flask(__name__)


# Define a route for your function
@app.route("/summariser", methods=["POST"])
def handle_request():
    try:
        # Get parameters from the request
        data = request.get_json()
        parameters = data.get("text")

        # Call your function
        summary, embedding = create_summary_and_embedding(parameters)

        # Return the result as JSON
        return jsonify({"summary": summary, "embedding": embedding.tolist()})
    except Exception as e:
        # Handle errors gracefully
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True)
