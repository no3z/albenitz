import time
from camera import VideoCamera
from envirophat import light, motion, weather, leds, analog
from flask import Flask, render_template, jsonify, redirect, url_for, Response, request
from uptime import boottime
from functools import wraps
import subprocess
import utilities
import monitor
import password

app = Flask(__name__)

rows = []

@app.route('/_update', methods= ['GET'] )
def updateIndexData():
    monitor.updateData()
    return jsonify(data=monitor.data)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def check_auth(username, password):
    return username == passwd.user and password == passwd.password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})
        
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/video_feed1')
@requires_auth
def video_feed1():
    return Response(gen(VideoCamera(0)),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
@requires_auth
def video_feed2():
    return Response(gen(VideoCamera(1)),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/dashboard')
def dashboard():
    interval='7 days'
    rows = []
    dates = []
    temp_y = []
    cd = monitor.updateData()
    for idx, cdata in enumerate(cd):
        rows.insert(idx, utilities.get_data(utilities.dbname, interval))
        dates.insert(idx, utilities.create_xaxis(rows[idx]))
        temp_y.insert(idx, utilities.create_yaxis(rows[idx],cdata,idx+1))
        
    return render_template('dashboard.html', data=monitor.chart_data, xdata=dates, ydata=temp_y)

@app.route('/led/<status>')
@requires_auth
def led(status):
    if status=='on':
	leds.on()
    elif status=='off':
	leds.off()
    return redirect(url_for('index'))

@app.route('/reboot')
@requires_auth
def reboot():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]

@app.route('/')
def index():   
    monitor.updateData()
    return render_template('index.html', data=monitor.data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)
