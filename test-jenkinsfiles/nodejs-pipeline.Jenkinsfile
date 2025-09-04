pipeline {
    agent {
        docker {
            image 'node:18-alpine'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        NODE_ENV = 'test'
        NPM_CONFIG_CACHE = '/tmp/.npm'
        CYPRESS_CACHE_FOLDER = '/tmp/.cache/Cypress'
    }
    
    parameters {
        choice(name: 'NODE_VERSION', choices: ['16', '18', '20'], description: 'Node.js version')
        booleanParam(name: 'RUN_E2E_TESTS', defaultValue: false, description: 'Run end-to-end tests')
        string(name: 'DEPLOY_BRANCH', defaultValue: 'main', description: 'Branch to deploy')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'node --version'
                sh 'npm --version'
                sh 'npm ci --prefer-offline --no-audit'
            }
        }
        
        stage('Lint & Format') {
            parallel {
                stage('ESLint') {
                    steps {
                        sh 'npm run lint'
                    }
                    post {
                        always {
                            publishHTML([
                                allowMissing: true,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'reports',
                                reportFiles: 'eslint.html',
                                reportName: 'ESLint Report'
                            ])
                        }
                    }
                }
                
                stage('Prettier') {
                    steps {
                        sh 'npm run format:check'
                    }
                }
                
                stage('Type Check') {
                    steps {
                        sh 'npm run type-check'
                    }
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                sh 'npm run test:unit -- --coverage --watchAll=false'
            }
            post {
                always {
                    junit 'reports/jest-junit.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'coverage/lcov-report',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm run build'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'dist/**/*', fingerprint: true
                }
            }
        }
        
        stage('Security Audit') {
            steps {
                sh 'npm audit --audit-level=high'
                sh 'npx retire --outputformat=json --outputpath=retire-report.json || true'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'retire-report.json', allowEmptyArchive: true
                }
            }
        }
        
        stage('E2E Tests') {
            when {
                expression { return params.RUN_E2E_TESTS }
            }
            steps {
                sh '''
                    npm run start:test &
                    sleep 30
                    npm run test:e2e
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'cypress/screenshots/**/*', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'cypress/videos/**/*', allowEmptyArchive: true
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch params.DEPLOY_BRANCH
            }
            steps {
                sh '''
                    echo "Deploying to staging..."
                    npm run deploy:staging
                '''
            }
        }
    }
    
    post {
        always {
            sh 'pkill -f "npm run start:test" || true'
        }
        failure {
            emailext (
                subject: "Node.js Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "The Node.js build has failed. Please check the console output.",
                to: "frontend-team@company.com"
            )
        }
    }
}