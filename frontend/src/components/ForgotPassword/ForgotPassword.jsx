import "./ForgotPassword.css"
import { useState } from "react"
import { toast } from "react-toastify"
import { requestPasswordReset } from "../services/UserService"

function ForgotPassword() {
  const [email, setEmail] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await requestPasswordReset({ email })
      toast.success("If the email exists, a reset link has been sent.")
      setEmail("")
    } catch {
      toast.error("Something went wrong.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="forgot-container">
      <form className="forgot-card forgot-form" onSubmit={handleSubmit}>
        <h2>Forgot your password?</h2>
        <p className="forgot-subtitle">Enter your email and we’ll send you a reset link.</p>

        <input
          type="email"
          placeholder="Your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <button className="forgot-btn" disabled={loading}>
          {loading ? "Sending..." : "Send reset link"}
        </button>
      </form>
    </div>
  )
}

export default ForgotPassword