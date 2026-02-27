import { useState, useEffect } from "react"
import { getUserProfile } from "../services/UserService"
import "./Profile.css"

function Profile() {

    const [profile, setProfile] = useState(null)
    const [editData, setEditData] = useState({})
    const [loading, setLoading] = useState(null)
    const baseURL = import.meta.env.VITE_API_URL

    useEffect(() => {

        const fetchProfile = async () => {
            try {
                const data = await getUserProfile()
                setProfile(data);
                setEditData({
                    full_name: data.full_name || "",
                    phone: data.phone || "",
                    city: data.city || "",
                    country: data.country || "",
                    dob: data.dob || "",
                });
            } catch (err) {
                console.error("Failed to fetch profile:", err);
            } finally {
                setLoading(false);
            }
        }

        fetchProfile()
    }, [])

    const handleChange = (e) => {
        setEditData({
            ...editData,
            [e.target.name]: e.target.value,
        });
    };

    const handleUpdate = () => {
        alert("Update function is not implemented.");
    };

    if (loading) return <p>Loading profile...</p>
    if (!profile) return <p>Failed to load profile.</p>

    return(
        <div className="profile-card">
            <h2>Your Profile</h2>
            <div className="profile-container">
                <div className="profile-left">
                    <img
                        src={`${baseURL} + ${profile.profile_image}` || "/images/user-icon.png"}
                        alt="Profile"
                        className="profile-image"
                    />
                    {console.log(profile.profile_image)}
                    <p><b>Username:</b> {profile.username}</p>
                    <p><b>Email:</b> {profile.email}</p>
                    <p><b>Full Name:</b> {profile.full_name}</p>
                    <p><b>Phone:</b> {profile.phone}</p>
                    <p><b>City:</b> {profile.city}</p>
                    <p><b>Country:</b> {profile.country}</p>
                    <p><b>Date Of Birth:</b> {profile.dob}</p>
                    <p><b>MFA:</b> {profile.mfa_enabled ? "Enabled" : "Disabled"}</p>
                    {!profile.mfa_enabled && <button className="mfa-btn">Enable MFA</button>}
                </div>
                <div className="profile-right">
                    <h3>Edit Profile</h3>
                    <form className="profile-form">
                        <label>Full Name</label>
                        <input type="text" name="full_name" value={editData.full_name} 
                        onChange={handleChange} placeholder="Full Name" />

                        <label>Phone</label>
                        <input type="text" name="phone" value={editData.phone} 
                        onChange={handleChange} placeholder="Phone" />

                        <label>City</label>
                        <input type="text" name="city" value={editData.city}
                        onChange={handleChange} placeholder="City" />

                        <label>Country</label>
                        <input type="text" name="country" value={editData.country}
                        onChange={handleChange} placeholder="Country" />

                        <label>Date of Birth</label>
                        <input type="date" name="dob" value={editData.dob}
                        onChange={handleChange} />

                        <button type="button" onClick={handleUpdate}>Save Changes</button>
                    </form>
                </div>
            </div>
        </div>
    )
}
export default Profile