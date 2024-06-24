import flask
from flask import request, jsonify
from pymavlink.dialects.v20 import common as mavlink2
from pymavlink import mavutil
import time
import datetime

app = flask.Flask(__name__)

@app.route('/api/getflyghtdetails', methods=['GET'])
def api_all():
    # Get the video URL from the query parameters
    video_url = request.args.get('video_url', type=str)
    
    # Establish a connection to the MAVLink stream using the provided video URL
    the_connection = mavutil.mavlink_connection(video_url)
    
    # Retrieve GLOBAL_POSITION_INT message
    Home = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    latitude = Home.lat
    longitude = Home.lon
    altitude = Home.alt

    # Retrieve ATTITUDE message
    ATTITUDE = the_connection.recv_match(type='ATTITUDE', blocking=True)
    roll = ATTITUDE.roll
    pitch = ATTITUDE.pitch
    yaw = ATTITUDE.yaw

    # Create flight details dictionary
    flyghtdetails = [
       {
           'lat': latitude,
           'lng': longitude,
           'alt': altitude,
           'nav_roll': roll,
           'nav_pitch': pitch,
           'nav_yaw': yaw,
           'StreamingStartTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    
    # Return flight details as JSON
    return jsonify(flyghtdetails)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)



#1. python your_flask_app.py
#2. http://localhost:8080/api/getflyghtdetails?video_url=your_video_url
