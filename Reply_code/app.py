from flask import Flask, request, render_template_string
from openai import OpenAI
import markdown

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    key = ""
    title = ""
    description = ""
    output = ""
    if request.method == "POST":
        if "suggestion" in request.form:
            context = request.form["title"]
            reply = request.form["description"]

            client = OpenAI(
                api_key=key,
            )

            prompt = f"""

            You are a friendly AI assistant helping with making effective posts in a canvas discussions.

            Abide by the following instructions:

                1)Check semantics for all potential posts:
                    AI assistant suggestion:
                        - If there is no issue, leave this blank
                        - If there is a negative connotations, or if the post has elements that could be offensive or not helpful give a warning with a rephrased message

                2)Check for clarity. Is the sentence structure clear. Are there grammatical errors, is the idea coherent and well put.
                    AI assistant suggestion:
                        - If there is no issue, give no suggestions for clarity
                        - if there are issues with clarity give suggestion on what items in the post can be clarified.
                3)Check for effectiveness
                    For replies, they should follow guidelines for effective reply.
                        Effective reply:
                            - Focus on the topic mentioned in the discussion post, and is specific to the post it is replying to
                            - Follows effective discussion guidelines
                                - Effective discussion:
                                    - Clearly State the Main Idea or Argument
                                    - Provide Supporting Evidence or Examples
                                    - Includes Open-Ended Follow-Up Questions

                    AI assistant suggestion:
                        - Based on the rules above for effective reply, give suggestions on which items in the post can be improved be more effective.

            Keep all replies in point form. Keep the identation. Only give suggestion, do not explain your suggestions.

            reply:
            {reply}

            The reply is to this discussion post:
            {context}

            """

            chat_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            output_text = chat_completion.choices[0].message.content

            # Replace the following line with your code logic
            # output = display(Markdown(output_text))
            output = markdown.markdown(output_text)
        elif "clear" in request.form:
            title = ""
            description = ""
            output = ""

    return render_template_string('''
        <html>
            <head>
                <title>Canvas Discussion</title>
                <style>
                    body {font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px;}
                    .container {width: 50%; margin: auto; background: #fff; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1);}
                    h1 {text-align: center;}
                    label {font-weight: bold;}
                    input[type="text"] {width: 100%; padding: 10px; margin: 10px 0;}
                    button {padding: 10px 20px; margin: 10px 5px; cursor: pointer;}
                    .output {margin: 20px 0; padding: 10px; background: #e9ecef; border-radius: 5px;}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Canvas Discussion</h1>
                    <form method="post">
                        <label for="title">Discussion Before</label>
                        <input type="text" id="title" name="title" value="{{ title }}">
                        <br>
                        <label for="description">New Reply</label>
                        <input type="text" id="description" name="description" value="{{ description }}">
                        <br>
                        <div class="output">{{ output|safe }}</div>
                        <br>
                        <button type="submit" name="suggestion">Suggestion</button>
                        <button type="submit" name="clear">Clear</button>
                    </form>
                </div>
            </body>
        </html>
    ''', title=title, description=description, output=output)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
