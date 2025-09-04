pipeline {
    agent none
    
    parameters {
        choice(name: 'MATRIX_TYPE', choices: ['full', 'minimal'], description: 'Matrix build type')
    }
    
    stages {
        stage('Matrix Build') {
            matrix {
                axes {
                    axis {
                        name 'JAVA_VERSION'
                        values '11', '17', '21'
                    }
                    axis {
                        name 'OS'
                        values 'ubuntu', 'windows', 'macos'
                    }
                }
                excludes {
                    exclude {
                        axis {
                            name 'JAVA_VERSION'
                            values '21'
                        }
                        axis {
                            name 'OS'
                            values 'windows'
                        }
                    }
                }
                stages {
                    stage('Build on Matrix') {
                        agent {
                            label "${OS}"
                        }
                        tools {
                            jdk "jdk-${JAVA_VERSION}"
                        }
                        steps {
                            sh 'java -version'
                            sh 'mvn clean test'
                        }
                    }
                }
            }
        }
        
        stage('Collect Results') {
            agent any
            steps {
                echo 'Collecting matrix build results'
            }
        }
    }
}