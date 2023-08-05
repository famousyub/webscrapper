from flask import Flask, request, render_template,jsonify
import os
from  extractdatapdf import extract_data_from_resume
import nltk
from linkedinscv import ScrappingJobs

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    nltk.download('averaged_perceptron_tagger')
    if 'resume' not in request.files:
        return "No file part"

    resume_file = request.files['resume']
    if resume_file.filename == '':
        return "No selected file"

    # Save the uploaded file
    resume_path = os.path.join('uploads', resume_file.filename)
    resume_file.save(resume_path)

    # Call the function to extract data from the uploaded resume
    extracted_data = extract_data_from_resume(resume_path)
    print (extracted_data)

    return extracted_data

@app.route("/jobtitle/<job>/<country>")
def findingjobs(job,country):
    scf = ScrappingJobs(country=country,query=job)

    scf.jobfind()

    return jsonify({'response':'jobsfetching'})


if __name__ == '__main__':
    app.run(debug=True)
