from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-advice', methods=['POST'])
def get_advice():
    # Example of generating advice based on dummy data
    user_data = request.json
    advice = {"message": f"Personalized advice for {user_data['name']}!"}
    return jsonify(advice)

if __name__ == '__main__':
    app.run(debug=True)
