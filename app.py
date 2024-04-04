from flask import Flask, jsonify, render_template
import re
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/list-files')
def list_files():
    output_folder = './outputs'  # Adjust this path to your output folder
    try:
        files = os.listdir(output_folder)
        files = [file for file in files if file.endswith('.txt')]  # Adjust if necessary
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/process-file/<filename>')
def process_file(filename):
    print(f"Processing file: {filename}")
    print(os.getcwd())
    # Replace this path with the actual location of your files
    filepath = f"./outputs/{filename}"
    points = []

    try:
        with open(filepath, 'r') as file:
            if "output.txt" in filename:
                print("output.txt")
            for line in file:
                print(line)
                # Extracting latitude and longitude using regular expression
                match = re.search(r'Latitude: (\d+) Long: (-?\d+)', line)
                if match:
                    if "output.txt" in filename:
                        print(match.groups())
                        
                    lat, lon = match.groups()
                    # Convert to decimal degrees
                    lat = int(lat) / 1e7
                    lon = int(lon) / 1e7
                    points.append([lon, lat])
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

    # Convert points to a linestring GeoJSON object
    geojson = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": points
        },
        "properties": {}
    }

    return jsonify(geojson)

if __name__ == '__main__':
    app.run(debug=True)
