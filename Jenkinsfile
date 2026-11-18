pipeline {
    agent any
    triggers { githubPush() }
    environment {
        IMAGE = 'midterm-fa23-bds-049'
    }
    stages {
        stage('Fetch latest data') {
            steps {
                checkout scm
                script {
                    env.GIT_SHA = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                }
            }
        }
        stage('Train and Test') {
            steps {
                sh '''
                docker run --rm -u $(id -u):$(id -g) -e HOME=/tmp -e GIT_COMMIT=$GIT_SHA \
                  -v "$WORKSPACE":/app -w /app python:3.11-slim \
                  sh -c "pip install --user -q -r requirements.txt pytest && python train.py && python -m pytest -q"
                '''
            }
        }
        stage('Build Docker image') {
            steps {
                sh 'docker build --build-arg GIT_COMMIT=$GIT_SHA -t $IMAGE:latest .'
            }
        }
        stage('Deploy on EC2') {
            steps {
                sh '''
                docker rm -f $IMAGE || true
                docker run -d --name $IMAGE --restart unless-stopped -p 8000:8000 $IMAGE:latest
                sleep 8
                curl -sf http://localhost:8000/metrics
                '''
            }
        }
    }
    post {
        always {
            withCredentials([usernamePassword(credentialsId: 'gmail-smtp', usernameVariable: 'MAIL_USER', passwordVariable: 'MAIL_PASS')]) {
                sh "docker run --rm -e MAIL_USER -e MAIL_PASS -v \"\$WORKSPACE\":/app:ro -w /app python:3.11-slim python send_mail.py ${currentBuild.currentResult} \$GIT_SHA"
            }
        }
    }
}
