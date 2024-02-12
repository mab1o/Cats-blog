from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, Article
from app.forms import LoginForm, RegistrationForm, ArticleForm, DeleteArticleForm, UpdateArticleForm

@app.route('/')
@app.route('/index')
def index():
    articles = Article.query.all()
    theme_selectionne = request.args.get('theme')
    if not theme_selectionne:
        articles_filtres = articles
    else:
        articles_filtres = [article for article in articles if article.theme == theme_selectionne]
    return render_template('home.html', title='Home', articles=articles_filtres)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/gestion', methods=['GET', 'POST'])
def add_article():

    # add article
    add_article = ArticleForm()
    if add_article.validate_on_submit():
        article = Article(title=add_article.title.data, 
                          theme=add_article.theme.data, 
                          body=add_article.body.data, 
                          author_id= add_article.author_id.data,
                          timestamp= add_article.timestamp.data)
        db.session.add(article)
        db.session.commit()
        flash('Article ajouté avec succès!', 'success')
        return redirect(url_for('index'))
    
    # delete article
    del_article = DeleteArticleForm()
    del_article.article.choices = [(article.id, article.title) for article in Article.query.all()]
    if del_article.validate_on_submit():
        article_id = del_article.article.data
        article = Article.query.get(article_id)
        db.session.delete(article)
        db.session.commit()
        flash('Article supprimé avec succès!', 'success')
        return redirect(url_for('index'))
    
    # modifier article
    mod_article = UpdateArticleForm()
    mod_article.article.choices = [(article.id, article.title) for article in Article.query.all()]
    if mod_article.validate_on_submit():
        article_id = mod_article.article.data
        article = Article.query.get(article_id)
        article.title = mod_article.title.data
        article.body = mod_article.body.data
        db.session.add(article)
        db.session.commit()
        flash('Article modifié avec succès!', 'success')
        return redirect(url_for('index'))

    return render_template('gestion.html', title='Admin', 
                           add_article=add_article, 
                           del_article=del_article,
                           mod_article=mod_article)

@app.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', title='Article', article=article)
