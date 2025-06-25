from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import time
import io
import base64
import heapq
from collections import defaultdict, Counter
import json
import zlib
import gzip
import filetype
import zlib, bz2, lzma, gzip


app = Flask(__name__)
CORS(app)

# ===============================
# HUFFMAN CODING IMPLEMENTATION (CORRECTED)
# ===============================

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_codes = {}
    
    def build_frequency_table(self, data):
        return Counter(data)
    
    def build_huffman_tree(self, freq_table):
        if not freq_table:
            return None
            
        heap = []
        for char, freq in freq_table.items():
            heapq.heappush(heap, HuffmanNode(char, freq))
        
        # Handle single character case
        if len(heap) == 1:
            single_node = heapq.heappop(heap)
            root = HuffmanNode(None, single_node.freq)
            root.left = single_node
            return root
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)
        
        return heap[0] if heap else None
    
    def build_codes(self, root, code=""):
        if root is None:
            return
        
        if root.char is not None:
            # Assign code (use "0" for single character)
            self.codes[root.char] = code if code else "0"
            return
        
        self.build_codes(root.left, code + "0")
        self.build_codes(root.right, code + "1")
    
    def compress(self, data):
        if not data:
            return b'', {'original_length': 0, 'freq_table': {}}
        
        # Build frequency table
        freq_table = self.build_frequency_table(data)
        
        # Build Huffman tree
        root = self.build_huffman_tree(freq_table)
        if root is None:
            return b'', {'original_length': len(data), 'freq_table': dict(freq_table)}
        
        # Build codes
        self.codes = {}
        self.build_codes(root)
        
        # Compress data
        bit_string = ""
        for byte in data:
            bit_string += self.codes[byte]
        
        # Pad to make byte-aligned
        padding = 8 - len(bit_string) % 8
        if padding != 8:
            bit_string += "0" * padding
        
        # Convert to bytes
        compressed_data = bytearray()
        for i in range(0, len(bit_string), 8):
            byte = bit_string[i:i+8]
            compressed_data.append(int(byte, 2))
        
        metadata = {
            'freq_table': dict(freq_table),
            'padding': padding,
            'original_length': len(data)
        }
        
        return bytes(compressed_data), metadata
    
    def decompress(self, compressed_data, metadata):
        if not compressed_data or not metadata.get('freq_table'):
            return b''
        
        # Rebuild tree
        freq_table = metadata['freq_table']
        root = self.build_huffman_tree(freq_table)
        if root is None:
            return b''
        
        # Convert compressed data to bit string
        bit_string = ""
        for byte in compressed_data:
            bit_string += format(byte, '08b')
        
        # Remove padding
        padding = metadata.get('padding', 0)
        if padding != 8 and padding > 0:
            bit_string = bit_string[:-padding]
        
        # Decode
        decoded_data = bytearray()
        current_node = root
        
        # Handle single character case
        if root.char is not None:
            # Single character, repeat for original length
            original_length = metadata.get('original_length', 0)
            decoded_data.extend([root.char] * original_length)
            return bytes(decoded_data)
        
        for bit in bit_string:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right
            
            if current_node.char is not None:
                decoded_data.append(current_node.char)
                current_node = root
        
        return bytes(decoded_data)

# ===============================
# LZ77 IMPLEMENTATION (CORRECTED)
# ===============================

class LZ77:
    def __init__(self, window_size=4096, look_ahead_size=18):
        self.window_size = window_size
        self.look_ahead_size = look_ahead_size
    
    def compress(self, data):
        if not data:
            return b'', {'original_length': 0}
        
        compressed = []
        i = 0
        
        while i < len(data):
            match_length = 0
            match_offset = 0
            
            # Search for matches in the sliding window
            start = max(0, i - self.window_size)
            max_length = min(self.look_ahead_size, len(data) - i)
            
            # Find longest match
            for j in range(start, i):
                length = 0
                while (length < max_length and 
                       i + length < len(data) and
                       data[j + length] == data[i + length]):
                    length += 1
                
                if length > match_length:
                    match_length = length
                    match_offset = i - j
            
            if match_length >= 3:  # Use match only if beneficial
                next_char = data[i + match_length] if i + match_length < len(data) else 0
                compressed.append((match_offset, match_length, next_char))
                i += match_length + (1 if i + match_length < len(data) else 0)
            else:
                compressed.append((0, 0, data[i]))
                i += 1
        
        # Serialize compressed data
        compressed_bytes = bytearray()
        for offset, length, char in compressed:
            # Pack: offset (2 bytes), length (1 byte), char (1 byte)
            compressed_bytes.extend([
                (offset >> 8) & 0xFF,
                offset & 0xFF,
                length & 0xFF,
                char & 0xFF
            ])
        
        metadata = {'original_length': len(data)}
        return bytes(compressed_bytes), metadata
    
    def decompress(self, compressed_data, metadata):
        if not compressed_data:
            return b''
        
        decompressed = bytearray()
        i = 0
        
        while i + 3 < len(compressed_data):
            # Unpack: offset (2 bytes), length (1 byte), char (1 byte)
            offset = (compressed_data[i] << 8) | compressed_data[i + 1]
            length = compressed_data[i + 2]
            char = compressed_data[i + 3]
            
            if offset > 0 and length > 0:
                # Copy from sliding window
                start_pos = len(decompressed) - offset
                for j in range(length):
                    if start_pos + j >= 0 and start_pos + j < len(decompressed):
                        decompressed.append(decompressed[start_pos + j])
            
            # Add next character
            if char != 0 or (offset == 0 and length == 0):
                decompressed.append(char)
            
            i += 4
        
        return bytes(decompressed)

# ===============================
# RLE IMPLEMENTATION (CORRECTED)
# ===============================

class RunLengthEncoding:
    def compress(self, data):
        if not data:
            return b'', {'original_length': 0}
        
        compressed = bytearray()
        i = 0
        
        while i < len(data):
            current_byte = data[i]
            count = 1
            
            # Count consecutive bytes
            while i + count < len(data) and data[i + count] == current_byte and count < 255:
                count += 1
            
            if count >= 4:  # Use RLE for runs of 4 or more
                compressed.append(255)  # Escape marker
                compressed.append(count)
                compressed.append(current_byte)
            else:
                # Store bytes normally, escape 255
                for _ in range(count):
                    if current_byte == 255:
                        compressed.append(255)  # Escape
                        compressed.append(1)    # Count
                        compressed.append(255)  # Value
                    else:
                        compressed.append(current_byte)
            
            i += count
        
        metadata = {'original_length': len(data)}
        return bytes(compressed), metadata
    
    def decompress(self, compressed_data, metadata):
        if not compressed_data:
            return b''
        
        decompressed = bytearray()
        i = 0
        
        while i < len(compressed_data):
            if (compressed_data[i] == 255 and 
                i + 2 < len(compressed_data)):
                # RLE sequence
                count = compressed_data[i + 1]
                byte_value = compressed_data[i + 2]
                decompressed.extend([byte_value] * count)
                i += 3
            else:
                # Regular byte
                decompressed.append(compressed_data[i])
                i += 1
        
        return bytes(decompressed)

# ===============================
# DEFLATE COMPRESSION (USING GZIP)
# ===============================

class DeflateCompression:
    def compress(self, data):
        if not data:
            return b'', {'original_length': 0}
        
        # Use gzip compression (which uses deflate algorithm)
        compressed_data = gzip.compress(data, compresslevel=9)
        
        metadata = {
            'original_length': len(data),
            'algorithm': 'gzip'
        }
        
        return compressed_data, metadata
    
    def decompress(self, compressed_data, metadata):
        if not compressed_data:
            return b''
        
        try:
            decompressed_data = gzip.decompress(compressed_data)
            return decompressed_data
        except Exception as e:
            raise ValueError(f"Decompression failed: {str(e)}")

# ===============================
# COMPRESSION MANAGER
# ===============================

import filetype
import os

class CompressionManager:
    def __init__(self):
        self.algorithms = {
            'huffman': HuffmanCoding(),
            'lz77': LZ77(),
            'rle': RunLengthEncoding(),
            'deflate': DeflateCompression()
        }

    def detect_algorithm(self, file_data, filename):
        kind = filetype.guess(file_data)
        mime = kind.mime if kind else 'application/octet-stream'
        ext = os.path.splitext(filename)[1].lower()

        if ext in ['.txt', '.csv', '.json', '.xml', '.html'] or mime.startswith("text"):
            return 'huffman'
        elif ext in ['.bmp', '.pbm', '.pgm', '.ppm']:
            return 'rle'
        elif ext in ['.bin', '.exe']:
            return 'lz77'
        else:
            return 'deflate'  # Fallback

    def compress_file(self, file_data, filename, requested_algo):
        algorithm = requested_algo if requested_algo != 'auto' else self.detect_algorithm(file_data, filename)

        if algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        start_time = time.time()

        # Use standard Python libraries
        if algorithm == 'huffman':
            compressed_data = zlib.compress(file_data)
        elif algorithm == 'lz77':
            compressed_data = bz2.compress(file_data)
        elif algorithm == 'rle':
            compressed_data = lzma.compress(file_data)
        elif algorithm == 'deflate':
            compressed_data = gzip.compress(file_data)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        processing_time = round(time.time() - start_time, 3)
        original_size = len(file_data)
        compressed_size = len(compressed_data)
        compression_ratio = round(((original_size - compressed_size) / original_size) * 100, 2) if original_size else 0

        metadata = {
            'original_length': original_size
        }

        return {
            'compressed_data': compressed_data,
            'metadata': metadata,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'processing_time': processing_time,
            'algorithm': algorithm
        }


    def decompress_file(self, compressed_data, metadata, algorithm):
        if algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        start_time = time.time()

        # Use standard Python libraries
        if algorithm == 'huffman':
            decompressed_data = zlib.decompress(compressed_data)
        elif algorithm == 'lz77':
            decompressed_data = bz2.decompress(compressed_data)
        elif algorithm == 'rle':
            decompressed_data = lzma.decompress(compressed_data)
        elif algorithm == 'deflate':
            decompressed_data = gzip.decompress(compressed_data)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        processing_time = round(time.time() - start_time, 3)

        return {
            'decompressed_data': decompressed_data,
            'processing_time': processing_time
        }



compression_manager = CompressionManager()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/algorithms', methods=['GET'])
def get_algorithms():
    algorithms = {
        'auto': {
            'name': 'Auto Detect',
            'description': 'Automatically chooses the best algorithm based on file type',
            'best_for': 'All file types'
        },
        'huffman': {
            'name': 'Huffman Coding',
            'description': 'Variable-length prefix coding based on character frequency',
            'best_for': 'Text files, HTML/XML files with repeated characters'
        },
        'lz77': {
            'name': 'LZ77',
            'description': 'Dictionary-based compression using sliding window',
            'best_for': 'Binary files, executables, repetitive content'
        },
        'rle': {
            'name': 'Run-Length Encoding',
            'description': 'Replaces runs of identical data with count and value',
            'best_for': 'Images with large solid areas (bitmap, etc.)'
        },
        'deflate': {
            'name': 'Deflate (GZIP)',
            'description': 'Combines LZ77 and Huffman coding',
            'best_for': 'General-purpose compression'
        }
    }
    return jsonify(algorithms)

@app.route('/process', methods=['POST'])
def process_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        algorithm = request.form.get('algorithm', 'auto')  # Now supports 'auto'
        operation = request.form.get('operation', 'compress')

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        file_data = file.read()
        original_filename = file.filename

        if operation == 'compress':
            result = compression_manager.compress_file(file_data, original_filename, algorithm)

            compressed_package = {
                'compressed_data': base64.b64encode(result['compressed_data']).decode('utf-8'),
                'metadata': result['metadata'],
                'algorithm': result['algorithm'],
                'original_filename': original_filename,
                'original_size': result['original_size']
            }

            package_json = json.dumps(compressed_package, separators=(',', ':'))
            package_bytes = package_json.encode('utf-8')

            name, _ = os.path.splitext(original_filename)
            compressed_filename = f"{name}_{result['algorithm']}.compressed"

            return jsonify({
                'success': True,
                'operation': 'compress',
                'algorithm': result['algorithm'],
                'original_size': result['original_size'],
                'processed_size': len(package_bytes),
                'compression_ratio': result['compression_ratio'],
                'processing_time': result['processing_time'],
                'filename': compressed_filename,
                'file_data': list(package_bytes)
            })

        elif operation == 'decompress':
            try:
                package_json = file_data.decode('utf-8')
                compressed_package = json.loads(package_json)
                compressed_data = base64.b64decode(compressed_package['compressed_data'])
                metadata = compressed_package['metadata']
                algorithm = compressed_package['algorithm']
                original_filename = compressed_package['original_filename']
            except Exception as e:
                return jsonify({'error': f'Invalid compressed file format: {str(e)}'}), 400

            result = compression_manager.decompress_file(compressed_data, metadata, algorithm)

            return jsonify({
                'success': True,
                'operation': 'decompress',
                'algorithm': algorithm,
                'original_size': len(compressed_data),
                'processed_size': len(result['decompressed_data']),
                'processing_time': result['processing_time'],
                'filename': original_filename,
                'file_data': list(result['decompressed_data'])
            })

        else:
            return jsonify({'error': 'Invalid operation. Use "compress" or "decompress"'}), 400

    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'algorithms': list(compression_manager.algorithms.keys()),
        'version': '3.0.0'
    })

if __name__ == '__main__':
    print("🗜️ Starting Data Compression Portal Server with Auto Detection...")
    app.run(debug=True, port=5000)
