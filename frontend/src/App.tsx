import { useState } from 'react'

interface UploadedData {
  filename: string
}

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [uploadedData, setUploadedData] = useState<UploadedData | null>(null)
  const [result, setResult] = useState<string>("")

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`);
      }

      const data = await response.json();
      console.log("Backend response:", data);

      setUploadedData({ filename: data.filename });
      setResult(
        `Skrá hlaðin upp: ${data.rows} raðir, ${data.columns.length} dálkar`
      );
    } catch (error) {
      console.error("Upload error:", error);
      setResult(`Villa við upphleðslu: ${error}`);
    }
  };

  const handleAnalysis = (type: string) => {
    if (!uploadedData) return;
    setResult(`${type} - Bakendi API kemur bráðlega`);
  };

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "0 auto" }}>
      <h1>Hvað eypi ég?</h1>

      <div style={{ marginBottom: "30px" }}>
        <h2>Hlaða upp xlsx</h2>
        <input
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={handleFileChange}
        />
        <button onClick={handleUpload} disabled={!file}>
          Hlaða upp
        </button>
        {uploadedData && <p>Hlaðið upp: {uploadedData.filename}</p>}
      </div>

      <div>
        <h2>Greining</h2>
        <button
          onClick={() => handleAnalysis("Útgjöld yfirlit")}
          disabled={!uploadedData}
        >
          Útgjöld yfirlit
        </button>
        <button
          onClick={() => handleAnalysis("Top 5 útgjöld")}
          disabled={!uploadedData}
        >
          Top 5 útgjöld
        </button>
        <button
          onClick={() => handleAnalysis("Helstu viðtakendur")}
          disabled={!uploadedData}
        >
          Helstu viðtakendur
        </button>
        <button
          onClick={() => handleAnalysis("Mánaðarleg útgjöld")}
          disabled={!uploadedData}
        >
          Mánaðarleg útgjöld
        </button>
        <button
          onClick={() => handleAnalysis("AI flokkun")}
          disabled={!uploadedData}
        >
          Gemma flokkun
        </button>
        {result && <p>{result}</p>}
      </div>
    </div>
  );
}

export default App

