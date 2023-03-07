from flask import Flask, render_template
import config

app = Flask(__name__, static_url_path="/occupancy/<int:station_id>")


@app.route("/occupancy/<int:station_id>")
def main():
    return render_template("occupancy.html", apikey=config.APIKEY)


if __name__ == '__main__':
    app.run(debug=True)
