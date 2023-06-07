pipeline {
  agent any
  stages {
    stage('CheckCode') {
      steps {
        git(url: 'https://github.com/JakubWronowski/simple_flask_app.git', branch: 'main')
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

    stage('DockerBuild') {
      steps {
        sh '''#!/bin/bash
docker build -t simple_flask_app:latest .'''
      }
    }

  }
}