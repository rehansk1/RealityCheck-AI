import "./Login.css";

function Login({
  onLogin,
  onRegister,
  onForgotPassword,
  onBack,
}) {
  const handleSubmit = (e) => {
    e.preventDefault();

    if (onLogin) {
      onLogin();
    }
  };

  return (
    <div className="login-page">

      {/* Background */}
      <div className="login-background-glow login-glow-one"></div>
      <div className="login-background-glow login-glow-two"></div>

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
          ✦ AI-POWERED VERIFICATION
        </div>

        <h2>
          Verify before
          <span> you believe.</span>
        </h2>

        <p>
          RealityCheck AI helps you analyze news, images and
          documents using intelligent AI-powered verification
          and evidence-based analysis.
        </p>

        <div className="auth-info-features">

          <div>
            <span>✓</span>

            <div>
              <strong>AI-Powered Analysis</strong>
              <small>Intelligent content verification</small>
            </div>
          </div>

          <div>
            <span>◈</span>

            <div>
              <strong>Evidence-Based</strong>
              <small>Understand the evidence behind results</small>
            </div>
          </div>

          <div>
            <span>🔒</span>

            <div>
              <strong>Secure & Private</strong>
              <small>Your information stays protected</small>
            </div>
          </div>

        </div>

        <div className="auth-info-status">
          <span></span>
          Verification systems operational
        </div>

      </div>

      {/* =================================================
          LOGIN CONTENT
          ================================================= */}

      <div className="login-container">

        {/* Logo */}

        <div className="login-logo">

          <div className="login-logo-icon">
            ✓
          </div>

          <div>
            <strong>RealityCheck</strong>
            <span>AI</span>
          </div>

        </div>

        {/* Heading */}

        <div className="login-heading">

          <div className="login-small-label">
            WELCOME BACK
          </div>

          <h1>
            Sign in to your account
          </h1>

          <p>
            Continue to your RealityCheck AI workspace.
          </p>

        </div>

        {/* Card */}

        <div className="login-card">

          <form onSubmit={handleSubmit}>

            <div className="login-field">

              <label htmlFor="login-email">
                Email address
              </label>

              <input
                id="login-email"
                type="email"
                placeholder="you@example.com"
                autoComplete="email"
                required
              />

            </div>

            <div className="login-field">

              <div className="login-password-label">

                <label htmlFor="login-password">
                  Password
                </label>

                <button
                  type="button"
                  className="forgot-password-link"
                  onClick={onForgotPassword}
                >
                  Forgot password?
                </button>

              </div>

              <input
                id="login-password"
                type="password"
                placeholder="Enter your password"
                autoComplete="current-password"
                required
              />

            </div>

            <label className="remember-me">

              <input type="checkbox" />

              <span>
                Remember me
              </span>

            </label>

            <button
              type="submit"
              className="login-submit"
            >
              <span>Sign In</span>
              <span>→</span>
            </button>

          </form>

          <div className="login-divider">
            <span></span>
            <strong>OR</strong>
            <span></span>
          </div>

          <button
            type="button"
            className="google-login"
            onClick={() =>
              alert("Google login will be connected later.")
            }
          >
            <span className="google-icon">
              G
            </span>

            <span>
              Continue with Google
            </span>
          </button>

          <div className="register-prompt">

            <span>
              Don't have an account?
            </span>

            <button
              type="button"
              onClick={onRegister}
            >
              Create an account
            </button>

          </div>

        </div>

        <div className="login-security">
          🔒 Secure authentication · RealityCheck AI
        </div>

      </div>

    </div>
  );
}

export default Login;