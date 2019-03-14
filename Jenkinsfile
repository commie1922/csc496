pipeline {
  agent any
  stages {
    stage('build') {
      steps {
              retry(3) {
                bat 'python --version'
              }

              timeout(time: 3, unit: 'MINUTES') {
                  echo 'We can check timeouts, this echo certainly is pointless though!'
              }
      }
    }
  }
}
