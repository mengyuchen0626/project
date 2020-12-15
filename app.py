from flask import Flask, request, render_template
from redis import Redis, RedisError, StrictRedis
import joblib
import pandas as pd
import random
import time

from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary
from prometheus_client import Histogram

REQUESTS = Counter('project_app_requests_total','How many times the application has been accessed')
EXCEPTIONS = Counter('project_app_exception_total','How many times the application issued an exception')

INPROGRESS = Gauge('project_app_inprogress_gauge','How many requests to the app are currently in progress')
LAST = Gauge('project_app_last_accessed_gauge','When was the application last accessed')

LATENCY = Summary('project_app_latency_summary_seconds','time needed for a request')
LATENCY_HIS = Histogram('project_app_latency_histogram_seconds','time needed for a request',buckets = [0.0001,0.001,0.01,0.1,1.0,1.5,2.0,3.0])

model = joblib.load('tweet.model')
data = pd.read_csv('./tweet_fin.csv')


app = Flask(__name__)

def get_result(text):
    if text == '':
        return ''
        
    test = text.split(' ')
    vec = model.infer_vector(doc_words=test,alpha=0.025,steps=500)
    sim = model.docvecs.most_similar([vec],topn=20)
    tweet = list(data['ori_tweet'])
    responce = []
    for count,sims in sim:
        sentence = tweet[count]
        words=''
        for word in sentence:
            words = words + word + ''
        responce.append(words)

    return responce



@app.route('/', methods=['GET', 'POST'])
def index():
    text = u''
    result = ''
    REQUESTS.inc()
    #with EXCEPTIONS.count_exceptions():
     #    if random.random() < 0.2:
     #        raise Exceptions     
    LAST.set(time.time())
    INPROGRESS.inc()
    start = time.time()
    #time.sleep(random.random())
       
    #time.sleep(5)
    if request.method == 'POST':
        text = request.form['text']
        result = get_result(text)
        return render_template('index.html',text=text,result=result)
    INPROGRESS.dec()
    lat = time.time()
    LATENCY.observe(lat - start)
    LATENCY_HIS.observe(lat - start)
    return render_template('index.html',text=text,result=result)


if __name__ == '__main__':
    start_http_server(8010)
    redis_client = StrictRedis(host='redis', port=6379)
    app.run(host='0.0.0.0')
