const API_URL = "http://127.0.0.1:8000/api";

// =====================================================
// ANALYZE NEWS TEXT
// =====================================================

export async function analyzeText(text) {
  const response = await fetch(`${API_URL}/analyze-text`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.message ||
      "News analysis failed."
    );
  }

  return data;
}


// =====================================================
// VERIFY NEWS
// =====================================================

export async function verifyNews(text) {
  const response = await fetch(`${API_URL}/verify-news`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.message ||
      "News verification failed."
    );
  }

  return data;
}


// =====================================================
// UPLOAD FILE
// =====================================================

export async function uploadFile(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.message ||
      "File upload failed."
    );
  }

  return data;
}


// =====================================================
// IMAGE DETECTION
// =====================================================

export async function detectImage(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_URL}/detect-image`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.message ||
      "Image detection failed."
    );
  }

  return data;
}


// =====================================================
// ANALYZE URL
// =====================================================

export async function analyzeUrl(url) {
  const response = await fetch(`${API_URL}/analyze-url`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.message ||
      "URL analysis failed."
    );
  }

  return data;
}


// =====================================================
// BACKWARD COMPATIBILITY
// =====================================================

export const uploadArticle = uploadFile;