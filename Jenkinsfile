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
python3 -m pytest login_test.py'''
      }
    }

  }
}