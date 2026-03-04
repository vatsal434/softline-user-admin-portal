/**
 * Shared API helper and auth utilities.
 */

const API_BASE = window.location.origin + "/api";

// ──────────────── Token Management ────────────────

function saveAuth(data) {
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("role", data.role);
    localStorage.setItem("user_id", data.user_id);
}

function getToken() {
    return localStorage.getItem("token");
}

function getRole() {
    return localStorage.getItem("role");
}

function getUserId() {
    return localStorage.getItem("user_id");
}

function clearAuth() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("user_id");
}

function isLoggedIn() {
    return !!getToken();
}

function logout() {
    clearAuth();
    window.location.href = "/login.html";
}

// ──────────────── API Helper ────────────────

async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {}),
    };

    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(url, {
            ...options,
            headers,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong");
        }

        return data;
    } catch (error) {
        if (error.message === "Invalid or expired token" || error.message === "Not authenticated") {
            clearAuth();
            window.location.href = "/login.html";
            return;
        }
        throw error;
    }
}

// ──────────────── UI Helpers ────────────────

function showAlert(elementId, message, type = "error") {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = message;
    el.className = `alert alert-${type}`;
    el.style.display = "block";
    setTimeout(() => {
        el.style.display = "none";
    }, 5000);
}

function setLoading(buttonId, loading) {
    const btn = document.getElementById(buttonId);
    if (!btn) return;
    if (loading) {
        btn.dataset.originalText = btn.innerHTML;
        btn.innerHTML = '<span class="spinner"></span> Please wait...';
        btn.disabled = true;
    } else {
        btn.innerHTML = btn.dataset.originalText || btn.innerHTML;
        btn.disabled = false;
    }
}

// ──────────────── Route Guards ────────────────

function requireAuth(allowedRole) {
    if (!isLoggedIn()) {
        window.location.href = "/login.html";
        return false;
    }
    if (allowedRole && getRole() !== allowedRole) {
        window.location.href = getRole() === "admin" ? "/admin.html" : "/user.html";
        return false;
    }
    return true;
}

function redirectIfLoggedIn() {
    if (isLoggedIn()) {
        window.location.href = getRole() === "admin" ? "/admin.html" : "/user.html";
    }
}
