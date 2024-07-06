from flask import Flask
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    fig = px.scatter(x=[1, 2, 3], y=[4, 5, 6])
    return fig.to_html()

if __name__ == '__main__':
    app.run(debug=True)
