from flask import Flask, render_template, request, Response
import os
import replicate

app = Flask(__name__)

os.environ['REPLICATE_API_TOKEN'] = 'r8_'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gender = request.form['gender']
        age = request.form['age']
        weight = request.form['weight']
        height = request.form['height']
        main_goal = request.form['main_goal']
        physical_restrictions = request.form['physical_restrictions']
        dietary_restrictions = request.form['dietary_restrictions']
        extra = request.form['extra']
        prompt = f'You are an extraordinary fitness coach and nutritionist that helps people get into shape by giving them custom weekly workout plans along with weekly meal idea/recipes that have the right nutrients to help them reach their goal. The workouts and meal plans should be tailored to an individual’s fitness goals, physical attributes, gender, physical limitations, and dietary restrictions, and more. Here is the following information to consider when giving workout/meal plans: gender: {gender}, age: {age}, weight: {weight} pounds, height (in feet): {height}, main goal: {main_goal}, physical restrictions: {physical_restrictions}, dietary restrictions: {dietary_restrictions}, something extra to consider: {extra} . Furthermore, there should be cohesion between workouts, in other words, you can’t recommend yoga one day, muscle training the next, and cycling the next day, there needs to be consistency in the workout plan, this should be mainly dictated by a persons main goal. The workout plan should have the name of the workout, and the sets and reps (or time, depending on exercise). The meals that are recommended should also include recipes on how to make such meals and adhere to any dietary restrictions a person may have, and it should cover Monday-Sunday. Now give me the weekly work out plan and weekly meal plan.'


        output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
                                input={"prompt": f"{prompt} Trainer: ",
                                       "temperature": 0.1, "top_p": 0.9, "max_length": 12800, "repetition_penalty": 1})

        full_response = ""
        for item in output:
            full_response += item

        return render_template('result.html', response=full_response)

    return render_template('index.html')

@app.route('/download_result', methods=['POST'])
def download_result():
    # Retrieve and process form data, similar to your existing code in index()
    # ...

    # Replicate API call and response processing, similar to your existing code in index()
    # ...

    full_response = ""
    for item in output:
        full_response += item

    # Create a text file with the generated response content
    filename = "generated_result.txt"
    with open(filename, "w") as file:
        file.write(full_response)

    # Create a response object to offer the file for download
    with open(filename, "rb") as file:
        response = Response(file.read(), content_type="text/plain")
        response.headers["Content-Disposition"] = "attachment; filename=generated_result.txt"

    # Remove the temporary file
    os.remove(filename)

    return response

if __name__ == '__main__':
    app.run(debug=True)

