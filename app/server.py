from flask import Flask, render_template, send_file, abort
import matplotlib.pyplot as plt
from io import BytesIO
import networkx as nx


app = Flask(__name__)

@app.route('/<page>')
def html_lookup(page):
    try:
        return render_template('{}.html'.format(page))
    except:
        abort(404)

@app.route('/<int:nodes>')
def ind(nodes):
    return render_template("image.html", nodes=nodes)

@app.route('/graph/<int:nodes>')
def graph(nodes):
    G = nx.complete_graph(nodes)
    fig = plt.figure()
    nx.draw(G)
    fig.set_facecolor("#9e999800")
    fig.set_size_inches((15, 15))
    img = BytesIO() # file-like object for the image
    plt.savefig(img) # save the image to the stream
    img.seek(0) # writing moved the cursor to the end of the file, reset
    plt.clf() # clear pyplot

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)