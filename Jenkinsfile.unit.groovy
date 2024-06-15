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
                sh 'docker stop apiserver || true'                
                sh 'docker rm apiserver || true'    
                sh 'make test-api'
                archiveArtifacts artifacts: 'results/*.xml'
                sh 'docker stop apiserver || true'                
                sh 'docker rm apiserver || true'
            }
        }
        stage('E2e test') {
            steps {
                sh 'docker stop apiserver || true'                
                sh 'docker rm apiserver || true'                
                sh 'make test-e2e'                
                archiveArtifacts artifacts: 'results/*.xml'
                sh 'docker stop apiserver || true'                
                sh 'docker rm apiserver || true'                
            }
        }        
    }
    post {
        always {
            junit 'results/*_result.xml'
            emailext (
                subject: "Build \${currentBuild.fullDisplayName}",
                body: "Job \${env.JOB_NAME} build \${env.BUILD_NUMBER}:\n\nCheck console output at \${env.BUILD_URL} to view the results.",
                to: 'david.perez.rod@gmail.com'
            )
        }
    }
}
