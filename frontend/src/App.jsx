import { useState } from "react";

import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import NewsVerifier from "./components/NewsVerifier";
import Features from "./components/Features";
import Footer from "./components/Footer";

import Login from "./components/Login";
import Register from "./components/Register";
import ForgotPassword from "./components/ForgotPassword";

import "./App.css";

function App() {
  const [currentPage, setCurrentPage] = useState("home");

  /* =====================================================
     MAIN WEBSITE
     ===================================================== */

  const showHome = () => {
    setCurrentPage("home");

    setTimeout(() => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    }, 50);
  };

  const showAnalyze = () => {
    setCurrentPage("home");

    setTimeout(() => {
      const element = document.getElementById("analyze");

      if (element) {
        element.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    }, 100);
  };

  const showFeatures = () => {
    setCurrentPage("home");

    setTimeout(() => {
      const element = document.getElementById("features");

      if (element) {
        element.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    }, 100);
  };

  /* =====================================================
     AUTHENTICATION
     ===================================================== */

  const openLogin = () => {
    setCurrentPage("login");

    window.scrollTo({
      top: 0,
      behavior: "instant",
    });
  };

  const openRegister = () => {
    setCurrentPage("register");

    window.scrollTo({
      top: 0,
      behavior: "instant",
    });
  };

  const openForgotPassword = () => {
    setCurrentPage("forgot");

    window.scrollTo({
      top: 0,
      behavior: "instant",
    });
  };

  const handleLogin = () => {
    /*
      Frontend demo login.

      Later we can connect this to your FastAPI
      authentication backend.
    */

    alert("Login successful!");

    setCurrentPage("home");

    setTimeout(() => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    }, 50);
  };

  const handleRegister = () => {
    /*
      Frontend demo registration.

      Later we can connect this to your backend
      database and authentication system.
    */

    alert("Account created successfully!");

    setCurrentPage("login");

    window.scrollTo({
      top: 0,
      behavior: "instant",
    });
  };

  const handleResetPassword = () => {
    /*
      Frontend demo password reset.

      Later we can connect this to email/password
      reset functionality in the backend.
    */

    alert("Password reset link has been sent!");

    setCurrentPage("login");

    window.scrollTo({
      top: 0,
      behavior: "instant",
    });
  };

  /* =====================================================
     AUTH PAGES
     ===================================================== */

  if (currentPage === "login") {
    return (
      <main className="auth-page-wrapper">
        <Login
          onLogin={handleLogin}
          onRegister={openRegister}
          onForgotPassword={openForgotPassword}
          onBack={showHome}
        />
      </main>
    );
  }

  if (currentPage === "register") {
    return (
      <main className="auth-page-wrapper">
        <Register
          onRegister={handleRegister}
          onLogin={openLogin}
          onBack={showHome}
        />
      </main>
    );
  }

  if (currentPage === "forgot") {
    return (
      <main className="auth-page-wrapper">
        <ForgotPassword
          onResetPassword={handleResetPassword}
          onLogin={openLogin}
          onBack={showHome}
        />
      </main>
    );
  }

  /* =====================================================
     MAIN WEBSITE
     ===================================================== */

  return (
    <div className="app">
      <div className="main-site">

        {/* ================= NAVBAR ================= */}

        <Navbar
          onHome={showHome}
          onAnalyze={showAnalyze}
          onFeatures={showFeatures}
          onLogin={openLogin}
          onGetStarted={openRegister}
        />

        {/* ================= HERO ================= */}

        <Hero
          onAnalyze={showAnalyze}
          onFeatures={showFeatures}
        />

        {/* ================= ANALYZER ================= */}

        <section id="analyze">
          <NewsVerifier />
        </section>

        {/* ================= FEATURES ================= */}

        <Features />

        {/* ================= FOOTER ================= */}

        <Footer
          onHome={showHome}
          onAnalyze={showAnalyze}
          onFeatures={showFeatures}
          onLogin={openLogin}
        />

      </div>
    </div>
  );
}

export default App;