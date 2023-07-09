from flask import Flask, request, jsonify,send_from_directory
import subprocess
from flask_cors import CORS
import glob
import os
import urllib.parse
from process_files import process_file
from process_pdf import process_pdf_file
from messages import send_message

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
cors = CORS(app, origins="*")

@app.route("/api/", methods=["get"])
def get_root():
     return jsonify({"api":"/"})

@app.route("/api/files", methods=["POST"])
def get_files():
    try:
        data = request.get_json()
        folders = data.get('folders')
        customer = data.get('customer')
        if not folders:
            return jsonify({"error":"folders required"})
        files = {}
        for folder in folders: 
            try:
                files[folder] = [len(os.listdir(folder+"/"+customer))]
                if os.path.exists(folder+"/"+customer+"/processed"):
                    files[folder].append(len(os.listdir(folder+"/"+customer+"/processed")))
                    files[folder][0]  = files[folder][0] - 1
                else:
                    files[folder].append(0)    
                if os.path.exists(folder+"/"+customer+"/processed/keywords.txt"):
                    try:
                        with open(folder+"/"+customer+"/processed/keywords.txt") as fp:
                            files[folder].append(fp.read())
                    except Exception as e:
                        print(e)
                        files[folder].append('')
            except:
                files[folder] = [0,0, '']     
                  
        return jsonify(files)
    except Exception as e:
        print(e)
        return jsonify({"error":"Unable to complete your request"})

     

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        # Get the files and folder name from the request
        folder_names = request.form.get('folders').split(',')
        customer = request.form.get('customer')
        file_count = 0
        for folder_name in folder_names:
            files = request.files.getlist(folder_name)
            # Check if the folder exists, create it if it doesn't
            if os.path.exists(folder_name+"/"+customer):
                
                pdf_path =os.path.abspath(folder_name+"/"+customer)
                # os.remove(pdf_path)
                for filename in os.listdir(pdf_path):
                    file_path = os.path.join(pdf_path, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                if(os.path.exists(folder_name+"/"+customer+"/processed")):
                    pdf_path1 = os.path.abspath(folder_name+"/"+customer+"/processed")
                    for filename in os.listdir(pdf_path1):
                        file_path = os.path.join(pdf_path1, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)

            if not os.path.exists(folder_name+"/"+customer):
                os.makedirs(folder_name+"/"+customer)

            # Save each file in the folder
            for file in files:
                if file.filename.endswith('.pdf') or file.filename.endswith('.PDF'):
                    file.save(os.path.join(folder_name+"/"+customer, file.filename))

            # Get the total number of files in the folder 
        response = {'message': 'Files uploaded successfully', 'files': 3}
        return jsonify(response)  
    except Exception as e:
        print(e)
        return jsonify({"error":str(e)})

@app.route('/api/process/test', methods=['POST'])
def process_files_test():
    folder_name = request.json.get('folder')
    customer = request.json.get('customer')
    try:
        command = ['python', 'process_files.py', folder_name+"/"+customer]
        subprocess.Popen(command)
    except Exception as e: print(e)    
    return jsonify({"image":"Image file processing in background"})

@app.route('/api/process', methods=['POST'])
def process_files():
      # Get the folder name from the request
    folder_name = request.json.get('folder')
    customer = request.json.get('customer')

    # Check if the folder exists
    if not os.path.exists(folder_name+"/"+customer):
        return jsonify({'error': 'Folder not found'})
    
    
    try:
        isimg = process_pdf_file(os.path.join(folder_name,customer))
        print(isimg)
        if isimg:
            send_message('Image file processing in the background, please wait...')
            command = ['python', 'process_files.py', folder_name+"/"+customer]
            subprocess.Popen(command)
            return jsonify({"image":"Image file processing in background"})

    except Exception as e: 
        print(e)
        pass 
    
    return jsonify({"processing":"done"})

# get file list
@app.route('/api/list', methods=['POST'])
def get_file_list():
    folders = request.json.get('folders')
    files = {}
    for folder in folders:
        pdf_files = []
        folder_path = os.path.abspath(folder)
        search_path = os.path.join(folder_path, "*.pdf")
        pdf_files = glob.glob(search_path)
        pdf_files = [os.path.basename(file) for file in pdf_files if os.path.isfile(file)]
        files[folder] = pdf_files
    return jsonify(files)

@app.route("/api/getpdf", methods=['get'])
def get_pdf():
    folder = urllib.parse.unquote(request.args.get("folder"))
    customer = urllib.parse.unquote(request.args.get("customer"))
    print(customer)
    print(request.args.get("customer"))
    print(folder)
    pdf_path =os.path.abspath(folder)+'/'+customer+'/processed'
    print(pdf_path)
    if os.path.exists(pdf_path):
        
        pdf_files = [file for file in os.listdir(pdf_path) if file.lower().endswith('.pdf')]
    
        if(len(pdf_files)>0):
            return send_from_directory(pdf_path, pdf_files[0])
    else:
        pdf_path =os.path.abspath(folder)+'/'+customer
        if not os.path.exists(pdf_path): return send_from_directory(pdf_path, 'none.pdf')
        pdf_files = [file for file in os.listdir(pdf_path) if file.lower().endswith('.pdf')]
        if(len(pdf_files)>0):
             return send_from_directory(pdf_path, pdf_files[0])
    return send_from_directory(pdf_path, 'none.pdf')
@app.route("/api/delete", methods=['get'])
def delete_pdf():
    folder_name = urllib.parse.unquote(request.args.get("folder"))
    customer = urllib.parse.unquote(request.args.get("customer"))

    if os.path.exists(folder_name+"/"+customer):
                
                pdf_path =os.path.abspath(folder_name+"/"+customer)
                # os.remove(pdf_path)
                for filename in os.listdir(pdf_path):
                    file_path = os.path.join(pdf_path, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                if(os.path.exists(folder_name+"/"+customer+"/processed")):
                    pdf_path1 = os.path.abspath(folder_name+"/"+customer+"/processed")
                    for filename in os.listdir(pdf_path1):
                        file_path = os.path.join(pdf_path1, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
    
    return jsonify({"file":"success"})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)