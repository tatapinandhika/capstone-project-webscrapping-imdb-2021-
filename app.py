from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url = 'https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

#creating an empty list,
movie_title = []
metascore = []
rating = []
votes = []


#find your right key here
data = soup.findAll('div', attrs= {'class': 'lister-item mode-advanced'})
row_length = len(data)

for store in data:
    title = store.h3.a.text
    movie_title.append(title)
    
    rate = store.find('div', class_ = 'inline-block ratings-imdb-rating').text.replace('\n', '')
    rating.append(rate)
    
    meta  = store.find('span', class_ = 'metascore').text.replace(' ', '') if store.find('span', class_ = 'metascore') else '0'
    metascore.append(meta)
    value = store.find_all('span', attrs = {'name': 'nv'})
    
    vote = value[0].text.replace(',', '')
    votes.append(vote)
    



#change into dataframe
movie = pd.DataFrame({'Title of movie': movie_title,'Movie Rating': rating, 'Metascore': metascore, 'votes':votes})

#insert data wrangling here
movie['Movie Rating']=movie['Movie Rating'].astype('float64')
movie['Metascore']=movie['Metascore'].astype('int64')
movie['votes']=movie['votes'].astype('int64')
favorit=movie.head(7)
favorit1=favorit.set_index('Title of movie', drop=True)


#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{movie["Metascore"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = favorit1['Metascore'].plot.bar(title = 'seven most popular movie in 2021',
                xlabel = 'Title of movie',
                ylabel = 'Metascore',figsize = (10,5)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)