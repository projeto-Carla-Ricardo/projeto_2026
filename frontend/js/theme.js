document.addEventListener("DOMContentLoaded", () => {
    const themeToggleBtn = document.getElementById("theme-toggle");
    
    // Check local storage or default to light
    const currentTheme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", currentTheme);
    
    updateThemeIcon(currentTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            let targetTheme = "light";
            if (document.documentElement.getAttribute("data-theme") === "light") {
                targetTheme = "dark";
            }
            
            document.documentElement.setAttribute("data-theme", targetTheme);
            localStorage.setItem("theme", targetTheme);
            updateThemeIcon(targetTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (!themeToggleBtn) return;
        if (theme === "dark") {
            themeToggleBtn.innerHTML = "☀️";
        } else {
            themeToggleBtn.innerHTML = "🌙";
        }
    }
});
