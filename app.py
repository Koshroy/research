from flask import Flask, render_template, g, session, request, url_for, abort
import POSParser, json
import tempfile, subprocess
#import POSParser

app = Flask(__name__)

@app.route("/sentviz")
def sentviz():
    return render_template('sentviz.html')

@app.route("/sentparse", methods=['POST'])
def parse_sentence():
    t = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    t_name = t.name
    #return str(request.form['sentence'])
    sent = request.form['sentence']
    if sent == '':
        return '"error"'
    else:
        t.write(sent+'\n')
        t.close()
        p = subprocess.Popen(['sparser/lexparser-test.sh', t_name], stdout=subprocess.PIPE)
        outList = []
        for line in iter(p.stdout.readline, ''):
            outList.append(line.rstrip())
        toParse = ''.join(outList)
        p = POSParser.POSParser()
        parsedSent = p.parse(toParse)
        return json.dumps(parsedSent)
        
    

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    
