import "./ForgotPassword.css";

function ForgotPassword({
  onResetPassword,
  onLogin,
  onBack,
}) {
  const handleSubmit = (e) => {
    e.preventDefault();

    if (onResetPassword) {
      onResetPassword();
    }
  };

  return (
    <div className="forgot-page">

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
          ✦ ACCOUNT SECURITY
        </div>

        <h2>
          Your account,
          <span> protected.</span>
        </h2>

        <p>
          Don't worry. Resetting your password is quick and
          secure. We'll help you get back to your RealityCheck
          AI workspace.
        </p>

        <div className="auth-info-features">

          <div>
            <span>✓</span>

            <div>
              <strong>Secure Recovery</strong>
              <small>Reset your password safely</small>
            </div>
          </div>

          <div>
            <span>✉</span>

            <div>
              <strong>Email Verification</strong>
              <small>We'll send instructions to your email</small>
            </div>
          </div>

          <div>
            <span>🔒</span>

            <div>
              <strong>Privacy Focused</strong>
              <small>Your account information stays protected</small>
            </div>
          </div>

        </div>

        <div className="auth-info-status">
          <span></span>
          Secure account recovery
        </div>

      </div>

      {/* =================================================
          FORGOT PASSWORD
          ================================================= */}

      <div className="forgot-container">

        <div className="forgot-logo">

          <div className="forgot-logo-icon">
            ✓
          </div>

          <div>
            <strong>RealityCheck</strong>
            <span>AI</span>
          </div>

        </div>

        <div className="forgot-heading">

          <div className="forgot-small-label">
            ACCOUNT RECOVERY
          </div>

          <h1>
            Forgot your password?
          </h1>

          <p>
            Enter your email and we'll help you reset your password.
          </p>

        </div>

        <div className="forgot-card">

          <form onSubmit={handleSubmit}>

            <div className="forgot-field">

              <label htmlFor="forgot-email">
                Email address
              </label>

              <input
                id="forgot-email"
                type="email"
                placeholder="you@example.com"
                autoComplete="email"
                required
              />

            </div>

            <button
              type="submit"
              className="forgot-submit"
            >
              <span>Send Reset Link</span>
              <span>→</span>
            </button>

          </form>

          <div className="forgot-login">

            <span>
              Remember your password?
            </span>

            <button
              type="button"
              onClick={onLogin}
            >
              Back to Login
            </button>

          </div>

        </div>

        <div className="forgot-security">
          🔒 Secure authentication · RealityCheck AI
        </div>

      </div>

    </div>
  );
}

export default ForgotPassword;