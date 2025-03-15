const fileInput = document.getElementById('planetary_data_file');
const dragDropArea = document.getElementById('drag-drop-area');

dragDropArea.addEventListener('click', () => fileInput.click());

dragDropArea.addEventListener('dragover', (e) => {
    e = e || event
    e.preventDefault();
    e.stopPropagation();
    dragDropArea.classList.add('dragover');
},false);

dragDropArea.addEventListener('dragleave', (e) => {
    e = e || event
    e.stopPropagation();
    e.preventDefault();
    dragDropArea.classList.remove('dragover');
},false);

dragDropArea.addEventListener('drop', (e) => {
    e = e || event
    e.preventDefault();
    e.stopPropagation();
    dragDropArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (0 < files.length <= 1) {
        fileInput.files = files;
    }
},false);

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        dragDropArea.textContent = fileInput.files[0].name;
    }
},false);