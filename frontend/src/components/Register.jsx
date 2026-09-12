import "./Register.css";

function Register({
  onRegister,
  onLogin,
  onBack,
}) {
  const handleSubmit = (e) => {
    e.preventDefault();

    if (onRegister) {
      onRegister();
    }
  };

  return (
    <div className="register-page">

      {/* Back */}

      <button
        type="button"
        className="auth-back-button"
        onClick={onBack}
      >
        <span className="auth-back-arrow">←</span>
        <span>Back to RealityCheck AI</span>
      </button>

      {/* =================================================
          LEFT INFORMATION
          ================================================= */}

      <div className="auth-info-panel">

        <div className="auth-info-badge">
          ✦ JOIN REALITYCHECK AI
        </div>

        <h2>
          Start making
          <span> smarter decisions.</span>
        </h2>

        <p>
          Create your RealityCheck AI account and get access
          to intelligent tools designed to help you verify
          information before you trust or share it.
        </p>

        <div className="auth-info-features">

          <div>
            <span>01</span>

            <div>
              <strong>Analyze Images</strong>
              <small>Detect signs of AI-generated content</small>
            </div>
          </div>

          <div>
            <span>02</span>

            <div>
              <strong>Verify News</strong>
              <small>Check claims using supporting evidence</small>
            </div>
          </div>

          <div>
            <span>03</span>

            <div>
              <strong>Analyze Documents</strong>
              <small>Turn information into clear insights</small>
            </div>
          </div>

        </div>

        <div className="auth-info-status">
          <span></span>
          Your verification workspace awaits
        </div>

      </div>

      {/* =================================================
          REGISTER
          ================================================= */}

      <div className="register-container">

        <div className="register-logo">

          <div className="register-logo-icon">
            ✓
          </div>

          <div>
            <strong>RealityCheck</strong>
            <span>AI</span>
          </div>

        </div>

        <div className="register-heading">

          <div className="register-small-label">
            GET STARTED
          </div>

          <h1>
            Create your account
          </h1>

          <p>
            Start verifying information with RealityCheck AI.
          </p>

        </div>

        <div className="register-card">

          <form onSubmit={handleSubmit}>

            <div className="register-field">

              <label htmlFor="register-name">
                Full name
              </label>

              <input
                id="register-name"
                type="text"
                placeholder="Your name"
                autoComplete="name"
                required
              />

            </div>

            <div className="register-field">

              <label htmlFor="register-email">
                Email address
              </label>

              <input
                id="register-email"
                type="email"
                placeholder="you@example.com"
                autoComplete="email"
                required
              />

            </div>

            <div className="register-field">

              <label htmlFor="register-password">
                Password
              </label>

              <input
                id="register-password"
                type="password"
                placeholder="Create a password"
                autoComplete="new-password"
                required
              />

            </div>

            <div className="register-field">

              <label htmlFor="register-confirm-password">
                Confirm password
              </label>

              <input
                id="register-confirm-password"
                type="password"
                placeholder="Confirm your password"
                autoComplete="new-password"
                required
              />

            </div>

            <label className="register-terms">

              <input
                type="checkbox"
                required
              />

              <span>
                I agree to the Terms and Privacy Policy.
              </span>

            </label>

            <button
              type="submit"
              className="register-submit"
            >
              <span>Create Account</span>
              <span>→</span>
            </button>

          </form>

          <div className="login-prompt">

            <span>
              Already have an account?
            </span>

            <button
              type="button"
              onClick={onLogin}
            >
              Sign in
            </button>

          </div>

        </div>

        <div className="register-security">
          🔒 Secure authentication · RealityCheck AI
        </div>

      </div>

    </div>
  );
}

export default Register;