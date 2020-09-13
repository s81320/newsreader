from flask import Flask, render_template, url_for, request, redirect
import pyttsx3
import pandas as pd
import json
import os.path
import sys

app = Flask(__name__)

@app.route('/')
def index():
    # how many clusters are there? 
    try:
        K = sys.argv[1]
    except:
        print('Argument missing: Number of clusters. Make it an integer, please.')

    return render_template('index.html', cluster=[['image_cluster'+str(k)+'.png', k] for k in range(int(K))])

@app.route('/article/<filename>')
def article(filename):
    fn = f'{int(filename):05}'
    if os.path.isfile('html_pres/static/'+fn+'.mp3'):
        print ("mp3 file exist")
    else:
        # get article text
        fn1 = 'articles_02/'+fn+'-clean.json'
        with open( fn1 , 'r') as myfile:
        #with open('../tagesspiegel_02/'+filename+'-clean.json' , 'r') as myfile:
            data = myfile.read()
        article = json.loads(data)
        text = article['text']
        #print(text[0:30])
        # text to speach engine
        engine = pyttsx3.init()
        engine.setProperty('rate', 140)
        try:
            engine.setProperty('voice', 'com.apple.speech.synthesis.voice.anna')
        except:
            print('could not change to German language. Voice setting was done for iOS / mac.')    
        engine.save_to_file(text, 'html_pres/static/'+fn+'.mp3')
        engine.runAndWait()
        engine.stop()
    # end if

    return render_template('article.html', source=fn+'.mp3')

@app.route('/readmore/<int:id>')
def readmore(id):
    cluster = id
    file = 'html_pres/static/articles_cluster'+str(cluster)+'.csv'
    if not os.path.isfile(file):
        print(file + ' not found in ' + os.getcwd())
    df = pd.read_csv(file, sep=";")
    df1 = df[['file_name', 'title', 'image','description','cluster']]
    return render_template('readmore.html',  items=[df1.iloc[i] for i in range (len(df1))] , col_names=list(df1))

if __name__ == "__main__":
    app.run(debug=True)
