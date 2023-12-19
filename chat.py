from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key="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"
)

messages = [{"role": "assistant", "content": "How can I help you?"}]

def get_assistant_response(user_input):
    messages.append({"role": "user", "content": user_input})
    r = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
    )
    response = r.choices[0].message.content
    messages.append({"role": "assistant", "content": response})
    return response

@app.route("/")
def home():
    return render_template("chat.html", messages=messages)

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]
    assistant_response = get_assistant_response(user_input)
    return jsonify({"assistant_response": assistant_response})

if __name__ == "__main__":
    app.run(debug=True)

