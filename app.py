from flask import Flask, render_template, request, Response
from groq import Groq
import os

os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask('__main__')

@app.route('/')
def QnA():
    return render_template('index.html')

@app.route("/answer", methods=["GET", "POST"])
def answer():
    data = request.get_json()
    message = data["message"]

    print(message)

    def generate():
        stream = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield(chunk.choices[0].delta.content.encode('utf-8')) 

    # return generate(), {"Content-Type": "text/plain"}
    return Response(generate(), content_type='text/plain; charset=utf-8')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')