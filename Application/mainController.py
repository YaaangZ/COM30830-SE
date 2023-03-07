from flask import Flask, render_template
import config

app = Flask(__name__, static_url_path="/")


@app.route("/")
def main():
    return render_template("index.html", apikey=config.APIKEY)


if __name__ == '__main__':
    app.run(debug=True)
