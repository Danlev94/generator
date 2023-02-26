from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ["OPEN_API_KEY"]
model_engine = "text-davinci-002"
max_tokens = 200

@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])

def home():
    if request.method == 'POST':
        business_idea = request.form['business_idea']
        country = request.form['country']
        budget = request.form['budget']
        profit = request.form['profit']

        # generate statements for business idea
        statement_output = generate_statements(business_idea)

        # perform market analysis for business idea in country
        market_analysis_output = market_analysis(business_idea, country)

        # perform financial analysis for business idea in country with budget and profit inputs
        financial_analysis_output = financial_analysis(business_idea, country, budget, profit)

        # render template with outputs
        return render_template('output.html', statement_output=statement_output, 
                               market_analysis_output=market_analysis_output, 
                               financial_analysis_output=financial_analysis_output)

    # render the home page with empty outputs
    return render_template('form.html')

def generate_statements(business_idea):
    prompt = f"Generate vision, mission and values for a business idea: {business_idea}"
    return ai(prompt)

def market_analysis(business_idea, country):
    prompt = f"Perform a market analysis (market potential, competitors, resources needed) for the following business idea {business_idea} in the following country: {country}"
    return ai(prompt)

def financial_analysis(business_idea, country, budget, profit):
    prompt = f"Perform a financial analysis (spending review, due diligence, inventory) for the following business idea {business_idea} in the following country: {country}. My budget is: {budget} and I want to have a yearly profit of {profit}. I want you to tell me if it is feasible to reach this profitability and how."
    return ai(prompt)

def ai(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
    )

    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)
 