"""
Script to load textbook content into the vector database for RAG chatbot.

This script will read textbook content and index it in Qdrant for semantic search.
"""

import asyncio
import os
import logging
from typing import List, Dict, Any

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.services.vector_service import VectorService
from api.services.cohere_service import CohereService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def load_sample_content():
    """
    Load sample textbook content into the vector database.
    In a real scenario, this would read from actual textbook files.
    """
    vector_service = VectorService()
    cohere_service = CohereService()

    # Sample textbook content about robotics
    sample_documents = [
        {
            "chapter_slug": "intro-robotics",
            "module_name": "Introduction to Robotics",
            "chunk_index": 1,
            "content": "Robotics is an interdisciplinary field that combines engineering and computer science to design, construct, operate, and use robots. Robots are programmable machines capable of carrying out a series of actions autonomously or semi-autonomously."
        },
        {
            "chapter_slug": "intro-robotics",
            "module_name": "Introduction to Robotics",
            "chunk_index": 2,
            "content": "The word 'robot' comes from the Czech word 'robota', meaning forced labor. The term was first used in Karel Capek's 1921 play R.U.R. (Rossum's Universal Robots). Modern robotics integrates fields such as mechanical engineering, electrical engineering, computer science, and artificial intelligence."
        },
        {
            "chapter_slug": "kinematics",
            "module_name": "Robot Kinematics",
            "chunk_index": 1,
            "content": "Kinematics is the study of motion without considering the forces that cause it. In robotics, kinematics deals with the relationship between the joint variables and the position and orientation of the robot's end-effector. Forward kinematics calculates the end-effector position given joint angles, while inverse kinematics determines joint angles needed to achieve a desired end-effector position."
        },
        {
            "chapter_slug": "kinematics",
            "module_name": "Robot Kinematics",
            "chunk_index": 2,
            "content": "The Jacobian matrix is a fundamental concept in robot kinematics that relates joint velocities to end-effector velocities. It is particularly important in differential kinematics and plays a crucial role in robot control and trajectory planning."
        },
        {
            "chapter_slug": "inverse-kinematics",
            "module_name": "Inverse Kinematics",
            "chunk_index": 1,
            "content": "Inverse kinematics (IK) is the process of determining the joint angles required to achieve a desired end-effector position and orientation. This is a fundamental problem in robotics, particularly for robotic arms and humanoid robots. The solution to inverse kinematics can be analytical for simple robots or numerical for complex multi-joint robots."
        },
        {
            "chapter_slug": "inverse-kinematics",
            "module_name": "Inverse Kinematics",
            "chunk_index": 2,
            "content": "Analytical solutions for inverse kinematics exist for robots with specific geometric arrangements. For a 6-DOF robot with a spherical wrist, the position and orientation problems can be decoupled. Numerical methods like the Jacobian transpose method, Jacobian pseudoinverse method, and damped least squares are used for more complex robots."
        },
        {
            "chapter_slug": "pid-control",
            "module_name": "PID Controllers",
            "chunk_index": 1,
            "content": "PID (Proportional-Integral-Derivative) controllers are the most commonly used feedback controllers in robotics and automation. A PID controller calculates an error value as the difference between a desired setpoint and a measured process variable, then applies a correction based on proportional, integral, and derivative terms."
        },
        {
            "chapter_slug": "pid-control",
            "module_name": "PID Controllers",
            "chunk_index": 2,
            "content": "The integral term accounts for past values of the error, accumulating a 'sum of error' over time. The derivative term estimates the future trend of the error based on its current rate of change. Proper tuning of PID parameters (Kp, Ki, Kd) is crucial for stable and responsive control."
        },
        {
            "chapter_slug": "humanoid-locomotion",
            "module_name": "Humanoid Robot Locomotion",
            "chunk_index": 1,
            "content": "Humanoid robot locomotion is one of the most challenging problems in robotics. Unlike wheeled robots, humanoid robots must maintain balance while walking on two legs. This requires sophisticated control algorithms and understanding of human-like gait patterns. Common approaches include Zero Moment Point (ZMP) control and Capture Point (CP) methods."
        },
        {
            "chapter_slug": "humanoid-locomotion",
            "module_name": "Humanoid Robot Locomotion",
            "chunk_index": 2,
            "content": "Balance control in humanoid robots involves maintaining the center of mass within the support polygon defined by the feet. Advanced techniques include whole-body control, where multiple tasks (balance, walking, manipulation) are combined using optimization methods. The Linear Inverted Pendulum Model (LIPM) is often used to simplify balance control for humanoid robots."
        }
    ]

    logger.info(f"Loading {len(sample_documents)} textbook chunks into vector database...")

    # Generate embeddings for all documents
    documents_with_embeddings = []
    for i, doc in enumerate(sample_documents):
        logger.info(f"Processing document {i+1}/{len(sample_documents)}")
        try:
            embedding = await cohere_service.generate_embedding(doc['content'])
            documents_with_embeddings.append({
                'document': doc,
                'embedding': embedding
            })
        except Exception as e:
            logger.error(f"Error generating embedding for document {i+1}: {e}")
            continue

    # Prepare documents and embeddings for upsert
    documents = [item['document'] for item in documents_with_embeddings]
    embeddings = [item['embedding'] for item in documents_with_embeddings]

    if documents:
        try:
            await vector_service.upsert_documents(documents, embeddings)
            logger.info(f"Successfully loaded {len(documents)} textbook chunks into vector database!")
            logger.info("Textbook content is now available for semantic search in the chatbot.")
        except Exception as e:
            logger.error(f"Error upserting documents: {e}")
    else:
        logger.error("No documents were processed successfully.")


if __name__ == "__main__":
    asyncio.run(load_sample_content())