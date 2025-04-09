"use strict";

/**
 * Initializes TinyMCE editor with theme-aware styling.
 * @function initTinyMCE
 */
function initTinyMCE() {
  const isDarkMode = document.body.classList.contains("dark-mode");
  // Ensure TinyMCE is available before initialization
  if (!window.tinymce) {
    console.warn("TinyMCE not loaded; using plain textarea");
    return;
  }

  tinymce.init({
    selector: "textarea.rich-text",
    height: 600,
    menubar: false,
    // Comprehensive plugin set for rich text editing
    plugins: "advlist autolink lists link image charmap preview " +
             "anchor searchreplace visualblocks code fullscreen " +
             "insertdatetime media table code help wordcount",
    // Toolbar layout designed for essential formatting
    toolbar: "undo redo | blocks | bold italic forecolor " +
             "backcolor | alignleft aligncenter alignright " +
             "alignjustify | bullist numlist outdent indent | " +
             "link image media | removeformat code",
    skin: isDarkMode ? "oxide-dark" : "oxide",
    content_css: isDarkMode ? "dark" : "default",
    content_style: `
      body {
        font-family: Lato, sans-serif;
        font-size: 16px;
        color: ${isDarkMode ? "#f1f1f1" : "#3d3d3d"};
        background-color: ${isDarkMode ? "#1f1f1f" : "#ffffff"};
      }
    `
  });
}

/**
 * Triggers confetti animation for celebratory effects.
 * @function fireConfetti
 */
function fireConfetti() {
  if (window.confetti) {
    confetti({
      particleCount: 120, // Balanced visual impact
      spread: 60, // Controlled spread
      origin: { y: 0.6 } // Mid-screen origin
    });
  }
}

/**
 * Displays temporary notification messages.
 * @function showToast
 * @param {string} message - The message to display
 */
function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast-msg position-fixed bottom-0 end-0 " +
                    "bg-success text-white p-2 rounded m-3 shadow";
  toast.style.zIndex = 1055;
  toast.style.maxWidth = "300px";
  toast.style.fontSize = "0.9rem";
  toast.textContent = message;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("fade-out");
    setTimeout(() => toast.remove(), 500);
  }, 2500); // Visible for 2.5s
}

/**
 * Retrieves a cookie value by name.
 * @function getCookie
 * @param {string} name - The name of the cookie
 * @returns {string|null} The cookie value or null
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const trimmed = cookie.trim();
      if (trimmed.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(trimmed.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Main DOM content loaded event listener
document.addEventListener("DOMContentLoaded", function () {
  console.log("custom.js loaded ✅");

  /* ==========================================================================
   * AOS Initialization
   * Why: Provides smooth scroll animations for better UX
   * ========================================================================== */
  AOS.init({
    duration: 700, // Balanced duration for visibility
    easing: "ease-out-quad", // Smooth animation curve
    once: true, // Prevents repeated triggers
  });

  /* ==========================================================================
   * Typed.js Setup
   * Why: Creates engaging welcome text animation
   * ========================================================================== */
  const typedTarget = document.getElementById("typed-text");
  if (typedTarget) {
    new Typed("#typed-text", {
      strings: [
        "Welcome to Inkstack!",
        "Learning. Writing. Growing.",
        "Sharing ideas that matter."
      ],
      typeSpeed: 45, // Moderate typing speed
      backSpeed: 20, // Slower backspace for readability
      backDelay: 1800, // Pause before looping
      loop: true // Continuous engagement
    });
  }

  /* ==========================================================================
   * Dark Mode Handling
   * Why: Enhances accessibility and user preference
   * ========================================================================== */
  const toggle = document.getElementById("darkModeToggle");
  const body = document.body;

  // Apply saved theme on load
  if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark-mode");
    if (toggle) toggle.checked = true;
  }

  // Toggle dark mode and reinitialize editor
  if (toggle) {
    toggle.addEventListener("change", function () {
      if (this.checked) {
        body.classList.add("dark-mode");
        localStorage.setItem("theme", "dark");
      } else {
        body.classList.remove("dark-mode");
        localStorage.setItem("theme", "light");
      }
      // Refresh TinyMCE to match theme
      if (tinymce.activeEditor) tinymce.activeEditor.remove();
      initTinyMCE();
    });
  }

  // Initial TinyMCE setup
  initTinyMCE();

  /* ==========================================================================
   * Form Submission Sync
   * Why: Ensures TinyMCE content is saved and validated
   * ========================================================================== */
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    if (form.querySelector("textarea.rich-text")) {
      form.addEventListener("submit", function (e) {
        if (window.tinymce) {
          tinymce.triggerSave(); // Sync editor content
          const contentField = form.querySelector("textarea.rich-text");
          // Prevent empty submissions
          if (contentField && contentField.value.trim() === "") {
            e.preventDefault();
            alert("Post content is required.");
            tinymce.activeEditor.focus();
          }
        }
      });
    }
  });

  /* ==========================================================================
   * Share Functionality
   * Why: Simplifies content sharing across platforms
   * ========================================================================== */
  const shareBtn = document.getElementById("shareBtn");
  if (shareBtn) {
    let isSharing = false; // Prevents multiple clicks

    if (navigator.share) {
      shareBtn.addEventListener("click", async () => {
        if (isSharing) return;
        isSharing = true;
        shareBtn.disabled = true;
        try {
          await navigator.share({
            title: document.title,
            text: "Check out this blog on Inkstack!",
            url: window.location.href,
          });
        } catch (err) {
          console.error("Share failed:", err);
        } finally {
          setTimeout(() => {
            shareBtn.disabled = false;
            isSharing = false;
          }, 1000); // Debounce reset
        }
      });
    } else {
      // Fallback for unsupported browsers
      shareBtn.innerHTML = '<i class="bi bi-clipboard me-1"></i> Copy Link';
      shareBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(window.location.href).then(() => {
          shareBtn.innerHTML =
            '<i class="bi bi-check2-circle me-1"></i> Copied!';
          setTimeout(() => {
            shareBtn.innerHTML =
              '<i class="bi bi-clipboard me-1"></i> Copy Link';
          }, 2000); // Feedback duration
        });
      });
    }
  }

  /* ==========================================================================
   * Emoji Reaction Handling
   * Why: Enables interactive post engagement
   * ========================================================================== */
  document.body.addEventListener("click", function (e) {
    if (e.target.closest(".btn-emoji")) {
      const btn = e.target.closest(".btn-emoji");
      const reaction = btn.dataset.reaction;
      const postId = btn.closest(".reaction-buttons").dataset.postId;
      // Send reaction to server
      fetch(`/react/${postId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `reaction=${reaction}`,
      })
        .then((res) => res.json())
        .then((data) => {
          // Update reaction count dynamically
          if (data[reaction + "s"] !== undefined) {
            btn.querySelector("span").textContent = data[reaction + "s"];
          }
        });
    }
  });

  /* ==========================================================================
   * Delete Comment AJAX
   * Why: Provides seamless comment removal
   * ========================================================================== */
  document.body.addEventListener("click", function (e) {
    if (e.target.classList.contains("delete-comment-btn")) {
      const btn = e.target;
      const commentId = btn.dataset.commentId;

      if (!confirm("Delete this comment?")) return;

      fetch(`/comment/${commentId}/delete/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            const commentDiv = document.getElementById(
              `comment-${commentId}`
            );
            commentDiv.remove();
            showToast("Comment deleted ✅");
          }
        });
    }
  });
});