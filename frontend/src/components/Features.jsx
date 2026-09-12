import {
  FiCpu,
  FiFileText,
  FiBarChart2,
  FiZap,
  FiShield,
  FiCheckCircle,
} from "react-icons/fi";

import "./Features.css";

function Features() {
  const features = [
    {
      icon: <FiCpu />,
      title: "AI Detection",
      text: "Advanced AI models analyze content and identify signs of misleading or manipulated information.",
    },
    {
      icon: <FiFileText />,
      title: "Smart Summarization",
      text: "Turn lengthy news articles and documents into clear, concise summaries in seconds.",
    },
    {
      icon: <FiBarChart2 />,
      title: "Confidence Score",
      text: "Understand how confident the AI is with every verification result and prediction.",
    },
    {
      icon: <FiZap />,
      title: "Lightning Fast",
      text: "Get AI-powered analysis quickly without complicated verification processes.",
    },
    {
      icon: <FiShield />,
      title: "Secure Analysis",
      text: "Your uploaded content is processed securely and is not publicly displayed.",
    },
    {
      icon: <FiCheckCircle />,
      title: "Evidence Based",
      text: "Verification can use supporting sources and evidence to provide a more informed result.",
    },
  ];

  return (
    <section className="features" id="features">
      <div className="features-container">

        {/* HEADER */}

        <div className="features-header">

          <div className="features-badge">
            <span className="features-badge-dot"></span>
            POWERFUL VERIFICATION TOOLS
          </div>

          <h2>
            Everything You Need to
            <span> Verify Information.</span>
          </h2>

          <p>
            RealityCheck AI combines artificial intelligence,
            evidence analysis and simple results to help you
            make better-informed decisions.
          </p>

        </div>

        {/* FEATURE GRID */}

        <div className="feature-grid">

          {features.map((feature, index) => (
            <div
              className="feature-card"
              key={index}
            >

              <div className="feature-card-top">

                <div className="feature-icon">
                  {feature.icon}
                </div>

                <span className="feature-number">
                  0{index + 1}
                </span>

              </div>

              <h3>
                {feature.title}
              </h3>

              <p>
                {feature.text}
              </p>

              <div className="feature-line"></div>

            </div>
          ))}

        </div>

        {/* BOTTOM TRUST BAR */}

        <div className="features-bottom">

          <div>
            <FiCheckCircle />
            <span>AI-Powered</span>
          </div>

          <div>
            <FiShield />
            <span>Privacy Focused</span>
          </div>

          <div>
            <FiBarChart2 />
            <span>Evidence Based</span>
          </div>

          <div>
            <FiZap />
            <span>Fast Results</span>
          </div>

        </div>

      </div>
    </section>
  );
}

export default Features;