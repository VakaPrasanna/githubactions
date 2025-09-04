pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'myapp'
        DOCKER_CREDS = credentials('docker-hub-credentials')
    }
    
    parameters {
        string(name: 'TAG', defaultValue: 'latest', description: 'Docker image tag')
        booleanParam(name: 'PUSH_IMAGE', defaultValue: true, description: 'Push to registry?')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/example/repo.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    def image = docker.build("${IMAGE_NAME}:${params.TAG}")
                }
            }
        }
        
        stage('Test Image') {
            steps {
                sh '''
                    docker run --rm ${IMAGE_NAME}:${params.TAG} /bin/sh -c "echo 'Testing container'"
                '''
            }
        }
        
        stage('Push to Registry') {
            when {
                expression { return params.PUSH_IMAGE }
            }
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-hub-credentials') {
                        def image = docker.image("${IMAGE_NAME}:${params.TAG}")
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker system prune -f'
        }
        failure {
            emailext (
                subject: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Build failed. Check console output at ${env.BUILD_URL}",
                to: "team@example.com"
            )
        }
    }
}