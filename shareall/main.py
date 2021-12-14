from flask import Flask, send_file, send_from_directory, render_template, url_for, flash, redirect, jsonify, request
import os
import pathlib
import socket
from extensions_categorizer import get_extension_icon

HOSTNAME = socket.gethostname()
LOCAL_IP = socket.gethostbyname(HOSTNAME)
BASE_DIR = pathlib.Path(__file__).resolve(strict=True).parent
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)


def reduce_file_name(filename):
    if len(filename) >= 20:
        filename = filename[0:10] + '...' + filename[-5:]
    return filename


@app.route("/", defaults={"file": None})
@app.route("/<path:file>")
def home(file):

    DEFAULT_DIR = pathlib.Path(__file__).resolve(strict=True).parent
    if not file:
        file = DEFAULT_DIR

    if os.path.isfile(file):
        return send_file(file, conditional=True)

    files = pathlib.Path(file).iterdir()
    media = []
    for f in files:
        media.append(
            {
                'filename': reduce_file_name(pathlib.Path(f).name),
                'absolutepath': pathlib.Path(f).absolute(),
                'filename_without_extenstion': pathlib.Path(f).stem,
                'is_dir': pathlib.Path(f).is_dir(),
                'extension_icon': get_extension_icon(f.name.split('.')[-1])
            })
        current_dir = pathlib.Path(file)
        parent_dir = current_dir.parent

    if request.args.get('ajax'):
        print('Ajax')
        for m in media:
            m['absolutepath'] = str(m['absolutepath'])
        return jsonify({
            "media": media,
            "current_dir": str(current_dir),
            "parent_dir": str(parent_dir)})

    return render_template('layout.html', media=media, current_dir=current_dir, parent_dir=parent_dir)


if __name__ == '__main__':
    app.run(debug=True, host=LOCAL_IP)
