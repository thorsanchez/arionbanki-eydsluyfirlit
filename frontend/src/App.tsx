import { useState } from "react";
import Chat from "./Chat";
interface UploadedData {
  filename: string;
  rows?: number;
  columns?: string[];
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadedData, setUploadedData] = useState<UploadedData | null>(null);
  const [result, setResult] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
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

  const handleUtgjoldYfirlit = async () => {
    if (!uploadedData) return;

    try {
      //senda get request til bakenda
      const response = await fetch(
        "http://localhost:8000/analysis/utgjold-yfirlit"
      );

      // athuga hvort það tókst
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      // parse-a json response
      const data = await response.json();
      console.log("Útgjöld yfirlit response:", data);

      //Sýna niðurstöðuna
      setResult(`Heildarútgjöld: ${data.formatted}`);
    } catch (error) {
      console.error("Analysis error:", error);
      setResult(`Villa við greiningu: ${error}`);
    }
  };

  const handleTop5Utgjold = async () => {
    if (!uploadedData) return;

    try {
      //senda get request til bakenda
      const response = await fetch(
        "http://localhost:8000/analysis/top5-utgjold"
      );

      // athuga hvort það tókst
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      // parse-a json response
      const data = await response.json();
      console.log("Top 5 útgjöld response:", data);

      //Formata gogn
      const formatted = data
        .map(
          (item: any, index: number) =>
            `${index + 1}. ${item.Explanation}: ${item.Amount.toLocaleString()} kr`
        )
        .join("\n");

      setResult(`Top 5 stærstu útgjöld:\n${formatted}`);
    } catch (error) {
      console.error("Analysis error:", error);
      setResult(`Villa við greiningu: ${error}`);
    }
  };

  const handleTopVidtakendur = async () => {
    if (!uploadedData) return;

    try {
      const response = await fetch(
        "http://localhost:8000/analysis/top-vidtakendur"
      );

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const data = await response.json();
      console.log("Top viðtakendur response:", data);

      const formatted = data
        .map(
          (item: any, index: number) =>
            `${index + 1}. ${item.Explanation}: ${item.Amount.toLocaleString()} kr (${item["Fjöldi færslna"]} færslur)`
        )
        .join("\n");

      setResult(`Helstu viðtakendur:\n${formatted}`);
    } catch (error) {
      console.error("Analysis error:", error);
      setResult(`Villa við greiningu: ${error}`);
    }
  };

  const handleManadarUtgjold = async () => {
    if (!uploadedData) return;

    try {
      const response = await fetch(
        "http://localhost:8000/analysis/manadar-utgjold"
      );

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      const data = await response.json();
      console.log("Mánaðar útgjöld response:", data);

      const formatted = data
        .map(
          (item: any) =>
            `${item["Mánuður"]}: ${item.Amount.toLocaleString()} kr`
        )
        .join("\n");

      setResult(`Mánaðarleg útgjöld:\n${formatted}`);
    } catch (error) {
      console.error("Analysis error:", error);
      setResult(`Villa við greiningu: ${error}`);
    }
  };

  const handleAnalysis = (type: string) => {
    if (!uploadedData) return;
    setResult(`${type} - Bakendi API kemur bráðlega`);
  };

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "0 auto" }}>
      <h1>Hvað eyði ég?</h1>

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
        <button onClick={handleUtgjoldYfirlit} disabled={!uploadedData}>
          Útgjöld yfirlit
        </button>
        <button onClick={handleTop5Utgjold} disabled={!uploadedData}>
          Top 5 útgjöld
        </button>
        <button
          onClick={handleTopVidtakendur}
          disabled={!uploadedData}
        >
          Helstu viðtakendur
        </button>
        <button
          onClick={handleManadarUtgjold}
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
      {/* /birta chat ef hlaðið upp, breytt i boolean */}
      <Chat isEnabled={!!uploadedData}/>
    </div>
  );
}

export default App;