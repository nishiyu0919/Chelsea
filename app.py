# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from db import insert_blog, insert_image, get_blog_details, get_images
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'  # 画像のアップロード先フォルダ
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# アップロード先フォルダが存在しない場合、自動的に作成
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def top():
    blogs = get_blog_details()
    return render_template('top.html', blogs=blogs)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        content = request.form['content']
        image_files = request.files.getlist('image')

        if not title or not date or not content:
            flash('タイトル、日付、記事内容は必須です')
        else:
            # 記事を挿入
            blog_id = insert_blog(title, date, content)

            if blog_id is not None:  # blog_id が None でないことを確認
                # 画像をアップロード
                for file in image_files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as img_file:
                            image_data = img_file.read()
                        insert_image(blog_id, filename, image_data)

                flash('記事が投稿されました')
                return redirect(url_for('top'))

    return render_template('write.html')


@app.route('/read/<int:blog_id>')
def read(blog_id):
    blog = get_blog_details(blog_id)
    images = get_images(blog_id)
    
    # 画像データをBase64エンコードして渡す
    image_data_base64 = []
    for image in images:
        image_data_base64.append(base64.b64encode(image[1]).decode('utf-8'))
    
    return render_template('read.html', blog=blog, images=images, image_data_base64=image_data_base64)


if __name__ == '__main__':
    app.run()