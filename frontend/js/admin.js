/**
 * Admin dashboard — user management with auto-refresh.
 */

let refreshInterval = null;

document.addEventListener("DOMContentLoaded", () => {
    if (!requireAuth("admin")) return;

    document.getElementById("topbarName").textContent = "Welcome, Admin";
    document.getElementById("logoutBtn").addEventListener("click", logout);

    loadUsers();

    // Auto-refresh every 5 seconds for real-time reflection
    refreshInterval = setInterval(loadUsers, 5000);
});

async function loadUsers() {
    try {
        const users = await apiFetch("/admin/users");
        renderStats(users);
        renderTable(users);
    } catch (err) {
        showAlert("alertBox", err.message);
    }
}

function renderStats(users) {
    const total = users.length;
    const active = users.filter((u) => u.is_active).length;
    const suspended = total - active;

    document.getElementById("statTotal").textContent = total;
    document.getElementById("statActive").textContent = active;
    document.getElementById("statSuspended").textContent = suspended;
}

function renderTable(users) {
    const tbody = document.getElementById("usersTableBody");

    if (users.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align:center; padding:32px; color:var(--text-light);">
                    No users registered yet.
                </td>
            </tr>`;
        return;
    }

    tbody.innerHTML = users
        .map(
            (user) => `
        <tr>
            <td>${escapeHtml(user.name || "—")}</td>
            <td>${escapeHtml(user.email)}</td>
            <td>${escapeHtml(user.phone || "—")}</td>
            <td>${escapeHtml(user.address || "—")}</td>
            <td>
                <span class="badge ${user.is_active ? "badge-active" : "badge-suspended"}">
                    ${user.is_active ? "Active" : "Suspended"}
                </span>
            </td>
            <td>
                <div class="table-actions">
                    <button class="btn btn-sm btn-warning" onclick="toggleSuspend('${user.id}')">
                        ${user.is_active ? "Suspend" : "Activate"}
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="confirmDelete('${user.id}', '${escapeHtml(user.name)}')">
                        Delete
                    </button>
                </div>
            </td>
        </tr>`
        )
        .join("");
}

async function toggleSuspend(userId) {
    try {
        const result = await apiFetch(`/admin/users/${userId}/suspend`, {
            method: "PATCH",
        });
        showAlert("alertBox", result.message, "success");
        await loadUsers();
    } catch (err) {
        showAlert("alertBox", err.message);
    }
}

function confirmDelete(userId, userName) {
    const modal = document.getElementById("deleteModal");
    document.getElementById("deleteUserName").textContent = userName || "this user";
    modal.classList.add("active");

    document.getElementById("confirmDeleteBtn").onclick = async () => {
        modal.classList.remove("active");
        await deleteUser(userId);
    };

    document.getElementById("cancelDeleteBtn").onclick = () => {
        modal.classList.remove("active");
    };
}

async function deleteUser(userId) {
    try {
        const result = await apiFetch(`/admin/users/${userId}`, {
            method: "DELETE",
        });
        showAlert("alertBox", result.message, "success");
        await loadUsers();
    } catch (err) {
        showAlert("alertBox", err.message);
    }
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
