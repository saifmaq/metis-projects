from flask import Flask, request, render_template
from recommender import * 
from flask_pure import Pure

app = Flask(__name__)
app.config['PURECSS_RESPONSIVE_GRIDS'] = True
app.config['PURECSS_USE_CDN'] = True
app.config['PURECSS_USE_MINIFIED'] = True
Pure(app)

@app.route('/', methods=['GET', 'POST'])
def recommendation():
    if request.method == 'GET':
        return render_template('layout.html')
    if request.method == 'POST':
        text = request.form['text']
        processed_text = text.lower()
        recs = cool_music(processed_text)       
       	return render_template('results_layout.html', recs=recs)
       
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
