pipeline {
    agent none
    
    environment {
        NODE_VERSION = '18'
        PYTHON_VERSION = '3.9'
    }
    
    stages {
        stage('Checkout') {
            agent any
            steps {
                checkout scm
            }
        }
        
        stage('Parallel Tests') {
            parallel {
                stage('Frontend Tests') {
                    agent {
                        docker {
                            image 'node:18-alpine'
                        }
                    }
                    steps {
                        sh 'npm install'
                        sh 'npm test'
                        sh 'npm run build'
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'coverage',
                                reportFiles: 'index.html',
                                reportName: 'Frontend Coverage Report'
                            ])
                        }
                    }
                }
                
                stage('Backend Tests') {
                    agent {
                        docker {
                            image 'python:3.9-slim'
                        }
                    }
                    steps {
                        sh 'pip install -r requirements.txt'
                        sh 'python -m pytest tests/ --junitxml=test-results.xml'
                    }
                    post {
                        always {
                            junit 'test-results.xml'
                        }
                    }
                }
                
                stage('Security Scan') {
                    agent any
                    steps {
                        sh 'trivy fs --format json --output trivy-results.json .'
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: 'trivy-results.json'
                        }
                    }
                }
            }
        }
        
        stage('Integration Tests') {
            agent any
            steps {
                sh 'docker-compose up -d'
                sh 'sleep 30'
                sh 'curl -f http://localhost:8080/health'
            }
            post {
                always {
                    sh 'docker-compose down'
                }
            }
        }
    }
}