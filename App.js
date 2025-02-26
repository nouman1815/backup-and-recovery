import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [files, setFiles] = useState([]);

  // Fetch List of Files
  const fetchFiles = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/files");
      setFiles(response.data.files);
    } catch (error) {
      console.error("Error fetching files:", error);
    }
  };

  // Upload File
  const uploadFile = async () => {
    if (!selectedFile) {
      alert("Please select a file to upload!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      await axios.post("http://127.0.0.1:5000/upload", formData);
      alert("File uploaded successfully!");
      fetchFiles();
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  // Download File
  const downloadFile = async (filename) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/download/${filename}`,
        { responseType: "blob" }
      );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error("Error downloading file:", error);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  return (
    <div className="container">
      <h2>IBM Cloud Backup System</h2>
      <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} />
      <button onClick={uploadFile}>Upload File</button>
      <h3>Stored Files</h3>
      <ul>
        {files.length > 0 ? (
          files.map((file, index) => (
            <li key={index}>
              {file}{" "}
              <button onClick={() => downloadFile(file)}>Download</button>
            </li>
          ))
        ) : (
          <p>No files stored yet.</p>
        )}
      </ul>
    </div>
  );
}

export default App;
