const dropArea = document.querySelector(".drop-area");
const text = dropArea.querySelector("p");
const button = document.getElementById("browse-file-btn");
const input = document.getElementById("input-file");

//handling input click event using button
button.addEventListener("click", () => input.click());

//adding an event listener to the input
input.addEventListener("change", (e) => {
  //extracting a file from an event object
  let file = e.target.files[0];
  //calling upload function
  upload(file);
});

//if user drag file over drop area stop default functionality
dropArea.addEventListener("dragover", (e) => e.preventDefault());

//When a user drops a file, the file is uploaded.
dropArea.addEventListener("drop", (e) => {
  //stops default functionality
  e.preventDefault();
  //extraction of a file from a drop event
  let file = e.dataTransfer.files[0];
  //calling upload function
  upload(file);
});

//function to check the image type. return 'true' or 'false'
const check = (file) => {
  let extensions = ["image/png", "image/jpg", "image/jpeg"];
  if (extensions.includes(file.type)) return true;

  return false;
};

//function to remove a previous image
const clear = () => {
  let img = dropArea.querySelector("img");
  if (img) dropArea.removeChild(img);
};

//function to upload image
const upload = (file) => {
  //calling clear function first
  clear();

  //checking if the file type is an image or not
  if (check(file)) {
    //create a string of the given file object
    let imgLink = URL.createObjectURL(file);
    //creating a new image tag
    let imgTag = document.createElement("img");
    //adding imgLink to the new image tag source
    imgTag.src = imgLink;
    //append this new image tag to the drop area.
    dropArea.appendChild(imgTag);
    dropArea.classList.add("active");
    dropArea.classList.remove("error");
    text.innerText = "Drag and drop to upload file";
  } else {
    dropArea.classList.remove("active");
    dropArea.classList.add("error");
    text.innerText = "File type is not an image try again!";
  }
};
