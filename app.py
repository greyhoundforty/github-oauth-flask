from flask import Flask, redirect, url_for, session, render_template 
from authlib.integrations.flask_client import OAuth
import os
from logging_extension import create_app

app = create_app()
app.secret_key = os.environ['APP_SECRET_KEY']

oauth = OAuth(app)

github = oauth.register(
    name='github',
  client_id=os.environ.get('GITHUB_CLIENT_ID'),
  client_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
  access_token_url='https://github.com/login/oauth/access_token',
  authorize_url='https://github.com/login/oauth/authorize',
  api_base_url='https://api.github.com/',
)

@app.route('/')
def home():
  if 'github_token' in session:
    return render_template('home.html', logged_in=True)
  else:
    return render_template('home.html', logged_in=False)

@app.route('/login')
def login():
  redirect_uri = url_for('authorized', _external=True)
  return github.authorize_redirect(redirect_uri, scope='read:org')

@app.route('/authorized')
def authorized():
  token = github.authorize_access_token()
  session['github_token'] = token['access_token'] 
  return redirect('/')

@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('login'))

@app.route('/repos')
def repos():
  from github import Github
  token = session['github_token']
  g = Github(token)

  org = g.get_organization('cloud-design-dev')
  repos = org.get_repos()

  tagged_repos = []
  for repo in repos:
    topics = repo.get_topics()
    if 'deployable' in topics:
      tagged_repos.append(repo)

  return render_template('repos.html', repos=tagged_repos)
  
if __name__ == '__main__':
    app.run(debug=True, port=8080)
