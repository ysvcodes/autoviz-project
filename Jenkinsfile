// Jenkinsfile for autoviz-project (inspired by example)
/*
 * Author: autoviz-project user
 * Project: autoviz-project
 * Purpose: Jenkins declarative pipeline for the autoviz-project.
 *          Automates build, test, and simulated deployment using Docker.
 *          Uses 'bat' for Windows compatibility.
 */
pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'autoviz-project'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = "${DOCKER_IMAGE_NAME}-container"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Build and Test') {
            steps {
                script {
                    echo "Starting Build and Test stage..."
                    try {
                        echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                        bat "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} -f app/Dockerfile app"
                        echo "Docker image built successfully."

                        echo "Running tests inside the container..."
                        bat "docker run --rm ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} pytest tests/"
                        echo "Tests completed."

                    } catch (Exception e) {
                        echo "Build or test failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error("Build or test stage failed: ${e.message}")
                    }
                }
            }
        }

        stage('Deploy (Simulated)') {
            steps {
                script {
                    echo "Starting Deploy (Simulated) stage..."
                    try {
                        echo "Attempting to stop existing container: ${CONTAINER_NAME}"
                        bat "docker stop ${CONTAINER_NAME}"
                        echo "Attempting to remove existing container: ${CONTAINER_NAME}"
                        bat "docker rm ${CONTAINER_NAME}"
                        echo "Cleanup of existing container successful (if it existed)."
                    } catch (Exception e) {
                        echo "No existing container named '${CONTAINER_NAME}' to clean up, or an error occurred: ${e.message}"
                    }

                    try {
                        echo "Deploying new container: ${CONTAINER_NAME} from image ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                        bat "docker run -d -p 8001:5000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                        echo "Deployment successful. Container '${CONTAINER_NAME}' started."
                        echo "Access at http://localhost:8001 if Jenkins runs locally."
                    } catch (Exception e) {
                        echo "Deployment failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error("Deployment stage failed: ${e.message}")
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Cleaning up workspace..."
            cleanWs()
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}
