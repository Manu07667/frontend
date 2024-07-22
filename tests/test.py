import pytest
from app import app, db
from app.models import User, Article

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_create_article(client):
    response = client.post('/api/login', json={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 200

    response = client.post('/api/articles', json={'title': 'Test Article', 'content': 'This is a test article content'})
    assert response.status_code == 200

    article_id = response.json['article_id']
    article = Article.query.get(article_id)
    assert article.title == 'Test Article'
