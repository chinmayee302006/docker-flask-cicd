pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'ghcr.io/chinmayee302006/my-flask-app'
        CONTAINER_NAME = 'flask-cicd'
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {

        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'docker run -d --name flask-test-%BUILD_NUMBER% --mount "type=bind,source=%WORKSPACE%,target=/workspace,readonly" python:3.12-slim sleep 3600'

                bat 'docker exec flask-test-%BUILD_NUMBER% pip install -r /workspace/requirements.txt'
            }
        }

        stage('Run Application Tests') {
            steps {
                bat 'docker exec -w /workspace flask-test-%BUILD_NUMBER% python -B -m unittest -v test_app'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:ci-%BUILD_NUMBER% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                bat 'docker push %IMAGE_NAME%:ci-%BUILD_NUMBER%'
            }
        }

        stage('Deploy Container') {
            steps {
                powershell '''
                $existing = docker ps -aq --filter "name=^/flask-cicd$"

                if ($LASTEXITCODE -ne 0) {
                    throw "Docker access failed"
                }

                if ($existing) {
                    docker rm -f flask-cicd

                    if ($LASTEXITCODE -ne 0) {
                        throw "Container removal failed"
                    }
                }

                docker run -d --name flask-cicd -p 127.0.0.1:5001:5000 -e APP_ENV=production "$($env:IMAGE_NAME):ci-$($env:BUILD_NUMBER)"

                if ($LASTEXITCODE -ne 0) {
                    throw "Deployment failed"
                }

                Write-Output "Container deployed successfully"
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                powershell '''
                for ($i = 0; $i -lt 15; $i++) {
                    try {
                        $response = Invoke-RestMethod -Uri http://localhost:5001/api/health -TimeoutSec 5

                        if ($response.status -eq "healthy") {
                            Write-Output "Deployment successful"
                            exit 0
                        }
                    }
                    catch {
                        Write-Output "Checking application..."
                    }

                    Start-Sleep -Seconds 2
                }

                throw "Application health check failed"
                '''
            }
        }
    }

    post {
        always {
            bat(
                script: 'docker rm -f flask-test-%BUILD_NUMBER%',
                returnStatus: true
            )
        }

        success {
            echo 'CI/CD Pipeline Completed Successfully!'
        }

        failure {
            echo 'Pipeline Failed. Check Console Output.'
        }
    }
}