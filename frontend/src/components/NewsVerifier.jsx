import React, { useRef, useState } from "react";
import "./NewsVerifier.css";

const API_URL = "http://127.0.0.1:8000/api";

export default function NewsVerifier() {
  const fileInputRef = useRef(null);

  const [activeTab, setActiveTab] = useState("upload");
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const [url, setUrl] = useState("");
  const [articleText, setArticleText] = useState("");

  const [loading, setLoading] = useState(false);
  const [dragging, setDragging] = useState(false);

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // =========================================================
  // FILE SETTINGS
  // =========================================================

  const allowedExtensions = [
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".pdf",
    ".docx",
    ".txt",
  ];

  const maxSize = 20 * 1024 * 1024;

  // =========================================================
  // EXTENSION
  // =========================================================

  const getExtension = (filename) => {
    if (!filename) return "";

    const parts = filename.toLowerCase().split(".");

    if (parts.length < 2) return "";

    return "." + parts.pop();
  };

  // =========================================================
  // IMAGE CHECK
  // =========================================================

  const isImageFile = (file) => {
    if (!file) return false;

    return [
      ".jpg",
      ".jpeg",
      ".png",
      ".webp",
    ].includes(getExtension(file.name));
  };

  // =========================================================
  // DOCUMENT CHECK
  // =========================================================

  const isDocumentFile = (file) => {
    if (!file) return false;

    return [
      ".pdf",
      ".docx",
      ".txt",
    ].includes(getExtension(file.name));
  };

  // =========================================================
  // FILE HANDLER
  // =========================================================

  const handleFile = (file) => {
    if (!file) return;

    setError("");
    setResult(null);

    const extension = getExtension(file.name);

    if (!allowedExtensions.includes(extension)) {
      setError(
        "Unsupported file type. Please upload JPG, JPEG, PNG, WEBP, PDF, DOCX or TXT."
      );
      return;
    }

    if (file.size > maxSize) {
      setError(
        "File is too large. Maximum file size is 20 MB."
      );
      return;
    }

    setSelectedFile(file);

    if (isImageFile(file)) {
      const imageURL = URL.createObjectURL(file);
      setPreview(imageURL);
    } else {
      setPreview(null);
    }
  };

  // =========================================================
  // FILE INPUT
  // =========================================================

  const handleInputChange = (event) => {
    const file = event.target.files?.[0];

    if (file) {
      handleFile(file);
    }
  };

  // =========================================================
  // DRAG & DROP
  // =========================================================

  const handleDrop = (event) => {
    event.preventDefault();

    setDragging(false);

    const file = event.dataTransfer.files?.[0];

    if (file) {
      handleFile(file);
    }
  };

  // =========================================================
  // OPEN FILE PICKER
  // =========================================================

  const openFilePicker = () => {
    fileInputRef.current?.click();
  };

  // =========================================================
  // REMOVE FILE
  // =========================================================

  const removeFile = () => {
    if (preview) {
      URL.revokeObjectURL(preview);
    }

    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // =========================================================
  // CHANGE TAB
  // =========================================================

  const changeTab = (tab) => {
    setActiveTab(tab);

    setError("");
    setResult(null);
  };

  // =========================================================
  // ANALYZE FILE
  // =========================================================

  const analyzeFile = async () => {
    if (!selectedFile) {
      setError(
        "Please select an image or document first."
      );
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();

      formData.append(
        "file",
        selectedFile
      );

      let endpoint = "";

      if (isImageFile(selectedFile)) {
        endpoint = `${API_URL}/detect-image`;
      } else if (isDocumentFile(selectedFile)) {
        endpoint = `${API_URL}/upload`;
      } else {
        throw new Error(
          "Unsupported file type."
        );
      }

      console.log(
        "Sending file to:",
        endpoint
      );

      const response = await fetch(
        endpoint,
        {
          method: "POST",
          body: formData,
        }
      );

      let data;

      try {
        data = await response.json();
      } catch {
        throw new Error(
          "The server returned an invalid response."
        );
      }

      if (!response.ok) {
        throw new Error(
          data?.detail ||
          data?.message ||
          "File analysis failed."
        );
      }

      console.log(
        "FILE ANALYSIS RESULT:",
        data
      );

      setResult(data);

    } catch (err) {
      console.error(
        "FILE ANALYSIS ERROR:",
        err
      );

      setError(
        err.message ||
        "Unable to connect to the RealityCheck AI server."
      );

    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // ANALYZE URL
  // =========================================================

  const analyzeURL = async () => {
    if (!url.trim()) {
      setError(
        "Please enter a news article URL."
      );
      return;
    }

    if (
      !url.startsWith("http://") &&
      !url.startsWith("https://")
    ) {
      setError(
        "Please enter a valid HTTP or HTTPS URL."
      );
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `${API_URL}/analyze-url`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            url: url.trim(),
          }),
        }
      );

      let data;

      try {
        data = await response.json();
      } catch {
        throw new Error(
          "The server returned an invalid response."
        );
      }

      if (!response.ok) {
        throw new Error(
          data?.detail ||
          "URL analysis failed."
        );
      }

      setResult(data);

    } catch (err) {
      console.error(
        "URL ANALYSIS ERROR:",
        err
      );

      setError(
        err.message ||
        "Unable to analyze this article URL."
      );

    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // ANALYZE ARTICLE
  // =========================================================

  const analyzeArticle = async () => {
    if (!articleText.trim()) {
      setError(
        "Please paste a news article or claim."
      );
      return;
    }

    if (articleText.trim().length < 20) {
      setError(
        "Please enter more information about the news claim."
      );
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `${API_URL}/verify-news`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            text: articleText.trim(),
          }),
        }
      );

      let data;

      try {
        data = await response.json();
      } catch {
        throw new Error(
          "The server returned an invalid response."
        );
      }

      if (!response.ok) {
        throw new Error(
          data?.detail ||
          "Article verification failed."
        );
      }

      setResult(data);

    } catch (err) {
      console.error(
        "ARTICLE ANALYSIS ERROR:",
        err
      );

      setError(
        err.message ||
        "Unable to verify this news article."
      );

    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // RESULT HELPERS
  // =========================================================

  const getVerdict = () => {
    if (!result) {
      return "UNCERTAIN";
    }

    return (
      result.verdict ||
      result.prediction ||
      "UNCERTAIN"
    )
      .toString()
      .toUpperCase();
  };

  const verdict = getVerdict();

  const confidence = Math.min(
    100,
    Math.max(
      0,
      Number(result?.confidence || 0)
    )
  );

  const getVerdictClass = () => {
    if (verdict === "REAL") {
      return "real";
    }

    if (verdict === "FAKE") {
      return "fake";
    }

    return "uncertain";
  };

  const getVerdictIcon = () => {
    if (verdict === "REAL") {
      return "✓";
    }

    if (verdict === "FAKE") {
      return "×";
    }

    return "?";
  };

  // =========================================================
  // GET REASONS
  // =========================================================

  const getReasons = () => {
    if (!result) {
      return [];
    }

    if (
      Array.isArray(result.explanation) &&
      result.explanation.length > 0
    ) {
      return result.explanation.filter(
        (item) =>
          item &&
          typeof item === "string"
      );
    }

    if (
      Array.isArray(result.reasons) &&
      result.reasons.length > 0
    ) {
      return result.reasons.filter(
        (item) =>
          item &&
          typeof item === "string"
      );
    }

    if (result.reason) {
      return [
        result.reason
      ];
    }

    return [
      "The available evidence was analyzed by RealityCheck AI."
    ];
  };

  const reasons = getReasons();

  // =========================================================
  // GET SOURCES
  // =========================================================

  const getSources = () => {
    if (!result) {
      return [];
    }

    if (
      Array.isArray(result.source_details) &&
      result.source_details.length > 0
    ) {
      return result.source_details
        .filter(
          (source) =>
            source &&
            typeof source.url === "string" &&
            source.url.startsWith("http")
        )
        .slice(0, 8);
    }

    if (
      Array.isArray(result.sources) &&
      result.sources.length > 0
    ) {
      return result.sources
        .filter(
          (source) =>
            typeof source === "string" &&
            source.startsWith("http")
        )
        .slice(0, 8)
        .map((source) => ({
          url: source,
          title: "Reliable Source",
          domain: getDomain(source),
        }));
    }

    return [];
  };

  const sources = getSources();

  // =========================================================
  // DOMAIN
  // =========================================================

  const getDomain = (sourceUrl) => {
    try {
      return new URL(sourceUrl).hostname
        .replace("www.", "");
    } catch {
      return sourceUrl;
    }
  };

  // =========================================================
  // SOURCE TITLE
  // =========================================================

  const getSourceTitle = (source) => {
    if (source.title) {
      return source.title;
    }

    const domain =
      source.domain ||
      getDomain(source.url);

    if (
      domain.includes("reuters.com")
    ) {
      return "Reuters";
    }

    if (
      domain.includes("apnews.com")
    ) {
      return "Associated Press";
    }

    if (
      domain.includes("thehindu.com")
    ) {
      return "The Hindu";
    }

    if (
      domain.includes("indianexpress.com")
    ) {
      return "Indian Express";
    }

    if (
      domain.includes("pib.gov.in")
    ) {
      return "Official Government Source";
    }

    if (
      domain.endsWith(".gov.in")
    ) {
      return "Official Government Source";
    }

    return domain;
  };

  // =========================================================
  // FILE ICON
  // =========================================================

  const getFileIcon = () => {
    if (!selectedFile) {
      return "↑";
    }

    const extension =
      getExtension(
        selectedFile.name
      );

    if (
      [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
      ].includes(extension)
    ) {
      return "◉";
    }

    if (extension === ".pdf") {
      return "PDF";
    }

    if (extension === ".docx") {
      return "DOC";
    }

    if (extension === ".txt") {
      return "TXT";
    }

    return "FILE";
  };

  // =========================================================
  // RENDER
  // =========================================================

  return (
    <section
      className="news-verifier-section"
      id="analyze"
    >

      <div className="verification-container">

        {/* =================================================
            HEADER
        ================================================= */}

        <div className="verification-header">

          <div className="verification-badge">
            <span className="badge-dot"></span>
            AI VERIFICATION CENTER
          </div>

          <h2>
            Verify Before{" "}
            <span>You Believe.</span>
          </h2>

          <p>
            Analyze images, documents, articles and
            online news using AI-powered verification.
          </p>

        </div>


        {/* =================================================
            MAIN CARD
        ================================================= */}

        <div className="verification-card">

          {/* =================================================
              TABS
          ================================================= */}

          <div className="verification-tabs">

            <button
              className={`verification-tab ${
                activeTab === "upload"
                  ? "active"
                  : ""
              }`}
              onClick={() =>
                changeTab("upload")
              }
            >
              <span className="tab-icon">
                ↑
              </span>

              <span>
                <strong>Upload</strong>
                <small>
                  Image or document
                </small>
              </span>
            </button>


            <button
              className={`verification-tab ${
                activeTab === "url"
                  ? "active"
                  : ""
              }`}
              onClick={() =>
                changeTab("url")
              }
            >
              <span className="tab-icon">
                ↗
              </span>

              <span>
                <strong>URL</strong>
                <small>
                  Online article
                </small>
              </span>
            </button>


            <button
              className={`verification-tab ${
                activeTab === "article"
                  ? "active"
                  : ""
              }`}
              onClick={() =>
                changeTab("article")
              }
            >
              <span className="tab-icon">
                ▤
              </span>

              <span>
                <strong>Article</strong>
                <small>
                  News claim
                </small>
              </span>
            </button>

          </div>


          {/* =================================================
              UPLOAD
          ================================================= */}

          {activeTab === "upload" && (

            <div className="verification-content">

              <div className="content-heading">

                <div>

                  <div className="mini-label">
                    FILE VERIFICATION
                  </div>

                  <h3>
                    Upload & Verify
                  </h3>

                  <p>
                    Upload an image or document for
                    RealityCheck AI verification.
                  </p>

                </div>

              </div>


              {/* FILE TYPES */}

              <div className="file-types">

                <div className="file-type">

                  <div className="file-type-icon image-icon">
                    ◉
                  </div>

                  <div>

                    <strong>
                      Images
                    </strong>

                    <span>
                      JPG · JPEG · PNG · WEBP
                    </span>

                  </div>

                </div>


                <div className="file-type">

                  <div className="file-type-icon document-icon">
                    ▤
                  </div>

                  <div>

                    <strong>
                      Documents
                    </strong>

                    <span>
                      PDF · DOCX · TXT
                    </span>

                  </div>

                </div>

              </div>


              {/* DROP ZONE */}

              <div
                className={`drop-zone ${
                  dragging
                    ? "dragging"
                    : ""
                } ${
                  selectedFile
                    ? "has-file"
                    : ""
                }`}

                onDragOver={(event) => {
                  event.preventDefault();
                  setDragging(true);
                }}

                onDragLeave={() => {
                  setDragging(false);
                }}

                onDrop={handleDrop}

                onClick={
                  selectedFile
                    ? undefined
                    : openFilePicker
                }
              >

                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".jpg,.jpeg,.png,.webp,.pdf,.docx,.txt"
                  onChange={handleInputChange}
                  hidden
                />


                {!selectedFile ? (

                  <>

                    <div className="upload-orbit">

                      <div className="upload-icon">
                        ↑
                      </div>

                    </div>

                    <h4>
                      Drag & Drop your file
                    </h4>

                    <p>
                      or{" "}
                      <button
                        type="button"
                        onClick={(event) => {
                          event.stopPropagation();
                          openFilePicker();
                        }}
                      >
                        click to browse
                      </button>{" "}
                      your computer
                    </p>

                    <div className="format-list">
                      <span>JPG</span>
                      <span>JPEG</span>
                      <span>PNG</span>
                      <span>WEBP</span>
                      <span>PDF</span>
                      <span>DOCX</span>
                      <span>TXT</span>
                    </div>

                    <small className="file-limit">
                      Maximum 20 MB
                    </small>

                  </>

                ) : (

                  <div className="selected-file">

                    {preview ? (

                      <img
                        src={preview}
                        alt="Preview"
                        className="image-preview"
                      />

                    ) : (

                      <div className="document-preview">
                        {getFileIcon()}
                      </div>

                    )}


                    <div className="selected-file-info">

                      <strong>
                        {selectedFile.name}
                      </strong>

                      <span>
                        {(
                          selectedFile.size /
                          1024 /
                          1024
                        ).toFixed(2)}{" "}
                        MB
                      </span>

                      <small>
                        Ready for AI verification
                      </small>

                    </div>


                    <button
                      type="button"
                      className="remove-file"
                      onClick={(event) => {
                        event.stopPropagation();
                        removeFile();
                      }}
                    >
                      ×
                    </button>

                  </div>

                )}

              </div>


              {/* ANALYZE */}

              <button
                className="analyze-button"
                onClick={analyzeFile}
                disabled={
                  loading ||
                  !selectedFile
                }
              >

                {loading ? (

                  <>
                    <span className="spinner"></span>
                    Analyzing...
                  </>

                ) : (

                  <>
                    <span>⌕</span>
                    Analyze File
                  </>

                )}

              </button>


              <div className="security-note">
                <span>🔒</span>
                Your uploaded file is processed securely.
              </div>

            </div>

          )}


          {/* =================================================
              URL
          ================================================= */}

          {activeTab === "url" && (

            <div className="verification-content">

              <div className="content-heading">

                <div>

                  <div className="mini-label">
                    ARTICLE VERIFICATION
                  </div>

                  <h3>
                    Analyze News URL
                  </h3>

                  <p>
                    Enter an online article URL and
                    RealityCheck AI will analyze its claims.
                  </p>

                </div>

              </div>


              <div className="url-input-wrapper">

                <span className="input-icon">
                  ↗
                </span>

                <input
                  type="url"
                  value={url}
                  onChange={(event) =>
                    setUrl(
                      event.target.value
                    )
                  }
                  placeholder="https://example.com/news-article"
                  onKeyDown={(event) => {
                    if (
                      event.key === "Enter"
                    ) {
                      analyzeURL();
                    }
                  }}
                />

              </div>


              <div className="input-help">
                Paste the URL of a news article
                to analyze its content.
              </div>


              <button
                className="analyze-button"
                onClick={analyzeURL}
                disabled={
                  loading ||
                  !url.trim()
                }
              >

                {loading ? (

                  <>
                    <span className="spinner"></span>
                    Analyzing Article...
                  </>

                ) : (

                  <>
                    <span>⌕</span>
                    Analyze URL
                  </>

                )}

              </button>

            </div>

          )}


          {/* =================================================
              ARTICLE
          ================================================= */}

          {activeTab === "article" && (

            <div className="verification-content">

              <div className="content-heading">

                <div>

                  <div className="mini-label">
                    TEXT VERIFICATION
                  </div>

                  <h3>
                    Verify News Claim
                  </h3>

                  <p>
                    Paste a news article or claim and
                    let AI check the available evidence.
                  </p>

                </div>

              </div>


              <textarea
                className="article-textarea"
                value={articleText}
                onChange={(event) =>
                  setArticleText(
                    event.target.value
                  )
                }
                placeholder="Paste the news article or claim here..."
              />


              <div className="textarea-footer">

                <span>
                  {articleText.length} characters
                </span>

                <span>
                  AI-powered verification
                </span>

              </div>


              <button
                className="analyze-button"
                onClick={analyzeArticle}
                disabled={
                  loading ||
                  !articleText.trim()
                }
              >

                {loading ? (

                  <>
                    <span className="spinner"></span>
                    Verifying...
                  </>

                ) : (

                  <>
                    <span>⌕</span>
                    Verify Article
                  </>

                )}

              </button>

            </div>

          )}


          {/* =================================================
              ERROR
          ================================================= */}

          {error && (

            <div className="error-message">

              <span>!</span>

              <div>

                <strong>
                  Verification failed
                </strong>

                <p>
                  {error}
                </p>

              </div>

            </div>

          )}


          {/* =================================================
              NEW RESULT DESIGN
          ================================================= */}

          {result && !loading && (

            <div className="result-section">

              <div className="result-divider"></div>


              {/* RESULT HEADER */}

              <div className="result-header">

                <div>

                  <div className="mini-label">
                    VERIFICATION RESULT
                  </div>

                  <h3>
                    AI Analysis
                  </h3>

                </div>

              </div>


              {/* VERDICT */}

              <div
                className={`simple-verdict ${
                  getVerdictClass()
                }`}
              >

                <span className="simple-verdict-icon">
                  {getVerdictIcon()}
                </span>

                <div>

                  <strong>
                    {verdict}
                  </strong>

                  <span>
                    Confidence: {confidence}%
                  </span>

                </div>

              </div>


              {/* CONFIDENCE BAR */}

              <div className="confidence-card">

                <div className="confidence-top">

                  <span>
                    CONFIDENCE
                  </span>

                  <strong>
                    {confidence}%
                  </strong>

                </div>


                <div className="confidence-bar">

                  <div
                    className={`confidence-fill ${
                      getVerdictClass()
                    }`}
                    style={{
                      width: `${confidence}%`,
                    }}
                  ></div>

                </div>

              </div>


              {/* =================================================
                  SUMMARY
              ================================================= */}

              <div className="result-box">

                <div className="result-box-title">

                  <span>
                    ▣
                  </span>

                  Summary

                </div>

                <p>
                  {result.summary ||
                    "No summary available."}
                </p>

              </div>


              {/* =================================================
                  WHY
              ================================================= */}

              <div className="result-box">

                <div className="result-box-title">

                  <span>
                    ?
                  </span>

                  Why?

                </div>


                <div className="reason-list">

                  {reasons.map(
                    (reason, index) => (

                      <div
                        className="reason-item"
                        key={index}
                      >

                        <span>
                          •
                        </span>

                        <p>
                          {reason}
                        </p>

                      </div>

                    )
                  )}

                </div>

              </div>


              {/* =================================================
                  SOURCES
              ================================================= */}

              <div className="sources-box">

                <div className="result-box-title">

                  <span>
                    ↗
                  </span>

                  Sources

                </div>


                <p className="sources-description">

                  Evidence used for this verification.

                </p>


                {sources.length > 0 ? (

                  <div className="sources-list">

                    {sources.map(
                      (source, index) => (

                        <a
                          key={`${source.url}-${index}`}
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="source-item"
                        >

                          <span className="source-number">
                            {index + 1}
                          </span>


                          <div className="source-content">

                            <strong>
                              {getSourceTitle(
                                source
                              )}
                            </strong>

                            <small>
                              {source.url}
                            </small>

                          </div>


                          <span className="source-arrow">
                            ↗
                          </span>

                        </a>

                      )
                    )}

                  </div>

                ) : (

                  <div className="no-sources">

                    No reliable sources were returned.

                  </div>

                )}

              </div>


              {/* =================================================
                  ORIGINAL ARTICLE URL
              ================================================= */}

              {result.url && (

                <div className="original-source-box">

                  <div className="result-box-title">

                    <span>
                      ↗
                    </span>

                    Original Article

                  </div>


                  <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {result.url}
                  </a>

                </div>

              )}

            </div>

          )}

        </div>


        {/* =================================================
            TRUST BAR
        ================================================= */}

        <div className="verification-trust">

          <div className="trust-item">

            <span>✓</span>

            <div>

              <strong>
                AI Powered
              </strong>

              <small>
                Intelligent verification
              </small>

            </div>

          </div>


          <div className="trust-item">

            <span>◈</span>

            <div>

              <strong>
                Evidence Based
              </strong>

              <small>
                Reliable source analysis
              </small>

            </div>

          </div>


          <div className="trust-item">

            <span>🔒</span>

            <div>

              <strong>
                Private
              </strong>

              <small>
                Your content stays secure
              </small>

            </div>

          </div>


          <div className="trust-item">

            <span>⚡</span>

            <div>

              <strong>
                Fast Analysis
              </strong>

              <small>
                Results in seconds
              </small>

            </div>

          </div>

        </div>

      </div>

    </section>
  );
}