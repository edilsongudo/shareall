from flask import (
    Flask,
    send_file,
    send_from_directory,
    render_template,
    url_for,
    flash,
    redirect,
    jsonify,
    request,
)
import os
import pathlib
import socket
from utils import (
    get_extension_icon,
    reduce_file_name,
    generate_qr_code,
    is_wifi_turned_on,
)
import requests
import qrcode
# from flaskwebgui import FlaskUI


HOSTNAME = socket.gethostname()
LOCAL_IP = socket.gethostbyname(HOSTNAME)
PORT = 5000
BASE_DIR = pathlib.Path(__file__).resolve(strict=True).parent
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)
# ui = FlaskUI(app, close_server_on_exit=False)


@app.route("/", defaults={"path": None})
@app.route("/<path:path>")
def home(path):

    # if is_wifi_turned_on():
    #     return render_template("activate_wifi.html")

    generate_qr_code(LOCAL_IP, PORT)

    DEFAULT_DIR = pathlib.Path(__file__).resolve(strict=True).parent
    if not path:
        path = DEFAULT_DIR

    if os.path.isfile(path):
        return send_file(path, conditional=True)

    files = pathlib.Path(path).iterdir()
    media = []
    for f in files:
        if not pathlib.Path(f).name.startswith("."):
            media.append(
                {
                    "filename": reduce_file_name(pathlib.Path(f).name),
                    "absolutepath": str(pathlib.Path(f).absolute()),
                    "filename_without_extenstion": pathlib.Path(f).stem,
                    "is_dir": pathlib.Path(f).is_dir(),
                    "extension_icon": get_extension_icon(f.name.split(".")[-1]),
                    "url": str(request.url_root) + str(pathlib.Path(f).absolute()),
                }
            )
    current_dir = pathlib.Path(path)
    parent_dir = current_dir.parent

    if request.args.get("ajax"):
        return jsonify(
            {
                "media": media,
                "current_dir": str(current_dir),
                "parent_dir": str(parent_dir),
                "parent_dir_url": str(request.url_root) + str(parent_dir),
            }
        )

    return render_template("layout.html")


if __name__ == "__main__":
    # ui.run()
    app.run(debug=True, host="0.0.0.0", port=PORT)
