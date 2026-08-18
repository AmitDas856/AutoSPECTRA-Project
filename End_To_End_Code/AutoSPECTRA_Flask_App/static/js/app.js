const fileInput = document.getElementById("can_file");
const selectedFile = document.getElementById("selected-file");
const form = document.getElementById("analysis-form");
const loading = document.getElementById("loading-message");

if (fileInput && selectedFile) {
  fileInput.addEventListener("change", () => {
    selectedFile.textContent = fileInput.files.length
      ? fileInput.files[0].name
      : "No file selected";
  });
}

if (form && loading) {
  form.addEventListener("submit", () => {
    loading.hidden = false;
    const button = form.querySelector("button[type='submit']");
    if (button) {
      button.disabled = true;
      button.textContent = "Running analysis…";
    }
  });
}
