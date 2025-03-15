const planetaryFileInput = document.getElementById('planetary_data_file');
const rocketFileInput = document.getElementById('rocket_data_file');

const planetaryDropArea = document.getElementById('planetary-drag-drop-area');
const rocketDropArea = document.getElementById('rocket-drag-drop-area');

// si te pui frumos doar aici cand mai adaugi unu
const dropAreas = [planetaryDropArea, rocketDropArea];
const fileInputs = [planetaryFileInput, rocketFileInput];

for (let i = 0; i < dropAreas.length; i++) {
    const dropArea = dropAreas[i];
    const fileInput = fileInputs[i];

    dropArea.addEventListener('click', () => fileInput.click());

    dropArea.addEventListener('dragover', (e) => {
        e = e || event
        e.preventDefault();
        e.stopPropagation();
        dropArea.classList.add('dragover');
    }, false);

    dropArea.addEventListener('dragleave', (e) => {
        e = e || event
        e.stopPropagation();
        e.preventDefault();
        dropArea.classList.remove('dragover');
    }, false);

    dropArea.addEventListener('drop', (e) => {
        e = e || event
        e.preventDefault();
        e.stopPropagation();
        dropArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (0 < files.length <= 1) {
            fileInput.files = files;
        }
    }, false);

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            dropArea.textContent = fileInput.files[0].name;
        }
    }, false);
}

