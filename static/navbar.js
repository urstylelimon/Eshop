document.addEventListener("DOMContentLoaded", function () {
    const cartSidebar = document.getElementById("cartSidebar");

    // Create overlay only once
    if (!document.querySelector(".cart-overlay")) {
        const overlay = document.createElement("div");
        overlay.classList.add("cart-overlay");
        document.body.appendChild(overlay);

        overlay.addEventListener("click", () => {
            cartSidebar.classList.remove("open");
            overlay.classList.remove("show");
        });

        // Attach to global toggle function
        window.toggleCartSidebar = function () {
            cartSidebar.classList.toggle("open");
            overlay.classList.toggle("show");
        };
    }
});


