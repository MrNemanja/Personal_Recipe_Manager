import './ResendVerification.css'
import { useState } from "react";
import { toast } from "react-toastify";
import { ResendVerificationEmail } from "../services/UserService";

function ResendVerification() {

    const [email, setEmail] = useState("")
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) => {

        e.preventDefault()
        setLoading(true)

        try {

            const response = await ResendVerificationEmail({ email })
            toast.success("Verification email sent!");

        } catch {
            toast.error("Something went wrong.");
        } finally {
            setLoading(false);
        } 
    }


    return (
        <div className="resend-container">
            <form className="resend-card" onSubmit={handleSubmit}>
                <h2>Resend verification email</h2>
                <input
                    type="email"
                    placeholder="Your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <button disabled={loading}>
                    {loading ? "Sending..." : "Send"}
                </button>
            </form>
        </div>
  );

}
export default ResendVerification