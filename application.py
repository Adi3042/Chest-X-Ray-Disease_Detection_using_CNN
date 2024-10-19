from flask import Flask,request,render_template,jsonify
from logging import log

application = Flask(__name__)
app = application

@app.route('/', methods=['GET','POST'])
def home_page():
    try:
        results = ""
        if request.method=='GET':
            return render_template('index.html')
        
        else:
            file = request.files['file']
            file.save(file.filename)
            results = "File uploaded successfully"
            return render_template('index.html',results=results)
        
    except Exception as e:
        log.error("Error in home_page: "+str(e))
        return render_template('index.html',results="Error in uploading file")
    

if __name__ == '__main__':
    application.run(host = "0.0.0.0", debug = True, port = 5000)