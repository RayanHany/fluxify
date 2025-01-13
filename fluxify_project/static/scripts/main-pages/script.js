const dropArea = document.querySelector(".drop-area");
const text = dropArea.querySelector("p");
const button = document.getElementById("browse-file-btn");
const input = document.getElementById("input-file");
const form = document.getElementById("upload-form");

// Handling input click event using button
button.addEventListener("click", () => input.click());

// Adding an event listener to the input
input.addEventListener("change", (e) => {
  let file = e.target.files[0];
  upload(file);
});

// If user drags a file over drop area, stop default functionality
dropArea.addEventListener("dragover", (e) => e.preventDefault());

// When a user drops a file, handle the upload
dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  let file = e.dataTransfer.files[0];
  upload(file);
});

// Function to check the image type
const check = (file) => {
  let extensions = ["image/png", "image/jpg", "image/jpeg"];
  return extensions.includes(file.type);
};

// Function to clear previous images
const clear = () => {
  let img = dropArea.querySelector("img");
  if (img) dropArea.removeChild(img);
};

// Function to upload image
const upload = (file) => {
  clear();

  if (check(file)) {
    // Preview image
    let imgLink = URL.createObjectURL(file);
    let imgTag = document.createElement("img");
    imgTag.src = imgLink;
    dropArea.appendChild(imgTag);
    dropArea.classList.add("active");
    dropArea.classList.remove("error");
    text.innerText = "Drag and drop to upload file";

    // Submit image to the server
    const formData = new FormData();
    formData.append("image", file);

    fetch("/upload/", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": getCSRFToken(), // Ensure CSRF token is included
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  } else {
    dropArea.classList.remove("active");
    dropArea.classList.add("error");
    text.innerText = "File type is not an image. Try again!";
  }
};

// Function to get CSRF token from cookies
function getCSRFToken() {
  let cookieValue = null;
  let cookies = document.cookie.split(";");

  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    if (cookie.startsWith("csrftoken=")) {
      cookieValue = cookie.substring("csrftoken=".length);
      break;
    }
  }
  return cookieValue;
}
