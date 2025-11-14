from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import numpy as np
import base64
import io
from PIL import Image
import pickle
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Storage file for face encodings and metadata
STORAGE_FILE = 'face_data.pkl'

def load_data():
    """Load stored face encodings and metadata"""
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'rb') as f:
            return pickle.load(f)
    return {'encodings': [], 'metadata': []}

def save_data(data):
    """Save face encodings and metadata"""
    with open(STORAGE_FILE, 'wb') as f:
        pickle.dump(data, f)

def decode_image(image_data):
    """Decode base64 image or file upload"""
    try:
        # If it's base64 string
        if isinstance(image_data, str):
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        else:
            # If it's a file upload
            image = Image.open(image_data)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return np.array(image)
    except Exception as e:
        raise ValueError(f"Failed to decode image: {str(e)}")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/register', methods=['POST'])
def register_face():
    """
    Register a new person with their face and metadata
    Expected form data:
    - image: base64 string or file upload
    - name: person's name
    - age: person's age
    - gender: person's gender
    """
    try:
        # Get image
        if 'image' in request.files:
            image_data = request.files['image']
        elif 'image' in request.json:
            image_data = request.json['image']
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        # Get metadata
        name = request.form.get('name') or request.json.get('name')
        age = request.form.get('age') or request.json.get('age')
        gender = request.form.get('gender') or request.json.get('gender')
        
        if not all([name, age, gender]):
            return jsonify({'error': 'Name, age, and gender are required'}), 400
        
        # Decode image
        image_array = decode_image(image_data)
        
        # Find face encodings
        face_locations = face_recognition.face_locations(image_array)
        face_encodings = face_recognition.face_encodings(image_array, face_locations)
        
        if len(face_encodings) == 0:
            return jsonify({'error': 'No face detected in image'}), 400
        
        if len(face_encodings) > 1:
            return jsonify({'error': 'Multiple faces detected. Please provide image with single face'}), 400
        
        # Load existing data
        data = load_data()
        
        # Add new face encoding and metadata
        face_encoding = face_encodings[0]
        metadata = {
            'name': name,
            'age': int(age),
            'gender': gender,
            'registered_at': datetime.now().isoformat()
        }
        
        data['encodings'].append(face_encoding)
        data['metadata'].append(metadata)
        
        # Save data
        save_data(data)
        
        return jsonify({
            'success': True,
            'message': f'Successfully registered {name}',
            'person_id': len(data['encodings']) - 1,
            'metadata': metadata
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recognize', methods=['POST'])
def recognize_face():
    """
    Recognize a person from their face
    Expected data:
    - image: base64 string or file upload
    """
    try:
        # Get image
        if 'image' in request.files:
            image_data = request.files['image']
        elif 'image' in request.json:
            image_data = request.json['image']
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode image
        image_array = decode_image(image_data)
        
        # Find face encodings
        face_locations = face_recognition.face_locations(image_array)
        face_encodings = face_recognition.face_encodings(image_array, face_locations)
        
        if len(face_encodings) == 0:
            return jsonify({'error': 'No face detected in image'}), 400
        
        # Load stored data
        data = load_data()
        
        if len(data['encodings']) == 0:
            return jsonify({'error': 'No registered faces in database'}), 404
        
        # Check each detected face
        results = []
        for face_encoding in face_encodings:
            # Compare with stored encodings
            matches = face_recognition.compare_faces(data['encodings'], face_encoding, tolerance=0.6)
            face_distances = face_recognition.face_distance(data['encodings'], face_encoding)
            
            if True in matches:
                # Get best match
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    metadata = data['metadata'][best_match_index]
                    confidence = 1 - face_distances[best_match_index]
                    
                    results.append({
                        'recognized': True,
                        'name': metadata['name'],
                        'age': metadata['age'],
                        'gender': metadata['gender'],
                        'confidence': float(confidence),
                        'person_id': best_match_index
                    })
                else:
                    results.append({'recognized': False, 'message': 'Face not recognized'})
            else:
                results.append({'recognized': False, 'message': 'Face not recognized'})
        
        if len(results) == 1:
            return jsonify(results[0]), 200
        else:
            return jsonify({'faces': results}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list', methods=['GET'])
def list_people():
    """List all registered people"""
    try:
        data = load_data()
        people = []
        for i, metadata in enumerate(data['metadata']):
            people.append({
                'person_id': i,
                'name': metadata['name'],
                'age': metadata['age'],
                'gender': metadata['gender'],
                'registered_at': metadata.get('registered_at', 'Unknown')
            })
        return jsonify({'count': len(people), 'people': people}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    """Delete a registered person by ID"""
    try:
        data = load_data()
        
        if person_id < 0 or person_id >= len(data['encodings']):
            return jsonify({'error': 'Invalid person_id'}), 404
        
        deleted_metadata = data['metadata'][person_id]
        
        # Remove from lists
        del data['encodings'][person_id]
        del data['metadata'][person_id]
        
        # Save updated data
        save_data(data)
        
        return jsonify({
            'success': True,
            'message': f'Deleted {deleted_metadata["name"]}',
            'deleted': deleted_metadata
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_database():
    """Clear all registered faces (use with caution)"""
    try:
        data = {'encodings': [], 'metadata': []}
        save_data(data)
        return jsonify({'success': True, 'message': 'Database cleared'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Face Recognition API Starting...")
    print("Available endpoints:")
    print("  POST /register - Register a new face")
    print("  POST /recognize - Recognize a face")
    print("  GET /list - List all registered people")
    print("  DELETE /delete/<person_id> - Delete a person")
    print("  POST /clear - Clear all data")
    print("  GET /health - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)