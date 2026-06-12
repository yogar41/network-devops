pipeline {

    agent any

    environment {

        NET_USERNAME = credentials('net-user')
        NET_PASSWORD = credentials('net-pass')

        ANSIBLE_HOST_KEY_CHECKING = "False"
    }

    stages {

        stage('Checkout') {

            steps {

                git branch: 'main',
                url: 'git@github.com:yogar41/network-devops.git', credentialId: 'yoga-github-cred'
            }
        }

        stage('Install Dependencies') {

            steps {

                sh '''

                python3 -m venv venv

                . venv/bin/activate

                pip install --upgrade pip

                pip install -r requirements.txt

                '''
            }
        }

        stage('Deploy Configuration - Python') {

            steps {

                sh '''

                . venv/bin/activate

                python configs/onboarding.py

                '''
            }
        }

        stage('Validate Configuration - Ansible') {

            steps {

                sh '''

                . venv/bin/activate

                export ANSIBLE_USER=$NET_USERNAME

                export ANSIBLE_PASSWORD=$NET_PASSWORD

                cd ansible

                ansible-playbook validate.yml \
                  -u $NET_USERNAME \
                  -e ansible_password=$NET_PASSWORD

                '''
            }
        }

        stage('Archive Evidence') {

            steps {

                archiveArtifacts(
                    artifacts: '''
                    proofs/**,
                    backups/**,
                    reports/**
                    ''',
                    fingerprint: true
                )
            }
        }
    }

    post {

        always {

            junit allowEmptyResults: true,
                  testResults: 'reports/*.xml'
        }

        success {

            echo 'Deployment and validation completed.'
        }

        failure {

            echo 'Pipeline failed.'
        }
    }
}
