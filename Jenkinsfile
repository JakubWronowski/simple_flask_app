pipeline {
  agent any
  stages {
    stage('CheckCode') {
      steps {
        git(url: 'https://github.com/JakubWronowski/simple_flask_app', branch: 'main')
      }
    }

    stage('Login_test') {
      steps {
        sh '''python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m pytest login_test.py'''
      }
    }

  }
}