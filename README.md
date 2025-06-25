# 🗜️ Data Compression Portal

A modern, web-based file compression and decompression tool with multiple algorithms and intelligent auto-detection capabilities.

## 🌟 Features

### Core Functionality
- **Multiple Compression Algorithms**: Huffman Coding, LZ77, Run-Length Encoding (RLE), Deflate (GZIP)
- **Smart Auto-Detection**: Automatically selects the optimal algorithm based on file type
- **Universal File Support**: Text, images, documents, binary files, executables
- **Real-time Processing**: Live progress tracking with animated UI
- **Detailed Statistics**: Compression ratios, processing time, file size comparisons
- **Interactive Charts**: Animated bar charts showing before/after comparison

### Supported File Types
- **Text Files**: `.txt`, `.html`, `.xml`, `.json`, `.csv`, `.log`, `.py`, `.js`, `.css`
- **Images**: `.bmp`, `.pcx`, `.tga`, `.ppm`, `.wav`
- **Documents**: `.pdf`, `.doc`, `.docx`, `.ppt`, `.xlsx`
- **Binary Files**: `.exe`, `.dll`, `.bin`, `.rar`, `.zip`
- **Any File Type**: Universal support for all file formats

## 🚀 Quick Start

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Web server (for backend processing)
- Python 3.7+ (for backend implementation)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anuj-m02/ComeOnPress
   cd data-compression-portal
   ```

2. **Set up the frontend**
   ```bash
   # Simply serve the HTML file
   python -m http.server 8000
   # OR use any web server of your choice
   ```

3. **Set up the backend** (Python Flask example)
   ```bash
   pip install flask
   python app.py
   ```

### Usage

1. **Open the Portal**
   - Navigate to `http://localhost:8000` in your browser

2. **Upload File**
   - Click "Choose File" button
   - Select any file from your computer
   - File information will be displayed

3. **Select Algorithm**
   - **Auto Detect (Recommended)**: Let the system choose the best algorithm
   - **Huffman Coding**: Best for text files with repeated patterns
   - **LZ77**: Optimal for binary files and executables
   - **Run-Length Encoding**: Perfect for images with solid areas
   - **Deflate (GZIP)**: General-purpose compression for all file types

4. **Process File**
   - Click "Compress File" or "Decompress File"
   - Watch the animated progress bar
   - View detailed statistics and charts

5. **Download Results**
   - Click "Download Processed File" when complete
   - File will be saved with appropriate extension

## 🏗️ Architecture

### Frontend Components
```
├── HTML Structure
│   ├── Upload Section
│   ├── Algorithm Selection
│   ├── Processing Controls
│   ├── Statistics Display
│   ├── Animated Charts
│   └── Download Section
├── CSS Styling
│   ├── Modern Gradient Design
│   ├── Responsive Layout
│   ├── Animation Effects
│   └── Interactive Elements
└── JavaScript Logic
    ├── File Handling
    ├── Algorithm Selection
    ├── API Communication
    ├── Chart Rendering
    └── Progress Tracking
```

### Backend API Endpoints

#### POST `/process`
Process file compression or decompression

**Request Body (FormData):**
```javascript
{
  file: File,           // File to process
  algorithm: string,    // 'auto', 'huffman', 'lz77', 'rle', 'deflate'
  operation: string     // 'compress' or 'decompress'
}
```

**Response:**
```json
{
  "success": true,
  "original_size": 1048576,
  "processed_size": 524288,
  "compression_ratio": "50.0",
  "processing_time": "1.23",
  "algorithm": "deflate",
  "filename": "compressed_file.gz",
  "file_data": [binary_data_array]
}
```

## 🎨 UI Components

### Algorithm Cards
- **Auto Detect**: Intelligent algorithm selection with golden highlighting
- **Manual Selection**: Four specialized algorithms with detailed descriptions
- **Visual Feedback**: Selected cards highlight with colored borders
- **Hover Effects**: Interactive animations for better UX

### Statistics Dashboard
- **Original vs Processed Size**: Side-by-side comparison
- **Compression Ratio**: Percentage reduction in file size
- **Processing Time**: Algorithm execution duration
- **Algorithm Used**: Which compression method was applied

### Animated Bar Chart
- **Growing Bars**: Smooth animation from bottom to top
- **Bounce Effects**: Elastic scaling with cubic-bezier timing
- **Hover Interactions**: Bars scale on mouse hover
- **Value Labels**: Animated pop-in with rotation effects

## 🔧 Configuration

### Algorithm Selection Logic
```javascript
const algorithmSelection = {
  'auto': {
    text: 'huffman',
    image: 'rle',
    binary: 'lz77',
    default: 'deflate'
  }
}
```

### File Type Detection
```javascript
const fileTypeMap = {
  '.txt': 'text',
  '.html': 'text',
  '.bmp': 'image',
  '.exe': 'binary',
  // ... more mappings
}
```

## 📊 Performance Metrics

### Compression Ratios (Typical)
- **Text Files**: 40-60% reduction
- **HTML/XML**: 60-80% reduction
- **Images (BMP)**: 50-90% reduction
- **Binary Files**: 20-40% reduction

### Processing Speed
- **Small Files (<1MB)**: Near-instantaneous
- **Medium Files (1-10MB)**: 1-5 seconds
- **Large Files (>10MB)**: 5-30 seconds

## 🎯 Algorithm Details

### Huffman Coding
- **Method**: Variable-length prefix coding
- **Best For**: Text files with character frequency patterns
- **Complexity**: O(n log n)
- **Ratio**: 30-50% compression

### LZ77
- **Method**: Dictionary-based sliding window
- **Best For**: Binary files with repeated sequences
- **Complexity**: O(n²) worst case
- **Ratio**: 40-70% compression

### Run-Length Encoding
- **Method**: Replace consecutive identical values
- **Best For**: Images with large solid areas
- **Complexity**: O(n)
- **Ratio**: 50-95% compression (highly variable)

### Deflate (GZIP)
- **Method**: LZ77 + Huffman combination
- **Best For**: General-purpose compression
- **Complexity**: O(n log n)
- **Ratio**: 50-80% compression

## 🔒 Security Considerations

- **File Validation**: Check file types and sizes before processing
- **Memory Management**: Limit file sizes to prevent memory exhaustion
- **Input Sanitization**: Validate all user inputs
- **CORS Policy**: Configure appropriate cross-origin settings

## 🐛 Troubleshooting

### Common Issues

**File Not Uploading**
- Check file size limits (default: 50MB)
- Ensure file is not corrupted
- Verify browser supports File API

**Processing Fails**
- File may be already compressed
- Check backend server status
- Verify algorithm selection

**Download Not Working**
- Check browser download permissions
- Ensure sufficient disk space
- Clear browser cache

### Error Messages
- `"Please select a file first!"` - No file uploaded
- `"Processing failed"` - Backend error
- `"Network error"` - Connection issues

## 📈 Future Enhancements

- [ ] **Additional Algorithms**: LZMA, Brotli, Zstandard
- [ ] **Batch Processing**: Multiple file compression
- [ ] **Cloud Storage**: Direct upload to cloud services
- [ ] **API Keys**: Rate limiting and authentication
- [ ] **Progressive Web App**: Offline functionality
- [ ] **Advanced Analytics**: Detailed compression statistics

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request


## 👥 Authors

- **Anuj Singh** - [YourGitHub](https://github.com/Anuj-m02)
