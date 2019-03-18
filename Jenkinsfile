pipeline {
  agent any
  stages {
    stage('build') {
      parallel {
        stage('build') {
          steps {
            retry(count: 3) {
              bat 'python --version'
              bat 'python -compileall TeamProject496/'
            }

            timeout(time: 3, unit: 'MINUTES') {
              echo 'We can check timeouts, this echo certainly is pointless though!'
            }

          }
        }
        stage('Where am i') {
          steps {
            bat 'dir'
          }
        }
        stage('who am i') {
          steps {
            bat 'whoami'
          }
        }
      }
    }
    stage('test') {
      steps {
        bat 'echo \'test\''
      }
    }
  }
}
