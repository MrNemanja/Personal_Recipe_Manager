import './VerifyEmail.css'
import { useState, useEffect } from "react"
import { useSearchParams, Link } from "react-router-dom"
import { toast } from "react-toastify"
import { VeifyUserEmail } from "../services/UserService"

function VerifyEmail() {
    const [searchParams] = useSearchParams()
    const [status, setStatus] = useState("loading")

    useEffect(() => {
        
        const token = searchParams.get("token")

        if (!token) {
            setStatus("invalid")
            return
        }

        const verify = async () => {
            try {
                await VeifyUserEmail({ token })
                setStatus("success")
                toast.success("Email successfully verified!")
            } catch (err) {
                const detail = err.response?.data?.detail || ""

                if (detail.includes("expired")) {
                    setStatus("expired")
                } else {
                    setStatus("invalid")
                }
            }
        }

        verify()
    }, [searchParams])


   if (status === "loading") {
        return (
            <div className="verify-container">
                <div className="verify-spinner" />
                <p>Verifying your email...</p>
            </div>
        )
    }

    if (status === "success") {
        return (
            <div className="verify-container">
                <h2>Email verified ✅</h2>
                <p>You can now log in.</p>
                <Link to="/login">Go to login</Link>
            </div>
        )
    }

    if (status === "expired") {
        return (
            <div className="verify-container">
                <h2>Link expired ⏰</h2>
                <p>Your verification link has expired.</p>
                <Link to="/resend-verification">Resend verification</Link>
            </div>
        )
    }

   return (
        <div className="verify-container">
            <h2>Invalid verification link ❌</h2>
            <p>Please use the link from your email.</p>
        </div>
    )
}

export default VerifyEmail