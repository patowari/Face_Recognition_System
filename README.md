# 🎭 Face Recognition System

A powerful and easy-to-use face recognition system built with Flask and Python. Register people with their photos and recognize them instantly!

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
<img width="1376" height="774" alt="image" src="https://github.com/user-attachments/assets/7b042bcc-abc7-44db-9a23-425b093130bd" />

## ✨ Features

- 📝 **Face Registration** - Register people with their photos, name, age, and gender
- 🔍 **Face Recognition** - Identify registered people from photos with confidence scores
- 👥 **People Management** - View, list, and delete registered people
- 🖼️ **Multiple Input Formats** - Support for file uploads and base64 encoded images
- 🌐 **REST API** - Clean and well-documented RESTful API
- 💻 **Web Interface** - Beautiful HTML/CSS frontend for easy interaction
- 🔄 **Real-time Processing** - Fast face detection and recognition
- 💾 **Persistent Storage** - Face data stored locally using pickle

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- CMake (for dlib installation on Windows)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/patowari/Face_Recognition_System.git
   cd Face_Recognition_System
   ```

2. **Install dependencies**
   ```bash
   # Install required packages
   pip install Flask flask-cors numpy Pillow setuptools

   # Install dlib (Windows users)
   pip install dlib-bin

   # Install face-recognition
   pip install --no-deps face-recognition face-recognition-models
   pip install git+https://github.com/ageitgey/face_recognition_models
   ```

   Or simply use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open the web interface**
   - Open `index.html` in your browser
   - Or visit `http://127.0.0.1:5000` for API documentation

## 📖 Usage

### Web Interface

1. **Register a Person**
   - Upload a clear photo with a single face
   - Enter name, age, and gender
   - Click "Register Person"

2. **Recognize a Face**
   - Upload a photo
   - Click "Recognize Face"
   - View the results with confidence score

3. **Manage People**
   - View all registered people
   - Delete individual entries
   - Clear all data

### API Endpoints

#### 1. Register a New Person
```http
POST /register
Content-Type: multipart/form-data

Parameters:
- image: Image file (JPEG, PNG, etc.)
- name: Person's name (string)
- age: Person's age (integer)
- gender: Person's gender (string)

Response:
{
  "success": true,
  "message": "Successfully registered John Doe",
  "person_id": 0,
  "metadata": {
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "registered_at": "2025-11-14T15:30:00.000000"
  }
}
```

#### 2. Recognize a Face
```http
POST /recognize
Content-Type: multipart/form-data

Parameters:
- image: Image file (JPEG, PNG, etc.)

Response (Success):
{
  "recognized": true,
  "name": "John Doe",
  "age": 30,
  "gender": "male",
  "confidence": 0.95,
  "person_id": 0
}

Response (Not Found):
{
  "recognized": false,
  "message": "Face not recognized"
}
```

#### 3. List All Registered People
```http
GET /list

Response:
{
  "count": 2,
  "people": [
    {
      "person_id": 0,
      "name": "John Doe",
      "age": 30,
      "gender": "male",
      "registered_at": "2025-11-14T15:30:00.000000"
    },
    {
      "person_id": 1,
      "name": "Jane Smith",
      "age": 28,
      "gender": "female",
      "registered_at": "2025-11-14T15:35:00.000000"
    }
  ]
}
```

#### 4. Delete a Person
```http
DELETE /delete/<person_id>

Response:
{
  "success": true,
  "message": "Deleted John Doe",
  "deleted": {
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "registered_at": "2025-11-14T15:30:00.000000"
  }
}
```

#### 5. Clear All Data
```http
POST /clear

Response:
{
  "success": true,
  "message": "Database cleared"
}
```

#### 6. Health Check
```http
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2025-11-14T15:30:00.000000"
}
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Face Recognition**: face_recognition library (dlib + OpenCV)
- **Image Processing**: PIL/Pillow, NumPy
- **Storage**: Pickle (local file storage)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Cross-Origin**: Flask-CORS

## 📁 Project Structure

```
khoma/
├── app.py              # Main Flask application
├── index.html          # Web interface
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── face_data.pkl      # Face encodings database (auto-generated)
```

## 🔧 Configuration

### API Settings
- **Host**: `0.0.0.0` (accessible from network)
- **Port**: `5000`
- **Debug Mode**: Enabled (disable for production)

### Recognition Settings
- **Tolerance**: `0.6` (lower = stricter matching)
- **Face Detection**: HOG-based (faster, CPU-friendly)

### Modify in `app.py`:
```python
# Change recognition tolerance
matches = face_recognition.compare_faces(data['encodings'], face_encoding, tolerance=0.6)

# Change server configuration
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🎯 Best Practices

1. **Photo Quality**
   - Use clear, well-lit photos
   - Face should be clearly visible
   - Avoid multiple faces in one photo for registration
   - Recommended resolution: 640x480 or higher

2. **Security**
   - Don't expose the API to the internet without authentication
   - Use HTTPS in production
   - Implement rate limiting for public APIs
   - Sanitize user inputs

3. **Performance**
   - Keep the database size reasonable (<1000 faces)
   - Use GPU acceleration for large-scale deployments
   - Consider using a proper database (PostgreSQL, MongoDB) instead of pickle

## 🚨 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'dlib'`
- **Solution**: Install dlib-bin: `pip install dlib-bin`

**Issue**: `CMake is not installed`
- **Solution**: Install CMake: `pip install cmake` or download from cmake.org

**Issue**: `Object of type int64 is not JSON serializable`
- **Solution**: Already fixed in the code with explicit type conversions

**Issue**: `No face detected in image`
- **Solution**: Ensure the photo has a clear, visible face with good lighting

**Issue**: `CORS error in browser`
- **Solution**: Make sure Flask-CORS is installed and configured

## 📊 Performance

- **Face Detection**: ~0.5-2 seconds per image (CPU)
- **Face Recognition**: ~0.1-0.5 seconds per comparison
- **Registration**: ~1-3 seconds per person
- **Recommended**: Use GPU for better performance with large databases

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Swochchho**
- GitHub: [@Swochchho](https://github.com/patowari)

## 🙏 Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition) by Adam Geitgey
- [dlib](http://dlib.net/) by Davis King
- [Flask](https://flask.palletsprojects.com/) framework

## 📧 Support

If you have any questions or need help, please open an issue on GitHub.

---

**⭐ If you find this project helpful, please consider giving it a star!**
