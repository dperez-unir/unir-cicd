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
            script{
                emailext (
                    from: 'Jenkins Actividad-3 <jenkins@test.com>',
                    subject: "Build ${currentBuild.fullDisplayName}",
                    body: """<p>Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}:</p>
                             <p>Check console output at <a href="${env.BUILD_URL}">${env.BUILD_URL}</a> to view the results.</p>""",
                    to: 'david.perez.rod@gmail.com'
                )
            }
        }
    }
}
