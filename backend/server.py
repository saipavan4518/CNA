from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import pymongo
import json
import os


scriptPath = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'C:\\Users\\smadabat\\Documents\\CNA-NAA project\\backend\\uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def check_audit_info(customer_key, audit_id, audit_type):
    dbName = "CNA_Visualizer"
    dbClient = pymongo.MongoClient('localhost', 27017)
    db = dbClient[dbName]
    query = {"customer_key" : customer_key, "audit_id" : audit_id , "audit_type" : audit_type}
    res = db['upload_information'].find(query)
    result = list(res)
    print("Checking if audit is already available ... ")
    if len(result) == 0:
        print("Not found in the DB")
        return False
    else:
        print("Found in DB")
        return True


@app.route("/", methods=['GET'])
def default_route():
    if request.method == 'GET':
        result = {"details": "pavan is great"};
        return result


@app.route("/api/upload", methods=['POST'])
def upload():
    """
    this function is used to upload the audits from the user
    :return: it returns the status code for the frontend
    """
    if request.method == 'POST':
        # init the data for storing the input from the starting page
        # two audits with name audit 1 and audit 2
        data = {}
        if "audit_1" in request.files and "audit_2" in request.files and "cec_id" in request.form:
            # complete the if statement
            # these are the files
            audit_1 = request.files['audit_1']
            audit_2 = request.files['audit_2']

            cec_id = str(request.form['cec_id'])
            top_id = str(request.form['top_id'])
            cpy_key = str(request.form['cpy_key'])
            cname = str(request.form['cname'])
            audit1_id = str(request.form['audit1_id'])
            audit1_type = request.form['audit1_type']
            audit2_id = str(request.form['audit2_id'])
            audit2_type = request.form['audit2_type']

            if cec_id and cpy_key and audit1_id and audit2_id and audit2_type and audit1_type:
                # creating the data object using all the data
                data['cec_id'] = cec_id
                data['top_id'] = top_id
                data['cpy_key'] = cpy_key
                data['cname'] = cname
                data['audit1_id'] = audit1_id
                data['audit2_id'] = audit2_id
                data['audit1_type'] = audit1_type
                data['audit2_type'] = audit2_type
                data['audit1_filename'] = audit_1.filename
                data['audit2_filename'] = audit_2.filename

                print(data)

                # save both the files in the upload folder
                audit_1.save(os.path.join(UPLOAD_FOLDER, secure_filename(audit_1.filename)))
                audit_2.save(os.path.join(UPLOAD_FOLDER, secure_filename(audit_2.filename)))

                if not check_audit_info(data['cpy_key'], data['audit1_id'], data['audit1_type']):
                    saved_info_file = "uploadInfo_" + data['cpy_key'] + "_" + data['audit1_id'] + ".json"
                    with open(saved_info_file, "w") as f:
                        f.write(json.dumps(data))

                    # here we should store the data in the table


                return {"message": "success"}, 200
            else:
                return {"error": "Error Format in request"}, 400
        else:
            return {"error": "Error format in request header"}, 400


if __name__ == "__main__":
    app.run(debug=True)