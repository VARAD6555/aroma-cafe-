/* Aroma Cafe backend integration.
   The original UI remains intact; this file connects it to Flask + SQLite. */

const API = {
    menu: "/api/menu",
    orders: "/api/orders",
    waiter: "/api/waiter-requests",
    bill: "/api/bill-requests",
    feedback: "/api/feedback"
};

function getTableNumber() {
    const params = new URLSearchParams(window.location.search);
    return params.get("table") || "04";
}

function csrfToken() {
    return document.querySelector('meta[name="csrf-token"]')?.content || "";
}

async function apiFetch(url, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken(),
        ...(options.headers || {})
    };
    const response = await fetch(url, {...options, headers});
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(data.error || "Request failed.");
    }
    return data;
}

async function loadMenuFromBackend() {
    try {
        const data = await apiFetch(API.menu);
        // menuItems is declared by the original frontend as a const array.
        // Mutating it keeps all existing rendering/customisation functions working.
        menuItems.splice(0, menuItems.length, ...data);
        renderMenu("all");
    } catch (error) {
        console.error(error);
        showToast("Menu Error", "Could not load the menu from the server.", "fa-triangle-exclamation");
    }
}

function setTableIndicator() {
    const table = getTableNumber();
    const indicator = document.getElementById("tableIndicator");
    if (indicator) {
        indicator.innerHTML = `<span class="w-2 h-2 rounded-full bg-green-400 animate-ping"></span>Table #${table} • Securely Connected`;
    }
}

window.addEventListener("load", () => {
    setTableIndicator();
    loadMenuFromBackend();
});

async function checkoutOrder() {
    if (cart.length === 0) {
        showToast("Empty Order", "Add at least one item first.", "fa-basket-shopping");
        return;
    }

    try {
        const result = await apiFetch(API.orders, {
            method: "POST",
            body: JSON.stringify({
                table: getTableNumber(),
                items: cart.map(item => ({
                    id: item.id,
                    qty: item.qty,
                    addons: item.addons || [],
                    instructions: item.instructions || ""
                }))
            })
        });

        toggleCart();
        document.getElementById("successModal").classList.remove("hidden");
        cart = [];
        updateCartUI();

        showToast("Order Dispatched", `${result.order_number} sent to the kitchen.`, "fa-paper-plane");
    } catch (error) {
        showToast("Order Failed", error.message, "fa-triangle-exclamation");
    }
}

async function callWaiter() {
    try {
        const result = await apiFetch(API.waiter, {
            method: "POST",
            body: JSON.stringify({table: getTableNumber()})
        });
        showToast("Assistance Requested", result.message, "fa-bell");
    } catch (error) {
        showToast("Request Failed", error.message, "fa-triangle-exclamation");
    }
}

async function requestBill() {
    try {
        const result = await apiFetch(API.bill, {
            method: "POST",
            body: JSON.stringify({table: getTableNumber()})
        });
        showToast("Bill Requested", result.message, "fa-file-invoice-dollar");
    } catch (error) {
        showToast("Request Failed", error.message, "fa-triangle-exclamation");
    }
}

function openFeedbackModal() {
    document.getElementById("feedbackModal").classList.remove("hidden");
    window.selectedFeedbackRating = 5;
}

async function submitFeedback() {
    const modal = document.getElementById("feedbackModal");
    const textarea = modal.querySelector("textarea");
    const message = textarea ? textarea.value.trim() : "";
    const rating = window.selectedFeedbackRating || 5;

    try {
        const result = await apiFetch(API.feedback, {
            method: "POST",
            body: JSON.stringify({
                table: getTableNumber(),
                rating,
                message
            })
        });
        closeFeedbackModal();
        if (textarea) textarea.value = "";
        showToast("Thank You!", result.message, "fa-face-smile");
    } catch (error) {
        showToast("Feedback Failed", error.message, "fa-triangle-exclamation");
    }
}

/* Make the five stars actually selectable. */
document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll("#feedbackModal .fa-star");
    stars.forEach((star, index) => {
        star.addEventListener("click", () => {
            window.selectedFeedbackRating = index + 1;
            stars.forEach((s, i) => {
                s.classList.toggle("text-amber-400", i <= index);
                s.classList.toggle("text-gray-600", i > index);
            });
        });
    });
});
