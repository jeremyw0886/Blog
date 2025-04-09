'use strict';

document.addEventListener("DOMContentLoaded", function () {
  console.log("custom.js loaded ✅");

  // === AOS ===
  AOS.init({
    duration: 700,
    easing: "ease-out-quad",
    once: true,
  });

  // === Typed.js ===
  const typedTarget = document.getElementById("typed-text");
  if (typedTarget) {
    new Typed("#typed-text", {
      strings: [
        "Welcome to My Blog",
        "Learning. Writing. Growing.",
        "Sharing ideas that matter.",
      ],
      typeSpeed: 45,
      backSpeed: 20,
      backDelay: 1800,
      loop: true,
    });
  }

  // === Dark Mode Toggle ===
  const toggle = document.getElementById("darkModeToggle");
  const body = document.body;

  if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark-mode");
    if (toggle) toggle.checked = true;
  }

  if (toggle) {
    toggle.addEventListener("change", function () {
      if (this.checked) {
        body.classList.add("dark-mode");
        localStorage.setItem("theme", "dark");
      } else {
        body.classList.remove("dark-mode");
        localStorage.setItem("theme", "light");
      }
    });
  }

  // === Share Button ===
  const shareBtn = document.getElementById("shareBtn");
  if (shareBtn) {
    let isSharing = false;

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
          }, 1000);
        }
      });
    } else {
      // Fallback to copy link
      shareBtn.innerHTML = '<i class="bi bi-clipboard me-1"></i> Copy Link';
      shareBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(window.location.href).then(() => {
          shareBtn.innerHTML =
            '<i class="bi bi-check2-circle me-1"></i> Copied!';
          setTimeout(() => {
            shareBtn.innerHTML =
              '<i class="bi bi-clipboard me-1"></i> Copy Link';
          }, 2000);
        });
      });
    }
  }

  // === TinyMCE ===
  if (typeof tinymce !== "undefined") {
    tinymce.init({
      selector: "textarea.rich-text",
      height: 600,
      menubar: false,
      plugins:
        "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table code help wordcount",
      toolbar:
        "undo redo | blocks | bold italic forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | removeformat code",
      content_style: `
        body {
          font-family: Lato, sans-serif;
          font-size: 16px;
          color: #3d3d3d;
          background-color: transparent;
        }
      `,
    });
    console.log("tinymce loaded");
  }

  // === TinyMCE Form Sync ===
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function () {
      if (window.tinymce) {
        tinymce.triggerSave();
      }
    });
  });
});

// === Confetti (global) ===
function fireConfetti() {
  if (window.confetti) {
    confetti({
      particleCount: 120,
      spread: 60,
      origin: { y: 0.6 },
    });
  }
}

document.querySelectorAll(".react-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const reaction = btn.dataset.reaction;
    const postId = btn.closest(".reaction-buttons").dataset.postId;

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
        if (data[reaction + "s"] !== undefined) {
          btn.querySelector("span").textContent = data[reaction + "s"];
        }
      });
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
