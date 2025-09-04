pipeline {
    agent any
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Deployment environment')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag to deploy')
        booleanParam(name: 'RUN_MIGRATIONS', defaultValue: false, description: 'Run database migrations?')
    }
    
    environment {
        KUBECONFIG = credentials('kubeconfig')
        HELM_CHART_PATH = './helm/myapp'
        NAMESPACE = "${params.ENVIRONMENT}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Validate Kubernetes Config') {
            steps {
                sh 'kubectl cluster-info'
                sh 'helm version'
            }
        }
        
        stage('Database Migration') {
            when {
                expression { return params.RUN_MIGRATIONS }
            }
            steps {
                sh '''
                    kubectl create job migration-${BUILD_NUMBER} \
                        --from=cronjob/db-migration \
                        --namespace=${NAMESPACE}
                    kubectl wait --for=condition=complete job/migration-${BUILD_NUMBER} \
                        --timeout=300s --namespace=${NAMESPACE}
                '''
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    def valuesFile = "values-${params.ENVIRONMENT}.yaml"
                    sh """
                        helm upgrade --install myapp ${HELM_CHART_PATH} \
                            --namespace ${NAMESPACE} \
                            --create-namespace \
                            --values ${HELM_CHART_PATH}/${valuesFile} \
                            --set image.tag=${params.IMAGE_TAG} \
                            --wait --timeout=10m
                    """
                }
            }
        }
        
        stage('Smoke Tests') {
            steps {
                script {
                    def appUrl = sh(
                        script: "kubectl get ingress myapp -n ${NAMESPACE} -o jsonpath='{.spec.rules[0].host}'",
                        returnStdout: true
                    ).trim()
                    
                    sh "curl -f https://${appUrl}/health"
                    sh "curl -f https://${appUrl}/api/status"
                }
            }
        }
        
        stage('Production Approval') {
            when {
                expression { return params.ENVIRONMENT == 'production' }
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy',
                      submitterParameter: 'APPROVER'
            }
        }
    }
    
    post {
        success {
            slackSend(
                channel: '#deployments',
                color: 'good',
                message: "✅ Deployment to ${params.ENVIRONMENT} successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
        failure {
            slackSend(
                channel: '#deployments',
                color: 'danger',
                message: "❌ Deployment to ${params.ENVIRONMENT} failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}