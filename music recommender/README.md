# Recommending Music using Pitchfork Reviews

For this project, I implemented unsupervised learning with non-negative matrix factorization, Flask, and HTML/CSS to build a web app that recommends albums based on an artist that is input.

#### Here is a [demo](https://drive.google.com/file/d/1CZHtyu1_EJD8BYrYWw-h_wPjgs12V5WR/view?usp=sharing) of the app. 

## In this Repository:   

### Data
* I acquired the full text of 18,393 Pitchfork reviews from [Kaggle].

### Exploratory Data Analysis / NMF Topic Modeling Modeling
* [pitchfork_eda_modeling.ipynb](https://github.com/saifmaq/metis-projects/blob/master/music%20recommender/pitchfork_eda_modeling.ipynb) 

After some cleaning and initial analysis of the data, I used NMF to perform topic and subtopic modeling on all of the reviews in the corpus. This serves as the base for the recommender. In order to glean further insights into the data, VADER was used to perform sentiment analysis. 
  
### App 
* [app.py](https://github.com/saifmaq/metis-projects/blob/master/music%20recommender/flask_app/app.py)

Flask app which allows users to enter an artist and receive 10 recommendations

* [pitchfork_data.p](https://github.com/saifmaq/metis-projects/blob/master/music%20recommender/flask_app/pitchfork_data.p)

A pickled dataframe with topic and subtopic columns for each entry

* [recommender.py](https://github.com/saifmaq/metis-projects/blob/master/music%20recommender/flask_app/recommender.py)

A python function that makes the recommendations based on the topics and subtopics of the input 

### Slides
* [slides.pdf](https://github.com/saifmaq/metis-projects/blob/master/music%20recommender/slides.pdf)

The slides used to present the project include some further observations about the data and extensive visualization performed using Tableau. 


[Kaggle]: https://www.kaggle.com/nolanbconaway/pitchfork-data