import React from "react";
import {
  FiShield,
  FiArrowUpRight,
  FiGithub,
  FiMail,
  FiLock,
  FiCheckCircle,
} from "react-icons/fi";

import "./Footer.css";

function Footer() {
  const scrollTo = (id) => {
    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
    });
  };

  const goHome = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <footer className="site-footer">

      {/* ================================================
          FOOTER CTA
      ================================================= */}

      <div className="footer-container">

        <div className="footer-cta">

          <div className="footer-cta-content">

            <div className="footer-cta-badge">
              <span></span>
              AI-POWERED VERIFICATION
            </div>

            <h2>
              Don't just read it.
              <br />
              <span>RealityCheck it.</span>
            </h2>

            <p>
              Verify news, analyze images and check documents
              with intelligent AI-powered verification.
            </p>

          </div>

          <button
            className="footer-cta-button"
            onClick={() => scrollTo("analyze")}
          >
            Start Verification
            <FiArrowUpRight size={17} />
          </button>

        </div>


        {/* ================================================
            MAIN FOOTER
        ================================================= */}

        <div className="footer-main">

          {/* BRAND */}

          <div className="footer-brand">

            <button
              className="footer-logo"
              onClick={goHome}
              aria-label="Go to homepage"
            >
              <span className="footer-logo-icon">
                <FiShield size={21} />
              </span>

              <span className="footer-logo-text">
                RealityCheck
                <strong>AI</strong>
              </span>
            </button>

            <p>
              AI-powered fake news detection and content
              verification platform built to help you
              separate facts from misinformation.
            </p>

            <div className="footer-status">

              <span className="footer-status-dot"></span>

              <span>
                Verification systems operational
              </span>

            </div>

          </div>


          {/* PRODUCT */}

          <div className="footer-column">

            <h3>Product</h3>

            <button onClick={() => scrollTo("analyze")}>
              Image Verification
            </button>

            <button onClick={() => scrollTo("analyze")}>
              News Verification
            </button>

            <button onClick={() => scrollTo("analyze")}>
              Document Analysis
            </button>

            <button onClick={() => scrollTo("features")}>
              Features
            </button>

          </div>


          {/* COMPANY */}

          <div className="footer-column">

            <h3>Explore</h3>

            <button onClick={goHome}>
              Home
            </button>

            <button onClick={() => scrollTo("analyze")}>
              Analyze
            </button>

            <button onClick={() => scrollTo("features")}>
              Why RealityCheck
            </button>

            <button onClick={goHome}>
              About
            </button>

          </div>


          {/* TRUST */}

          <div className="footer-column">

            <h3>Trust & Security</h3>

            <div className="footer-info-item">
              <FiLock />
              <span>
                Secure processing
              </span>
            </div>

            <div className="footer-info-item">
              <FiCheckCircle />
              <span>
                Evidence-based analysis
              </span>
            </div>

            <div className="footer-info-item">
              <FiShield />
              <span>
                Privacy focused
              </span>
            </div>

            <div className="footer-info-item">
              <FiMail />
              <span>
                AI-assisted verification
              </span>
            </div>

          </div>

        </div>


        {/* ================================================
            FOOTER BOTTOM
        ================================================= */}

        <div className="footer-bottom">

          <div className="footer-copyright">

            <span>
              © 2026 RealityCheck AI.
            </span>

            <span>
              All rights reserved.
            </span>

          </div>


          <div className="footer-links">

            <button>
              Privacy
            </button>

            <span>•</span>

            <button>
              Terms
            </button>

            <span>•</span>

            <button>
              Security
            </button>

          </div>


          <div className="footer-socials">

            <a
              href="mailto:contact@realitycheck.ai"
              aria-label="Email RealityCheck AI"
            >
              <FiMail size={15} />
            </a>

            <a
              href="https://github.com/"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="RealityCheck AI GitHub"
            >
              <FiGithub size={15} />
            </a>

          </div>

        </div>

      </div>

    </footer>
  );
}

export default Footer;