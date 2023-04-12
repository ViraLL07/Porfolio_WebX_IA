import io
import json
import os

from flask import Flask, render_template, request

app = Flask(__name__)

common = {
    'first_name': 'Shivam Bhatt',
}


@app.route('/')
def index():
    return render_template('home.html', common=common)


@app.route('/timeline')
def timeline():
    timeline = get_static_json("static/files/timeline.json")
    return render_template('timeline.html', common=common, timeline=timeline)


@app.route('/projects')
def projects():
    data = get_static_json("static/projects/projects.json")['projects']
    data.sort(key=order_projects_by_weight, reverse=True)

    tag = request.args.get('tags')
    if tag is not None:
        data = [project for project in data if tag.lower() in [project_tag.lower() for project_tag in project['tags']]]

    return render_template('projects.html', common=common, projects=data, tag=tag)


def order_projects_by_weight(projects):
    try:
        return int(projects['weight'])
    except KeyError:
        return 0

def get_static_file(path):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, path)


def get_static_json(path):
    return json.load(open(get_static_file(path)))


if __name__ == "__main__":
    print("running py app")
    app.run(host="127.0.0.1", port=5000, debug=True)
