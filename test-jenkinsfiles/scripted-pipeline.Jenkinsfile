node {
    stage('Checkout') {
        checkout scm
    }
    
    stage('Build') {
        try {
            sh 'mvn clean compile'
        } catch (Exception e) {
            currentBuild.result = 'FAILURE'
            throw e
        }
    }
    
    stage('Test') {
        parallel(
            'Unit Tests': {
                sh 'mvn test'
            },
            'Integration Tests': {
                sh 'mvn integration-test'
            }
        )
    }
    
    stage('Deploy') {
        if (env.BRANCH_NAME == 'main') {
            sh 'echo "Deploying to production"'
        } else {
            sh 'echo "Deploying to staging"'
        }
    }
}