import React from "react";
import {
  FiArrowRight,
  FiShield,
  FiCheckCircle,
  FiZap,
  FiActivity,
} from "react-icons/fi";

import "./Hero.css";

function Hero() {
  const scrollToAnalyzer = () => {
    document
      .getElementById("analyze")
      ?.scrollIntoView({
        behavior: "smooth",
      });
  };

  const scrollToFeatures = () => {
    document
      .getElementById("features")
      ?.scrollIntoView({
        behavior: "smooth",
      });
  };

  return (
    <section className="hero" id="home">

      {/* Background Effects */}

      <div className="hero-glow hero-glow-one"></div>
      <div className="hero-glow hero-glow-two"></div>

      <div className="hero-grid"></div>

      <div className="hero-container">

        {/* LEFT SIDE */}

        <div className="hero-content">

          {/* Badge */}

          <div className="hero-badge">
            <span className="hero-badge-dot"></span>

            <FiShield size={14} />

            AI-POWERED VERIFICATION
          </div>

          {/* Heading */}

          <h1 className="hero-title">
            Detect Fake News
            <br />

            <span className="hero-gradient-text">
              Before You Believe.
            </span>
          </h1>

          {/* Description */}

          <p className="hero-description">
            RealityCheck AI helps you verify images, documents,
            articles and online news using intelligent AI analysis
            and evidence-based verification.
          </p>

          {/* Buttons */}

          <div className="hero-buttons">

            <button
              className="hero-primary-button"
              onClick={scrollToAnalyzer}
            >
              <span>Analyze Now</span>

              <FiArrowRight size={18} />
            </button>

            <button
              className="hero-secondary-button"
              onClick={scrollToFeatures}
            >
              Explore Features
            </button>

          </div>

          {/* Trust Row */}

          <div className="hero-trust-row">

            <div className="hero-trust-item">
              <FiCheckCircle />

              <span>AI Powered</span>
            </div>

            <div className="hero-trust-divider"></div>

            <div className="hero-trust-item">
              <FiShield />

              <span>Evidence Based</span>
            </div>

            <div className="hero-trust-divider"></div>

            <div className="hero-trust-item">
              <FiZap />

              <span>Fast Results</span>
            </div>

          </div>

        </div>


        {/* RIGHT SIDE */}

        <div className="hero-visual">

          {/* Main AI Card */}

          <div className="hero-ai-card">

            {/* Card Header */}

            <div className="hero-card-header">

              <div className="hero-card-brand">

                <div className="hero-card-logo">
                  <FiShield size={20} />
                </div>

                <div>
                  <strong>RealityCheck AI</strong>

                  <span>Verification Engine</span>
                </div>

              </div>

              <div className="hero-live">
                <span></span>
                LIVE
              </div>

            </div>


            {/* Scan Area */}

            <div className="hero-scan-area">

              <div className="scan-corner scan-top-left"></div>
              <div className="scan-corner scan-top-right"></div>
              <div className="scan-corner scan-bottom-left"></div>
              <div className="scan-corner scan-bottom-right"></div>

              <div className="hero-scan-icon">
                <FiActivity size={34} />
              </div>

              <div className="hero-scan-ring ring-one"></div>
              <div className="hero-scan-ring ring-two"></div>

              <div className="hero-scan-line"></div>

              <span className="hero-scan-text">
                AI ANALYZING
              </span>

            </div>


            {/* Analysis Stats */}

            <div className="hero-analysis">

              <div className="hero-analysis-item">

                <span>VERIFICATION</span>

                <strong>
                  Active
                </strong>

              </div>

              <div className="hero-analysis-item">

                <span>CONFIDENCE</span>

                <strong>
                  98.4%
                </strong>

              </div>

            </div>


            {/* Progress */}

            <div className="hero-progress-wrapper">

              <div className="hero-progress-header">

                <span>
                  Evidence Analysis
                </span>

                <span>
                  98%
                </span>

              </div>

              <div className="hero-progress">

                <div className="hero-progress-fill"></div>

              </div>

            </div>

          </div>


          {/* Floating Verification Badge */}

          <div className="hero-floating-card hero-floating-card-one">

            <div className="floating-icon floating-green">
              <FiCheckCircle />
            </div>

            <div>
              <strong>Verified</strong>
              <span>Reliable evidence found</span>
            </div>

          </div>


          {/* Floating Speed Badge */}

          <div className="hero-floating-card hero-floating-card-two">

            <div className="floating-icon floating-purple">
              <FiZap />
            </div>

            <div>
              <strong>Fast Analysis</strong>
              <span>Results in seconds</span>
            </div>

          </div>

        </div>

      </div>


      {/* Bottom Stats */}

      <div className="hero-bottom">

        <div className="hero-stat">
          <strong>AI</strong>
          <span>Powered Detection</span>
        </div>

        <div className="hero-stat">
          <strong>4+</strong>
          <span>Verification Methods</span>
        </div>

        <div className="hero-stat">
          <strong>20MB</strong>
          <span>File Support</span>
        </div>

        <div className="hero-stat">
          <strong>24/7</strong>
          <span>AI Analysis</span>
        </div>

      </div>

    </section>
  );
}

export default Hero;