import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from db import get_connection
from datetime import datetime

app = Flask(__name__)

# アップロードされた画像ファイルを保存するディレクトリ
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # 拡張子のチェックを行う関数
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blog')
    blog_posts = cursor.fetchall()
    conn.close()
    return render_template('top.html', posts=blog_posts)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        date_str = request.form['date']

        try:
            # フォームから取得した日付文字列を datetime オブジェクトに変換
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return "無効な日付形式です。正しい形式は 'YYYY-MM-DD' です。", 400

        content = request.form['content']

        if 'image' not in request.files:
            return "画像が選択されていません", 400

        image = request.files['image']

        if image.filename == '':
            return "画像ファイルがありません", 400

        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO blog (title, image, date, content) VALUES (%s, %s, %s, %s)',
                           (title, image.read(), date, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('write.html')

@app.route('/read/<int:post_id>')
def read(post_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blog WHERE id = %s', (post_id,))
    post = cursor.fetchone()
    conn.close()

    if post is None:
        return "記事が見つかりません", 404

    # 画像を表示するためにバイナリデータをBase64にエンコード
    image_data = post[2]  # 画像データは3番目の列にあると仮定

    return render_template('read.html', post=post, image_data=image_data)

if __name__ == '__main__':
    app.run(debug=True)
