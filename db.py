# db.py

import os
import psycopg2

# データベース接続用の関数
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

# ブログ記事を挿入する関数
def insert_blog(title, date, content):
    sql = "INSERT INTO blog (title, date, content) VALUES (%s, %s, %s) RETURNING id"
    args = (title, date, content)
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, args)
        blog_id = cursor.fetchone()[0]
        connection.commit()
        return blog_id
    except psycopg2.DatabaseError:
        return None
    finally:
        cursor.close()
        connection.close()

# 画像を挿入する関数
def insert_image(blog_id, filename, image_data):
    sql = "INSERT INTO images (blog_id, filename, image_data) VALUES (%s, %s, %s)"
    args = (blog_id, filename, image_data)
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, args)
        connection.commit()
    except psycopg2.DatabaseError:
        pass  # エラーハンドリングは必要に応じて追加してください
    finally:
        cursor.close()
        connection.close()

# すべてのブログ記事を取得する関数
def get_blog_details(blog_id=None):
    if blog_id is not None:
        sql = "SELECT title, date, content FROM blog WHERE id = %s"
        args = (blog_id,)
    else:
        sql = "SELECT id, title, date FROM blog"
        args = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        if args is not None:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        if blog_id is not None:
            blog = cursor.fetchone()
            return blog
        else:
            blogs = cursor.fetchall()
            return blogs
    except psycopg2.DatabaseError:
        return [] if blog_id is None else None
    finally:
        cursor.close()
        connection.close()

# 特定のブログ記事の画像を取得する関数
def get_images(blog_id):
    sql = "SELECT filename, image_data FROM images WHERE blog_id = %s"
    args = (blog_id,)
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, args)
        images = cursor.fetchall()
        return images
    except psycopg2.DatabaseError:
        return []
    finally:
        cursor.close()
        connection.close()
