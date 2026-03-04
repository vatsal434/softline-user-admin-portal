/**
 * User dashboard — profile view & update.
 */

document.addEventListener("DOMContentLoaded", () => {
    if (!requireAuth("user")) return;

    loadProfile();

    document.getElementById("editBtn").addEventListener("click", showEditForm);
    document.getElementById("cancelBtn").addEventListener("click", hideEditForm);
    document.getElementById("profileForm").addEventListener("submit", updateProfile);
    document.getElementById("logoutBtn").addEventListener("click", logout);
});

async function loadProfile() {
    try {
        const user = await apiFetch("/user/profile");
        renderProfile(user);
    } catch (err) {
        showAlert("alertBox", err.message);
    }
}

function renderProfile(user) {
    document.getElementById("userName").textContent = user.name || "—";
    document.getElementById("userEmail").textContent = user.email;
    document.getElementById("userPhone").textContent = user.phone || "—";
    document.getElementById("userAddress").textContent = user.address || "—";
    document.getElementById("userJoined").textContent = formatDate(user.created_at);

    // Pre-fill the edit form
    document.getElementById("editName").value = user.name || "";
    document.getElementById("editPhone").value = user.phone || "";
    document.getElementById("editAddress").value = user.address || "";

    // Update topbar
    document.getElementById("topbarName").textContent = `Welcome, ${user.name || user.email}`;
}

function showEditForm() {
    document.getElementById("profileView").style.display = "none";
    document.getElementById("profileEdit").style.display = "block";
}

function hideEditForm() {
    document.getElementById("profileView").style.display = "block";
    document.getElementById("profileEdit").style.display = "none";
}

async function updateProfile(e) {
    e.preventDefault();

    const name = document.getElementById("editName").value.trim();
    const phone = document.getElementById("editPhone").value.trim();
    const address = document.getElementById("editAddress").value.trim();

    if (!name) {
        showAlert("alertBox", "Name is required");
        return;
    }

    setLoading("saveBtn", true);

    try {
        const updated = await apiFetch("/user/profile", {
            method: "PUT",
            body: JSON.stringify({ name, phone, address }),
        });

        renderProfile(updated);
        hideEditForm();
        showAlert("alertBox", "Profile updated successfully!", "success");
    } catch (err) {
        showAlert("alertBox", err.message);
    } finally {
        setLoading("saveBtn", false);
    }
}

function formatDate(dateStr) {
    if (!dateStr) return "—";
    try {
        return new Date(dateStr).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
        });
    } catch {
        return dateStr;
    }
}
