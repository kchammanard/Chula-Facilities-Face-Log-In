# Face Recognition and Access Control Prototype for Chulalongkorn University

This project implements a real-time face recognition and access control system using OpenCV, face_recognition, and MongoDB. The system captures a live video stream, detects and encodes faces, and checks access permissions based on the recognized faces. It integrates with a MongoDB database to retrieve user and facility details and allows for checking access permissions dynamically.

## Features

- **Real-time Face Detection and Recognition**: Uses the `face_recognition` library to detect and compare faces with known encodings.
- **MongoDB Integration**: Connects to a MongoDB database to store and retrieve student and facility data.
- **Access Control**: Determines access to facilities based on a predefined entry policy stored in the database.
- **Live Video Feed**: Captures video from a webcam using OpenCV to display real-time recognition results.
- **Facility Selection**: Allows the user to choose a facility where access control is enforced.
- **Customizable UI**: Displays user details and access status using overlay images and custom graphics with OpenCV.

## Libraries Used

- `OpenCV`: For handling real-time video capture and display.
- `face_recognition`: For encoding and comparing faces.
- `cvzone`: For advanced graphical overlays on video frames.
- `MongoDB (pymongo)`: For storing and retrieving user, face, and facility data.
- `hashlib`: For hashing face encodings for secure storage.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/face-recognition-access-control.git
2. **Ensure MongoDB is running:** Verify that MongoDB is installed and running on your system. You can use the `mongod` command in your terminal to start the MongoDB server.
3. **Create necessary collections:** Use the `mongo` shell to create the following collections in your MongoDB database:
   ```javascript
   db.createCollection("students");
   db.createCollection("face");
   db.createCollection("facility");
   db.createCollection("activity");
   db.createCollection("entry");
4.Replace the MongoDB connection string with your own MongoDB cluster details.

5. Place background images and mode images in the Resources folder.

6. Run the Python script to start the system:
