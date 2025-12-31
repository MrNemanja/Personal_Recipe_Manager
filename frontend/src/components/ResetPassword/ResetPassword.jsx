import "./ResetPassword.css"
import { useState, useEffect } from "react"
import { useSearchParams, Link } from "react-router-dom"
import { toast } from "react-toastify"
import { resetPassword } from "../services/UserService"

function ResetPassword() {
  const [searchParams] = useSearchParams()
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [status, setStatus] = useState("loading")
  const [error, setError] = useState("")

  const token = searchParams.get("token")

  useEffect(() => {
    if (!token) {
      setStatus("invalid")
    } else {
      setStatus("ready")
    }
  }, [token])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")

    if (password !== confirmPassword) {
      setError("Passwords do not match")
      return
    }

    const data = { token, new_password: password }

    try {
      await resetPassword(data)
      toast.success("Password reset successful!")
      setStatus("success")
    } catch {
      toast.error("Reset link is invalid or expired")
    }
  }

  if (status === "invalid") {
    return (
      <div className="reset-container">
        <h2>Invalid reset link ❌</h2>
        <Link to="/forgot-password">Request new link</Link>
      </div>
    )
  }

  if (status === "success") {
    return (
      <div className="reset-container">
        <h2>Password reset successful ✅</h2>
        <Link to="/login">Go to Login</Link>
      </div>
    )
  }

  return (
    <div className="reset-container">
      <form className="reset-card reset-form" onSubmit={handleSubmit}>
        <h2>Reset password</h2>

        <input
          type="password"
          placeholder="New password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Confirm password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />

        {error && <p className="error-text">{error}</p>}

        <button className="reset-btn">Reset password</button>
      </form>
    </div>
  )
}

export default ResetPassword