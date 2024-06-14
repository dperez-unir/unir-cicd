pipeline {
    agent {
        label 'docker'
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building stage!'
                sh 'make build'
            }
        }
        stage('Unit tests') {
            steps {
                sh 'make test-unit'
                archiveArtifacts artifacts: 'results/*.xml'
            }
        }
        stage('Api test') {
            steps {
                sh 'docker rm apiserver'
                sh 'make test-api'
                archiveArtifacts artifacts: 'results/*.xml'
            }
        }
        stage('E2e test') {
            steps {
                sh 'make server'
                sh 'make test-e2e'                
                archiveArtifacts artifacts: 'results/*.xml'
            }
        }        
    }
    post {
        always {
            junit 'results/*_result.xml'
        }
    }
}
