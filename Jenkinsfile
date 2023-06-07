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
        sh '''#!/bin/bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python -m pytest login_test.py
'''
      }
    }

    stage('Build Docker') {
      steps {
        sh '''#!/bin/bash
cd ~/Desktop/simple_flask_app
docker build -f simple_flask_app/Dockerfile .'''
      }
    }

  }
}