# ReadWise Technical Overview

## 1. Project Overview
ReadWise is a modern mobile application designed to enhance the reading experience by leveraging Artificial Intelligence. It allows users to upload books (PDF/EPUB), automatically parses them into chapters, and generates AI-powered summaries, key points, and discussion questions for each chapter. The goal is to help users retain more information and engage deeply with their reading material.

## 2. Architecture
The project follows a classic Client-Server architecture:

*   **Frontend (Mobile App)**: A cross-platform mobile application built with React Native and Expo SDK 54 latest. It handles user interaction, file selection, and displaying the reading interface.
*   **Backend (API)**: A RESTful API built with Python and FastAPI. It handles file processing, AI generation, and data persistence.

### Communication
The frontend communicates with the backend via HTTP requests (REST API). File uploads are handled via multipart/form-data, while data retrieval uses standard JSON responses.

## 3. Features & Functionalities

### Core Features
1.  **Book Management**
    *   **Upload**: Users can upload books in PDF or EPUB formats.
    *   **Library**: A view to list all uploaded books with their progress.
    *   **Parsing**: The system automatically extracts text and structure (chapters) from the uploaded files.

2.  **AI-Enhanced Reading**
    *   **Summarization**: Each chapter is analyzed to generate a concise summary.
    *   **Key Points**: Extraction of the most important concepts from the text.
    *   **Interactive Questions**: Generation of thought-provoking questions to test understanding.

3.  **Reading Interface**
    *   **Chapter Navigation**: Users can browse through chapters.
    *   **Progress Tracking**: The app tracks reading progress (e.g., percentage completed).
    *   **Interactive UI**: Clean and modern interface for reading text and viewing AI insights.

4.  **Dashboard**
    *   **Overview**: Displays reading statistics and recently accessed books.
    *   **Quick Actions**: Easy access to resume reading or upload new content.

## 4. Data Entities (Conceptual)

### Book
Represents a single uploaded document.
*   **Attributes**: Title, Author, Total Chapters, Reading Progress, Creation Date.
*   **Relationships**: Contains multiple Chapters.

### Chapter
Represents a section of a book.
*   **Attributes**: Title, Content (Text), Summary (AI), Key Points (AI), Questions (AI), Completion Status.

## 5. Technology Stack

### Frontend (Mobile)
*   **Framework**: **React Native** with **Expo** (Managed Workflow).
*   **Routing**: **Expo Router** for file-based navigation.
*   **Language**: **TypeScript** for type safety.
*   **State Management**: **Zustand** for lightweight global state.
*   **UI/Styling**: Standard React Native styling (likely with utility libraries or custom components).
*   **Networking**: Native `fetch` or `axios` (implied) for API calls.

### Backend (API)
*   **Framework**: **FastAPI** (Python) for high-performance async API endpoints.
*   **Language**: **Python 3.x**.
*   **AI Integration**: Integration with LLM providers (e.g., OpenAI) for text analysis.
*   **File Processing**: Libraries for parsing PDF and EPUB files.
*   **Task Queue**: Background tasks (FastAPI `BackgroundTasks`) for handling long-running AI operations without blocking the UI.

## 6. Development Philosophy
This project is designed to be modular and scalable.
*   **Separation of Concerns**: The backend handles heavy lifting (parsing, AI), while the frontend focuses on presentation and user experience.
*   **MVP Approach**: The current iteration uses in-memory storage for simplicity, allowing for rapid prototyping. A production version would replace this with a persistent database (e.g., PostgreSQL, SQLite).
*   **Async Processing**: Heavy operations like AI generation are offloaded to background tasks to ensure the API remains responsive.
