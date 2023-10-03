from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 記事データを格納するリスト（実際のデータベースなどに置き換える必要があります）
blog_posts = []

@app.route('/')
def index():
    return render_template('top.html', blog_posts=blog_posts)

# /write ルートを追加
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        image = request.files['image'] if 'image' in request.files else None
        date = request.form['date']
        content = request.form['content']

        # データベースに記事を保存するなど、必要な処理を追加

        # このサンプルでは記事データをリストに追加しています
        blog_posts.append({
            'title': title,
            'image': image,
            'date': date,
            'content': content
        })

        return redirect(url_for('index'))

    return render_template('write.html')

if __name__ == '__main__':
    app.run(debug=True)
