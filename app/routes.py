from flask import render_template, url_for, flash, redirect, request, jsonify
from app import app, db
from app.models import Article, User
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/api/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify([article.serialize() for article in articles])

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify(article.serialize())

@app.route('/api/articles', methods=['POST'])
@login_required
def create_article():
    data = request.get_json()
    article = Article(title=data['title'], content=data['content'], author=current_user)
    db.session.add(article)
    db.session.commit()
    return jsonify({'message': 'Article created successfully', 'article_id': article.id})

@app.route('/api/articles/<int:article_id>', methods=['PUT'])
@login_required
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        return jsonify({'error': 'You are not authorized to update this article'}), 403
    data = request.get_json()
    article.title = data['title']
    article.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Article updated successfully'})

@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        return jsonify({'error': 'You are not authorized to delete this article'}), 403
    db.session.delete(article)
    db.session.commit()
    return jsonify({'message': 'Article deleted successfully'})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})
