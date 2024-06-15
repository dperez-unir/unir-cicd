pipeline {
    agent {
        label 'docker'
    }
    stages {
        stage('Report artifacts') {
            steps {
                sh '''
                    mkdir -p results_old
                    mv results/* results_old
                    rm -rf results_old
                    mkdir -p results/html
                    mkdir -p results/coverage
                    mkdir -p results/videos
                    mkdir -p results/screenshots
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building stage!'
                sh 'make build'
            }
        }
        stage('Unit tests') {
            steps {
             sh 'make test-unit'
            }
        }
        stage('Api test') {
            steps {
                sh 'docker stop apiserver || true'                
                sh 'docker rm apiserver || true'    
                sh 'make test-api'
                archiveArtifacts artifacts: 'results/*.xml'
                archiveArtifacts artifacts: 'results/*.html' 
            }
        }
        stage('E2e test') {
            steps {
                sh 'docker stop apiserver || true'                
                sh 'docker rm apiserver || true'                
                sh 'make test-e2e'                
                archiveArtifacts artifacts: 'results/*.xml'
                archiveArtifacts artifacts: 'results/*.html'  
            }
        } 
    }
    post {
        always {
            junit 'results/*_result.xml'
        }            
        failure {
                junit 'results/*_result.xml'            
                emailext (
                    subject: "Build ${currentBuild.fullDisplayName}",
                    body: """\
                        <html>
                            <head>
                                <style>
                                    body { font-family: Arial, sans-serif; }
                                    .header { background-color: #f8f9fa; padding: 10px; border-bottom: 1px solid #dee2e6; }
                                    .content { padding: 20px; }
                                    .footer { background-color: #f8f9fa; padding: 10px; border-top: 1px solid #dee2e6; text-align: center; }
                                </style>
                            </head>
                            <body>
                                <div class="header">
                                    <h2>Resultado de la Build: ${env.JOB_NAME} #${env.BUILD_NUMBER}</h2>
                                </div>
                                <div class="content">
                                    <p>El trabajo <strong>${env.JOB_NAME}</strong> se ha completado.</p>
                                    <p>Detalles del build:</p>
                                    <ul>
                                        <li>Nombre del trabajo: ${env.JOB_NAME}</li>
                                        <li>Número del build: ${env.BUILD_NUMBER}</li>
                                        <li>Estado: ${currentBuild.currentResult}</li>
                                    </ul>
                                    <p>Revisa la salida de la consola y los artefactos en los siguientes enlaces:</p>
                                    <p><a href="${env.BUILD_URL}">Ver detalles del build</a></p>
                                </div>
                                <div class="footer">
                                    <p>Este es un correo generado automáticamente por Jenkins.</p>
                                </div>
                            </body>
                        </html>
                    """,
                    mimeType: 'text/html',
                    to: 'david.perez.rod@gmail.com'
                )        
        }        
    }    
}
