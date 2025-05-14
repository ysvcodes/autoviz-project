// Jenkinsfile
/*
 * Initial Block Comment:
 * Author: Your Name (Replace with your actual name)
 * Project: autoviz-project
 * Purpose: Jenkins declarative pipeline for the autoviz-project.
 *          This pipeline automates the build, test, and deployment (simulated)
 *          of the application using Docker.
 *
 * Pipeline Stages:
 * 1. Checkout SCM: Clones the source code from the Git repository.
 * 2. Build Docker Image: Builds a Docker image using the Dockerfile.
 *    - Docker is used for containerization to ensure consistency.
 * 3. Run Unit Tests: Executes unit tests within a Docker container
 *    derived from the built image to ensure code quality.
 * 4. (Simulated) Deploy to Development: For this initial setup, "deploy" will mean
 *    running the Docker container. In a real scenario, this could involve
 *    pushing to a registry and deploying to a staging/production environment.
 *
 * This pipeline demonstrates:
 * - Automated builds triggered by Git changes (when configured in Jenkins job).
 * - Running automated tests.
 * - Containerizing the application using Docker.
 * - A basic deployment step orchestrated by Jenkins.
 */
pipeline {
    agent any // Specifies that Jenkins can use any available agent to run the pipeline.
              // For a simple setup where Jenkins controller has Docker, 'any' is fine.

    environment {
        // Define environment variables accessible throughout the pipeline
        DOCKER_IMAGE_NAME = "autoviz-project" // Name for your Docker image
        // BUILD_NUMBER is a built-in Jenkins environment variable
        // GIT_BRANCH is a built-in Jenkins environment variable (for multibranch pipelines or when SCM is configured)
    }

    stages {
        stage('Checkout SCM') {
            // Stage for checking out code from Version Control
            // Purpose: To get the latest source code for the pipeline.
            steps {
                script {
                    echo "Checking out source code..."
                    // This step is automatically handled by Jenkins when the job
                    // is configured to use 'Pipeline script from SCM' and points to your Git repo.
                    // You can explicitly call `checkout scm` if needed for specific scenarios,
                    // but usually it's implicit for the primary checkout.
                    // Example: checkout scm
                }
            }
        }

        stage('Build Docker Image') {
            // Stage for building the Docker image
            // Purpose: To package the application and its dependencies into a
            //          Docker image for consistent environments.
            // Docker is used here for containerization.
            steps {
                script {
                    echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
                    // docker.build() requires the Docker Pipeline plugin in Jenkins.
                    // The second argument './' specifies the build context (current directory where Dockerfile is).
                    def customImage = docker.build("${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}", "./")
                    echo "Successfully built ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"

                    // Tag the image as 'latest' as well for convenience.
                    // This tags it locally. It doesn't push to a remote registry yet.
                    customImage.push('latest')
                    echo "Tagged ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER} as ${DOCKER_IMAGE_NAME}:latest locally"
                }
            }
        }

        stage('Run Unit Tests') {
            // Stage for running automated tests
            // Purpose: To ensure code quality and that new changes haven't
            //          broken existing functionality. Tests are run inside the Docker environment.
            steps {
                script {
                    echo "Running unit tests inside a Docker container..."
                    // Uses the image built in the previous stage.
                    // The command runs the test_app.py script using python's unittest runner.
                    // If tests fail, this will throw an error and fail the stage.
                    docker.image("${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}").inside {
                        // Ensure your test script is executable and paths are correct within the container.
                        // The WORKDIR in your Dockerfile is /usr/src/app
                        // So, 'tests' folder should be directly accessible.
                        sh 'python -m unittest discover -s tests -p "test_*.py"'
                    }
                    echo "Unit tests completed successfully."
                }
            }
        }

        stage('(Simulated) Deploy to Development') {
            // Stage for deploying the application (simulated for now)
            // Purpose: To deploy the containerized application.
            //          In a real setup, this might involve pushing to a Docker registry
            //          and then deploying to Kubernetes, Docker Swarm, or another server.
            // Jenkins automates this deployment process.
            steps {
                script {
                    def containerName = "${DOCKER_IMAGE_NAME}-run"
                    echo "Simulating deployment of ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}..."
                    echo "In a real scenario, we would:"
                    echo "1. Push image to a Docker Registry (e.g., Docker Hub, ECR, GCR)"
                    // Example for pushing to a registry (requires registry credentials configured in Jenkins):
                    // docker.withRegistry('https://your-registry.com', 'your-jenkins-credentials-id') {
                    //    docker.image("${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}").push()
                    //    docker.image("${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}").push('latest') // Push latest tag too
                    // }
                    echo "2. Deploy the image to a staging/production environment (e.g., Kubernetes apply, docker-compose up, etc.)."
                    echo "For now, we'll just run the container locally on the Jenkins machine to show it works."

                    // Stop and remove any existing container with the same name to avoid conflicts
                    // Using --no-run-if-empty to prevent errors if no container is found
                    // Escaped the '$' in the regex for container name to prevent Groovy interpolation
                    sh "docker ps -q --filter name=^/${containerName}\\$ | xargs --no-run-if-empty docker stop"
                    sh "docker ps -aq --filter name=^/${containerName}\\$ | xargs --no-run-if-empty docker rm"

                    // Run the new container in detached mode
                    // We'll map port 5002 on the Jenkins host to port 5000 in the container
                    // to avoid clashes if Jenkins itself or other services use 5000.
                    sh "docker run -d --name ${containerName} -p 5002:5000 ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
                    echo "Application container '${containerName}' started."
                    echo "If Jenkins is running locally, try accessing the app at http://localhost:5002"
                }
            }
        }
    }

    post {
        // Post-pipeline actions that run after all stages complete
        always {
            echo 'Pipeline finished.'
            // Example: Clean up workspace or old Docker images if needed.
            // Be careful with `docker rmi` in a shared Jenkins environment or if you need to inspect images.
            // script {
            //     // Clean up older images of this project to save space (optional)
            //     // This is a very basic cleanup, more sophisticated strategies exist.
            //     def imagesToClean = sh(script: "docker images ${DOCKER_IMAGE_NAME} --format '{{.ID}} {{.Tag}}' | grep -v latest | grep -v ${env.BUILD_NUMBER} | awk '{print \$1}'", returnStdout: true).trim()
            //     if (imagesToClean) {
            //         sh "docker rmi -f ${imagesToClean}"
            //     }
            // }
        }
        success {
            echo 'Pipeline executed successfully!'
            // Example: Send notifications (Email, Slack, etc.)
        }
        failure {
            echo 'Pipeline failed.'
            // Example: Send notifications
        }
    }
}