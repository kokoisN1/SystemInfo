# Get VM info module
import os
import json
import socket
import multiprocessing
import datetime
import psutil
import urllib.request
import cpuinfo
import GPUtil
from flask import Flask, request

# required to modules to download/install  py-cpuinfo and psutil , GPUtil 
# pip install cpuinfo
# pip install GPUtil
# pip install flask

def main():
    def get_iso_time():
        time = datetime.datetime.now()
        ISO_8601_time = time.isoformat()
        return ISO_8601_time

    def get_local_ip():
        return socket.gethostbyname(socket.gethostname()) # need to fix ?

    def get_external_ip():
        try:
            with  urllib.request.urlopen('https://ident.me') as response:
                return response.read().decode('ascii')
        except:
            with  urllib.request.urlopen('https://6.tnedi.me') as response:
                return response.read().decode('ascii')

    def get_CPU_name():
        return cpuinfo.get_cpu_info()['brand_raw']

    def get_core_number(): # returning this number, but this does not take into account the hyper-threading on an Intel CPU.
        return multiprocessing.cpu_count()

    def get_vmm_size():
        return round(psutil.virtual_memory().total/1065310720) 

    # do not have access to a GPU - so this was not fully tested !
    def get_gpu_info():
        getGPUsNumber = GPUtil.getGPUs()
        if getGPUsNumber != []:
            GPU = GPUtil.getFirstAvailable()[0]
        else:
            GPU = "No GPU found"
        return GPU

    def get_SystemInfo():
        answers_dict = {}
        answers_dict['CPU Model'] = get_CPU_name()
        answers_dict['Time UTC On Server'] = get_iso_time()
        answers_dict['Memory Size'] = get_vmm_size()
        answers_dict['CPU Cores'] = get_core_number() 
        answers_dict['External IP Address'] = get_local_ip()
        answers_dict['External IP'] = get_external_ip()
        answers_dict['GPU Type'] = get_gpu_info()
        return answers_dict

    app = Flask(__name__)

    description =   """
                    <!DOCTYPE html>
                    <head>
                    <title>API Landing</title>
                    </head>
                    <body>  
                        <h3>swish.ai test API </h3>
                        <a href="http://localhost:5000/api?value=2">sample request</a>
                    </body>
                    """
                    
    # Routes refer to url'
    # our root url '/' will show our html description
    @app.route('/', methods=['GET'])
    def hello_world():
        return description

    # our '/api' url
    # requires user integer argument: value
    # returns error message if wrong arguments are passed.
    @app.route('/api', methods=['GET'])
    def square1():
        if not all(k in request.args for k in (["value"])):
            # we can also print dynamically 
            # using python f strings and with 
            # html elements such as line breaks (<br>)
            error_message =     f"\
                                Required paremeters : 'value'<br>\
                                Supplied paremeters : {[k for k in request.args]}\
                                "
            return error_message
        else:
            # assign and cast variable to int
            value = int(request.args['value'])
            # or use the built in get method and assign a type
            # http://werkzeug.palletsprojects.com/en/0.15.x/datastructures/#werkzeug.datastructures.MultiDict.get
            value = request.args.get('value', type=int)
            return json.dumps({"Value Squared" : value**2})
    @app.route('/api/SystemInfo', methods=['GET'])
    def getit():
        print( json.dumps(get_SystemInfo(), sort_keys=True, indent=4))
        return get_SystemInfo()

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=os.getenv('PORT'))

if __name__ == "__main__":
    main()




