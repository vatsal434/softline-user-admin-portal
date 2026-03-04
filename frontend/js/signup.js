/**
 * Signup page logic.
 */

document.addEventListener("DOMContentLoaded", () => {
    redirectIfLoggedIn();

    const form = document.getElementById("signupForm");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (!name || !email || !password || !confirmPassword) {
            showAlert("alertBox", "Please fill in all fields");
            return;
        }

        if (password.length < 6) {
            showAlert("alertBox", "Password must be at least 6 characters");
            return;
        }

        if (password !== confirmPassword) {
            showAlert("alertBox", "Passwords do not match");
            return;
        }

        setLoading("signupBtn", true);

        try {
            const data = await apiFetch("/auth/signup", {
                method: "POST",
                body: JSON.stringify({ name, email, password }),
            });

            saveAuth(data);
            window.location.href = "/user.html";
        } catch (err) {
            showAlert("alertBox", err.message);
        } finally {
            setLoading("signupBtn", false);
        }
    });
});
