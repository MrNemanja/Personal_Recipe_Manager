import { useState, useEffect } from "react";
import { SetupMfa, VerifyMfaSetup, VerifyMfaLogin } from "../services/UserService";
import './MfaModal.css'

function MfaModal({mfaToken, mode, onSuccess}) {

    const [code, setCode] = useState('')
    const [qrUrl, setQrUrl] = useState(false)

    useEffect(() => {
        
        if(mode === 'setup') {
            const fetchQr = async () => {
                const response = await SetupMfa();
                const url = URL.createObjectURL(response);
                setQrUrl(url);
            };
            fetchQr();
        }
    }, [mode]);

    const handleVerify = async (e) => {
        
        e.preventDefault();

         const data = {
            code: code,
            mfa_token: mfaToken
        }

        try {
            if (mode === "setup") {
                await VerifyMfaSetup({code});
            } else {
                await VerifyMfaLogin(data);
            }
            onSuccess();
        } catch (error) {
            alert(error.response?.data?.detail || "Invalid MFA code");
        }
  };

    return (
        <div className="mfa-modal-backdrop">
            <div className="mfa-modal">
                <h3>Multi-Factor Authentication</h3>
                {mode === "setup" && qrUrl && (
                    <>
                        <p>Scan the QR code with your authenticator app:</p>
                        <img src={qrUrl} alt="Scan QR code" />
                        <p>Then enter the 6-digit code:</p>
                    </>
                )}
                {mode === "login" && <p>Enter the 6-digit code from your authenticator app:</p>}

                <form onSubmit={handleVerify}>
                    <input
                        type="text"
                        value={code}
                        onChange={e => setCode(e.target.value)}
                        placeholder="6-digit code"
                        required
                    />
                    <button type="submit">{mode === "setup" ? "Enable MFA" : "Verify"}</button>
                </form>
            </div>
        </div>
    );

}
export default MfaModal