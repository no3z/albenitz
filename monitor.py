import time
from envirophat import light, motion, weather, leds, analog
import utilities
import subprocess
from uptime import boottime

data = {}
chart_data = {}

def updateData():
    data["lux"] = light.light()
    data["rgb"] = str(light.rgb())[1:-1].replace(' ', '')
    data["heading"] = motion.heading()
    data["temp_sensor"] = float(round(weather.temperature(),2))
    data["pressure"] = round(float(weather.pressure()/100),2)
    
    data["led_on"] = leds.is_on()
    data["led_off"] = leds.is_off()
    data["date"] = time.strftime("%c")
    data["boottime"] = boottime()
    process = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    output, _error = process.communicate()
    data["temp_cpu"] = float(output[output.index('=') + 1:output.rindex("'")])
    data["temp_fixed"] = data["temp_sensor"] - ((data["temp_cpu"]-data["temp_sensor"])/1.3)
    data["temp_fixed"] = float(round(data["temp_fixed"],2))

    #data["acceleration"] = str(motion.accelerometer())[1:-1].replace(' ', '')
    #data["magnetometer"] = str(motion.magnetometer())[1:-1].replace(' ', '')
    #data["analog"] = str(analog.read_all())[1:-1].replace(' ', '')

    for k,v in data.iteritems():
        if not isinstance(v, basestring) and str(v).replace('.','',1).isdigit():
            chart_data[k] = float(v)

    return chart_data

def insertData():
    updateData()
    utilities.log_data(chart_data)

if __name__ == '__main__':
    insertData()
