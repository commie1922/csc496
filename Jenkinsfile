pipeline {
    agent { docker { image 'python:2.7.11' } }
    stages {
        stage('build') {
            steps {
                bat 'python --version'
            }
        }
    }
}
