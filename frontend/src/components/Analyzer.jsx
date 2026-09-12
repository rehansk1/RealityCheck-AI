import React, { useRef, useState } from "react";
import { detectImage } from "../services/api";

function Analyzer({ result, setResult }) {
  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState("");

  // =====================================================
  // SUPPORTED FILE TYPES
  // =====================================================

  const allowedExtensions = [
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".pdf",
    ".docx",
    ".txt",
  ];

  const imageExtensions = [
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
  ];

  const documentExtensions = [
    ".pdf",
    ".docx",
    ".txt",
  ];

  const MAX_FILE_SIZE = 20 * 1024 * 1024;

  // =====================================================
  // GET EXTENSION
  // =====================================================

  function getExtension(fileName) {
    const name = fileName.toLowerCase();

    const lastDot = name.lastIndexOf(".");

    if (lastDot === -1) {
      return "";
    }

    return name.substring(lastDot);
  }

  // =====================================================
  // FILE TYPE CHECK
  // =====================================================

  function isAllowedFile(selectedFile) {
    if (!selectedFile) {
      return false;
    }

    const extension = getExtension(
      selectedFile.name
    );

    return allowedExtensions.includes(extension);
  }

  function isImageFile(selectedFile) {
    if (!selectedFile) {
      return false;
    }

    const extension = getExtension(
      selectedFile.name
    );

    return imageExtensions.includes(extension);
  }

  function isDocumentFile(selectedFile) {
    if (!selectedFile) {
      return false;
    }

    const extension = getExtension(
      selectedFile.name
    );

    return documentExtensions.includes(extension);
  }

  // =====================================================
  // FILE TYPE NAME
  // =====================================================

  function getFileType(selectedFile) {
    if (!selectedFile) {
      return "FILE";
    }

    const extension = getExtension(
      selectedFile.name
    );

    switch (extension) {
      case ".jpg":
      case ".jpeg":
        return "JPG IMAGE";

      case ".png":
        return "PNG IMAGE";

      case ".webp":
        return "WEBP IMAGE";

      case ".pdf":
        return "PDF DOCUMENT";

      case ".docx":
        return "WORD DOCUMENT";

      case ".txt":
        return "TEXT DOCUMENT";

      default:
        return "FILE";
    }
  }

  // =====================================================
  // SELECT FILE
  // =====================================================

  function handleFileSelect(selectedFile) {
    if (!selectedFile) {
      return;
    }

    setError("");
    setResult(null);

    // ---------------------------------------------------
    // FILE TYPE
    // ---------------------------------------------------

    if (!isAllowedFile(selectedFile)) {
      setError(
        "Unsupported file type. Please upload JPG, JPEG, PNG, WEBP, PDF, DOCX or TXT."
      );

      return;
    }

    // ---------------------------------------------------
    // FILE SIZE
    // ---------------------------------------------------

    if (selectedFile.size > MAX_FILE_SIZE) {
      setError(
        "File is too large. Maximum file size is 20 MB."
      );

      return;
    }

    // ---------------------------------------------------
    // SAVE FILE
    // ---------------------------------------------------

    setFile(selectedFile);

    // ---------------------------------------------------
    // IMAGE PREVIEW
    // ---------------------------------------------------

    if (isImageFile(selectedFile)) {
      const previewUrl =
        URL.createObjectURL(selectedFile);

      setPreview(previewUrl);
    } else {
      setPreview(null);
    }
  }

  // =====================================================
  // FILE INPUT
  // =====================================================

  function handleFileChange(event) {
    const selectedFile =
      event.target.files?.[0];

    handleFileSelect(selectedFile);
  }

  // =====================================================
  // DRAG OVER
  // =====================================================

  function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();

    setDragActive(true);
  }

  // =====================================================
  // DRAG LEAVE
  // =====================================================

  function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();

    setDragActive(false);
  }

  // =====================================================
  // DROP
  // =====================================================

  function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();

    setDragActive(false);

    const droppedFile =
      event.dataTransfer.files?.[0];

    handleFileSelect(droppedFile);
  }

  // =====================================================
  // ANALYZE FILE
  // =====================================================

  async function analyzeFile() {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    // ---------------------------------------------------
    // DOCUMENT
    // ---------------------------------------------------

    if (isDocumentFile(file)) {
      setError(
        "Document selected successfully. PDF, DOCX and TXT require the document verification API."
      );

      return;
    }

    // ---------------------------------------------------
    // IMAGE
    // ---------------------------------------------------

    if (!isImageFile(file)) {
      setError(
        "This file cannot be analyzed."
      );

      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await detectImage(file);

      setResult(data);

    } catch (err) {
      setError(
        err?.message ||
        "Unable to analyze the image. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  // =====================================================
  // RESET
  // =====================================================

  function resetFile() {
    if (preview) {
      URL.revokeObjectURL(preview);
    }

    setFile(null);
    setPreview(null);
    setResult(null);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  // =====================================================
  // RESULT
  // =====================================================

  const prediction = String(
    result?.prediction ||
    result?.result?.prediction ||
    "UNCERTAIN"
  ).toUpperCase();

  const confidence = Math.max(
    0,
    Math.min(
      100,
      Number(
        result?.confidence ??
        result?.result?.confidence ??
        0
      )
    )
  );

  const isFake =
    prediction === "FAKE" ||
    prediction === "AI" ||
    prediction === "AI-GENERATED";

  const isReal =
    prediction === "REAL";

  // =====================================================
  // RENDER
  // =====================================================

  return (
    <div className="upload-area">

      {/* =================================================
          FILE INPUT
      ================================================= */}

      <input
        ref={fileInputRef}
        type="file"
        accept=".jpg,.jpeg,.png,.webp,.pdf,.docx,.txt"
        onChange={handleFileChange}
        hidden
      />

      {/* =================================================
          DROP AREA
      ================================================= */}

      {!file && (
        <div
          className={`drop-box ${
            dragActive
              ? "drag-active"
              : ""
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() =>
            fileInputRef.current?.click()
          }
        >

          <div className="upload-icon">
            📤
          </div>

          <h3>
            Drag & Drop your file
          </h3>

          <p>
            or click to browse your computer
          </p>

          <div className="supported-files">

            <span>JPG</span>
            <span>PNG</span>
            <span>WEBP</span>
            <span>PDF</span>
            <span>DOCX</span>
            <span>TXT</span>

          </div>

          <small>
            Maximum 20 MB
          </small>

        </div>
      )}

      {/* =================================================
          SELECTED FILE
      ================================================= */}

      {file && (
        <div className="preview-container">

          {/* IMAGE */}

          {preview && (
            <img
              src={preview}
              alt="Selected preview"
              className="preview"
            />
          )}

          {/* DOCUMENT */}

          {!preview && (
            <div className="document-preview">

              <div className="document-icon">
                📄
              </div>

              <strong>
                {getFileType(file)}
              </strong>

              <span>
                Document selected
              </span>

            </div>
          )}

          {/* FILE INFO */}

          <div className="selected-file">

            <span>
              {isImageFile(file)
                ? "🖼️"
                : "📄"}
            </span>

            <div>

              <strong>
                {file.name}
              </strong>

              <small>
                {(
                  file.size /
                  1024 /
                  1024
                ).toFixed(2)}{" "}
                MB
                {" · "}
                {getFileType(file)}
              </small>

            </div>

          </div>

          {/* =================================================
              ANALYZE
          ================================================= */}

          <button
            type="button"
            className="primary-button"
            onClick={analyzeFile}
            disabled={loading}
          >

            {loading ? (
              <>
                <span className="spinner"></span>

                Analyzing...
              </>
            ) : (
              <>
                🔎 Analyze File
              </>
            )}

          </button>

          {/* =================================================
              RESET
          ================================================= */}

          <button
            type="button"
            className="secondary-button"
            onClick={resetFile}
            disabled={loading}
          >
            Choose Another File
          </button>

        </div>
      )}

      {/* =================================================
          ERROR
      ================================================= */}

      {error && (
        <div className="error-message">

          <span>
            ⚠️
          </span>

          <span>
            {error}
          </span>

        </div>
      )}

      {/* =================================================
          RESULT
      ================================================= */}

      {result && (
        <div className="result-card">

          {/* HEADER */}

          <div className="result-top">

            <div
              className={`result-icon ${
                isFake
                  ? "fake-icon"
                  : isReal
                    ? "real-icon"
                    : ""
              }`}
            >

              {isFake
                ? "⚠️"
                : isReal
                  ? "✓"
                  : "?"}

            </div>

            <div>

              <div className="result-label">
                IMAGE VERIFICATION
              </div>

              <h3>
                Analysis Complete
              </h3>

            </div>

          </div>

          {/* PREDICTION */}

          <div className="prediction-area">

            <div className="prediction-title">
              Prediction
            </div>

            <div
              className={`prediction ${
                isFake
                  ? "fake"
                  : isReal
                    ? "real"
                    : ""
              }`}
            >
              {prediction}
            </div>

            <p className="result-description">

              {isFake
                ? "This image appears to be AI-generated."
                : isReal
                  ? "This image appears to be a real image."
                  : "The image could not be confidently classified."}

            </p>

          </div>

          {/* CONFIDENCE */}

          <div className="confidence">

            <div className="confidence-header">

              <span>
                Confidence
              </span>

              <strong>
                {confidence}%
              </strong>

            </div>

            <div className="progress">

              <div
                className="progress-bar"
                style={{
                  width:
                    `${confidence}%`,
                }}
              />

            </div>

          </div>

          {/* FILE */}

          <div className="result-file">

            <span>
              🖼️
            </span>

            <span>
              {file?.name ||
                "Image analyzed"}
            </span>

          </div>

          {/* SUCCESS */}

          <p className="success-message">
            ✓ Image analyzed successfully.
          </p>

          {/* RESET */}

          <button
            type="button"
            className="secondary-button"
            onClick={resetFile}
          >
            Analyze Another File
          </button>

        </div>
      )}

    </div>
  );
}

export default Analyzer;