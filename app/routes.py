from flask import render_template,request
from app import app
from app.summarizer import Summarizer,nlp
from app.forms import Submitted_field

@app.route('/',methods=['GET','POST'])
def index():
    summarizer=Summarizer(nlp)
    form=Submitted_field(size=600)
    if form.validate_on_submit():
        text=request.form['text']
        num_sentences=int(request.form['num_sentences'])
        word_wts,sent_wts,sent,summary=summarizer.summarize_text(text,num_sentences)
        top_five_words=sorted(word_wts, key=word_wts.get, reverse=True)[:5]
        sentence_weights=[value for key,value in sent_wts.items()]
        weighted_sentence_weights=[value/max(sentence_weights) for value in sentence_weights]
        sentences_with_weights=list(zip(sent,weighted_sentence_weights))
        return render_template('summary.html',text=summary,top_words=top_five_words,sentence_weights=sentence_weights,sents=sentences_with_weights)
    return render_template('index.html',text='',form=form)

@app.route("/summary")
def summary():
    return render_template("summary.html")