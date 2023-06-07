pipeline {
  agent any
  stages {
    stage('CheckCode') {
      steps {
        git(url: 'https://github.com/JakubWronowski/simple_flask_app', branch: 'main')
      }
    }

  }
}