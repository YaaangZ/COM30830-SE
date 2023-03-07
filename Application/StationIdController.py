from flask import Flask, render_template
import config

app = Flask(__name__, static_url_path="/stations/<int:station_id>")


@app.route("/stations/<int:station_id>")
def main():
    return render_template("stations.html", apikey=config.APIKEY)


if __name__ == '__main__':
    app.run(debug=True)