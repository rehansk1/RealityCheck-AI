import React, { useEffect, useState } from "react";
import "./Navbar.css";

function Navbar({ onLogin }) {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);

    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  return (
    <header className={`navbar ${scrolled ? "navbar-scrolled" : ""}`}>
      <div className="navbar-container">

        {/* LOGO */}
        <button
          className="navbar-logo"
          onClick={() => scrollToSection("home")}
        >
          <span className="logo-mark">✓</span>

          <span className="logo-text">
            RealityCheck
            <span>AI</span>
          </span>
        </button>

        {/* NAVIGATION */}
        <nav className="navbar-links">

          <button
            className="nav-link"
            onClick={() => scrollToSection("home")}
          >
            <span>Home</span>
          </button>

          <button
            className="nav-link"
            onClick={() => scrollToSection("analyze")}
          >
            <span>Analyze</span>
          </button>

          <button
            className="nav-link"
            onClick={() => scrollToSection("features")}
          >
            <span>Features</span>
          </button>

        </nav>

        {/* ACTIONS */}
        <div className="navbar-actions">

          <button
            className="login-button"
            onClick={onLogin}
          >
            <span>Login</span>
          </button>

          <button
            className="get-started-button"
            onClick={() => scrollToSection("analyze")}
          >
            <span>Get Started</span>
            <span className="arrow">→</span>
          </button>

        </div>

      </div>
    </header>
  );
}

export default Navbar;