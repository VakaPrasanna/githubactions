pipeline {
    agent {
        label 'linux && docker'
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 2, unit: 'HOURS')
        timestamps()
        ansiColor('xterm')
        disableConcurrentBuilds()
    }
    
    triggers {
        cron('H 2 * * 1-5')
        pollSCM('H/15 * * * *')
    }
    
    parameters {
        choice(name: 'BUILD_TYPE', choices: ['release', 'snapshot', 'hotfix'], description: 'Type of build')
        string(name: 'VERSION', defaultValue: '1.0.0', description: 'Version number')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'Skip test execution')
        text(name: 'RELEASE_NOTES', defaultValue: '', description: 'Release notes')
    }
    
    environment {
        MAVEN_OPTS = '-Xmx2048m -XX:MaxPermSize=512m'
        SONAR_HOST_URL = 'https://sonarqube.company.com'
        ARTIFACTORY_URL = 'https://artifactory.company.com'
        DOCKER_REGISTRY = 'registry.company.com'
        APP_NAME = 'complex-app'
        BUILD_VERSION = "${params.VERSION}-${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Initialize') {
            steps {
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    
                    currentBuild.displayName = "#${env.BUILD_NUMBER} - ${params.BUILD_TYPE} - ${env.BUILD_VERSION}"
                }
                
                sh 'printenv | sort'
            }
        }
        
        stage('Code Quality Checks') {
            parallel {
                stage('Static Analysis') {
                    steps {
                        withSonarQubeEnv('SonarQube') {
                            sh '''
                                mvn sonar:sonar \
                                    -Dsonar.projectKey=${APP_NAME} \
                                    -Dsonar.projectVersion=${BUILD_VERSION}
                            '''
                        }
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        sh 'mvn org.owasp:dependency-check-maven:check'
                        
                        script {
                            def scanResults = sh(
                                script: 'find . -name "dependency-check-report.xml" | head -1',
                                returnStdout: true
                            ).trim()
                            
                            if (scanResults) {
                                publishHTML([
                                    allowMissing: false,
                                    alwaysLinkToLastBuild: true,
                                    keepAll: true,
                                    reportDir: 'target',
                                    reportFiles: 'dependency-check-report.html',
                                    reportName: 'OWASP Dependency Check'
                                ])
                            }
                        }
                    }
                }
                
                stage('License Check') {
                    steps {
                        sh 'mvn license:check'
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Build & Test') {
            when {
                not { params.SKIP_TESTS }
            }
            steps {
                sh 'mvn clean package -DskipITs=false'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: '**/target/surefire-reports/*.xml'
                    junit allowEmptyResults: true, testResults: '**/target/failsafe-reports/*.xml'
                    
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'target/site/jacoco',
                        reportFiles: 'index.html',
                        reportName: 'Code Coverage'
                    ])
                }
                success {
                    archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                script {
                    def image = docker.build("${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_VERSION}")
                    
                    // Security scan of the image
                    sh "trivy image --exit-code 0 --severity HIGH,CRITICAL ${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_VERSION}"
                    
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-creds') {
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                    expression { return params.BUILD_TYPE == 'release' }
                }
            }
            environment {
                DEPLOY_ENV = 'staging'
            }
            steps {
                withCredentials([kubeconfigFile(credentialsId: 'k8s-staging', variable: 'KUBECONFIG')]) {
                    sh '''
                        helm upgrade --install ${APP_NAME} ./helm/${APP_NAME} \
                            --namespace staging \
                            --create-namespace \
                            --set image.tag=${BUILD_VERSION} \
                            --set environment=staging \
                            --wait --timeout=10m
                    '''
                }
                
                // Health check
                sh '''
                    sleep 30
                    kubectl get pods -n staging
                    kubectl wait --for=condition=ready pod -l app=${APP_NAME} -n staging --timeout=300s
                '''
            }
        }
        
        stage('Integration Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                sh '''
                    mvn test -Dtest=IntegrationTest* \
                        -Dapp.url=https://staging.company.com \
                        -Dspring.profiles.active=integration
                '''
            }
            post {
                always {
                    junit 'target/surefire-reports/TEST-*IntegrationTest*.xml'
                }
            }
        }
        
        stage('Performance Tests') {
            when {
                expression { return params.BUILD_TYPE == 'release' }
            }
            steps {
                sh '''
                    jmeter -n -t performance-tests.jmx \
                        -Jhost=staging.company.com \
                        -Jusers=50 \
                        -Jrampup=300 \
                        -l results.jtl
                '''
            }
            post {
                always {
                    perfReport sourceDataFiles: 'results.jtl'
                }
            }
        }
        
        stage('Production Approval') {
            when {
                expression { return params.BUILD_TYPE == 'release' }
            }
            steps {
                script {
                    def approvers = ['john.doe', 'jane.smith', 'ops-team']
                    def approver = input(
                        message: 'Deploy to production?',
                        ok: 'Deploy',
                        submitterParameter: 'APPROVER',
                        submitter: approvers.join(','),
                        parameters: [
                            text(name: 'DEPLOYMENT_NOTES', defaultValue: params.RELEASE_NOTES, description: 'Deployment notes')
                        ]
                    )
                    env.APPROVER = approver.APPROVER
                    env.DEPLOYMENT_NOTES = approver.DEPLOYMENT_NOTES
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                expression { return params.BUILD_TYPE == 'release' && env.APPROVER }
            }
            environment {
                DEPLOY_ENV = 'production'
            }
            steps {
                withCredentials([kubeconfigFile(credentialsId: 'k8s-production', variable: 'KUBECONFIG')]) {
                    sh '''
                        # Blue-Green deployment
                        helm upgrade --install ${APP_NAME}-green ./helm/${APP_NAME} \
                            --namespace production \
                            --create-namespace \
                            --set image.tag=${BUILD_VERSION} \
                            --set environment=production \
                            --set deployment.color=green \
                            --wait --timeout=15m
                    '''
                    
                    // Switch traffic
                    sh '''
                        kubectl patch service ${APP_NAME} -n production \
                            -p '{"spec":{"selector":{"color":"green"}}}'
                    '''
                    
                    // Cleanup old deployment
                    sh '''
                        sleep 60
                        helm uninstall ${APP_NAME}-blue -n production || true
                        helm upgrade --install ${APP_NAME}-blue ./helm/${APP_NAME} \
                            --namespace production \
                            --set image.tag=${BUILD_VERSION} \
                            --set environment=production \
                            --set deployment.color=blue \
                            --set replicaCount=0
                    '''
                }
            }
        }
        
        stage('Post-Deploy Validation') {
            when {
                expression { return params.BUILD_TYPE == 'release' && env.APPROVER }
            }
            steps {
                sh '''
                    # Smoke tests
                    curl -f https://api.company.com/health
                    curl -f https://api.company.com/version | grep ${BUILD_VERSION}
                    
                    # Database connectivity
                    kubectl exec -n production deployment/${APP_NAME} -- \
                        /app/scripts/db-check.sh
                '''
            }
        }
    }
    
    post {
        always {
            script {
                def duration = currentBuild.durationString.replace(' and counting', '')
                def status = currentBuild.currentResult
                
                emailext (
                    subject: "${status}: ${env.JOB_NAME} - ${env.BUILD_DISPLAY_NAME}",
                    body: """
                        Build: ${env.BUILD_URL}
                        Duration: ${duration}
                        Commit: ${env.GIT_COMMIT_SHORT}
                        Build Type: ${params.BUILD_TYPE}
                        Version: ${env.BUILD_VERSION}
                        ${env.APPROVER ? "Approved by: ${env.APPROVER}" : ""}
                        ${env.DEPLOYMENT_NOTES ? "Notes: ${env.DEPLOYMENT_NOTES}" : ""}
                    """,
                    to: "team@company.com",
                    attachLog: status == 'FAILURE'
                )
            }
            
            cleanWs()
        }
        
        success {
            slackSend(
                channel: '#builds',
                color: 'good',
                message: "✅ ${env.JOB_NAME} #${env.BUILD_NUMBER} succeeded (${params.BUILD_TYPE})"
            )
        }
        
        failure {
            slackSend(
                channel: '#builds',
                color: 'danger',
                message: "❌ ${env.JOB_NAME} #${env.BUILD_NUMBER} failed (${params.BUILD_TYPE})"
            )
        }
        
        unstable {
            slackSend(
                channel: '#builds',
                color: 'warning',
                message: "⚠️ ${env.JOB_NAME} #${env.BUILD_NUMBER} unstable (${params.BUILD_TYPE})"
            )
        }
    }
}