/**
 * Login page logic.
 */

document.addEventListener("DOMContentLoaded", () => {
    redirectIfLoggedIn();

    const form = document.getElementById("loginForm");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        if (!email || !password) {
            showAlert("alertBox", "Please fill in all fields");
            return;
        }

        setLoading("loginBtn", true);

        try {
            const data = await apiFetch("/auth/login", {
                method: "POST",
                body: JSON.stringify({ email, password }),
            });

            saveAuth(data);

            if (data.role === "admin") {
                window.location.href = "/admin.html";
            } else {
                window.location.href = "/user.html";
            }
        } catch (err) {
            showAlert("alertBox", err.message);
        } finally {
            setLoading("loginBtn", false);
        }
    });
});
