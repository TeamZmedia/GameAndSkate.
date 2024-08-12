from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

content = {
    "home_text": "Welcome to the Game and Skate Website!",
    "home_image": "home_image.png",
    "events": [
        {"header": "Event 1", "description": "Description of Event 1."},
        {"header": "Event 2", "description": "Description of Event 2."}
    ],
    "about_top": "Text above the image.",
    "about_image": "about_image.png",
    "about_bottom": "Text below the image."
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html', content=content)

@app.route('/events')
def events():
    return render_template('events.html', content=content)

@app.route('/about')
def about():
    return render_template('about.html', content=content)

@app.route('/editedit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        content["home_text"] = request.form.get('home_text')
        content["events"][0]["header"] = request.form.get('event1_header')
        content["events"][0]["description"] = request.form.get('event1_description')
        content["events"][1]["header"] = request.form.get('event2_header')
        content["events"][1]["description"] = request.form.get('event2_description')
        content["about_top"] = request.form.get('about_top')
        content["about_bottom"] = request.form.get('about_bottom')

        # Handle file uploads
        home_image = request.files.get('home_image')
        about_image = request.files.get('about_image')
        
        if home_image and allowed_file(home_image.filename):
            filename = secure_filename("home_image.png")
            home_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            content["home_image"] = filename
        
        if about_image and allowed_file(about_image.filename):
            filename = secure_filename("about_image.png")
            about_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            content["about_image"] = filename

        flash('Content updated successfully!')
        return redirect(url_for('home'))
    return render_template('edit.html', content=content)

if __name__ == "__main__":
    app.run(debug=True)
    