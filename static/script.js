const dropZone = document.getElementById("drop_zone");
const output = document.getElementById("output");

// --- Function to search by text ---
document.getElementById("searchBtn").addEventListener("click", async function() {
    const query = document.getElementById("searchInput").value.trim();
    if (query === "") {
        output.innerHTML = "Please enter a search term.";
        return;
    }

    output.innerHTML = "Searching...";

    try {
        const response = await fetch('/search_text?query=' + encodeURIComponent(query), {
            method: 'GET',
        });

        const data = await response.json();

        if (data.length === 0) {
            output.innerHTML = "No images found for your query.";
            return;
        }

        // Display results
        const gridContainer = document.createElement('div');
        gridContainer.classList.add('grid-container');

        // Track image sources to avoid duplication
        const seenImages = new Set();

        data.forEach(result => {
            const imagePath = `/images/${result.relative_path}`;
            if (!seenImages.has(imagePath)) {
                seenImages.add(imagePath); // Add this image to the seen set
                const imgElement = document.createElement('img');
                imgElement.src = imagePath;
                imgElement.alt = result.image_id;
                imgElement.classList.add('grid-item');
                gridContainer.appendChild(imgElement);
            }
        });

        output.innerHTML = "";
        output.appendChild(gridContainer);
    } catch (error) {
        output.innerHTML = `Error: ${error}`;
        console.error('Error:', error);
    }
});

// --- Drag and Drop functionality ---
dropZone.addEventListener("dragover", e => {
    e.preventDefault();
    dropZone.classList.add("highlight");
});

dropZone.addEventListener("dragleave", () => dropZone.classList.remove("highlight"));

dropZone.addEventListener("drop", e => {
    e.preventDefault();
    dropZone.classList.remove("highlight");

    const files = e.dataTransfer.files;
    if (!files.length) return;

    const file = files[0];
    if (!file.type.startsWith("image/")) {
        output.innerHTML = "Please drop an image file.";
        return;
    }

    const reader = new FileReader();
    reader.onload = async function (event) {
        const base64Image = event.target.result.split(",")[1];
        
        // Set the background image of the drop zone and clear previous image
        dropZone.style.backgroundImage = `url(${event.target.result})`;
        dropZone.style.color = 'transparent'; // Hide the text when image is uploaded
        output.innerHTML = "Image uploaded. Extracting features...";

        try {
            // --- Step 1: Extract features ---
            const featureResponse = await fetch('/extract_features', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: base64Image })
            });

            const featureData = await featureResponse.json();

            if (!featureData.features) {
                output.innerHTML = `Error extracting features: ${featureData.error || 'Unknown error'}`;
                return;
            }

            output.innerHTML = `Features extracted. Searching similar images...`;

            // --- Step 2: Search for similar images ---
            const searchResponse = await fetch('/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    features: featureData.features,
                    metric: "cosineSimilarity(params.query_vector, 'image_embedding') + 1.0",
                    topK: 5
                })
            });

            const similarImages = await searchResponse.json();

            if (!Array.isArray(similarImages)) {
                output.innerHTML = `Server returned an unexpected response: ${JSON.stringify(similarImages)}`;
                return;
            }

            // ✅ Remove duplicates
            const uniqueImages = [];
            const seen = new Set();
            for (const img of similarImages) {
                const key = img.image_id || img.relative_path;
                if (!seen.has(key)) {
                    seen.add(key);
                    uniqueImages.push(img);
                }
            }

            // --- Step 3: Display results ---
            const gridContainer = document.createElement('div');
            gridContainer.classList.add('grid-container');

            uniqueImages.forEach(img => {
                let imagePath = `/images/${img.relative_path}`;

                // Remove '.txt' extension if it exists
                imagePath = imagePath.replace('.txt', '');

                const imgElement = document.createElement('img');
                imgElement.src = imagePath;
                imgElement.alt = `Image ID: ${img.image_id}`;
                imgElement.classList.add('grid-item');
                gridContainer.appendChild(imgElement);
            });

            // Ensure results show at the top
            output.innerHTML = "";
            output.appendChild(gridContainer);

            console.log('✅ Displayed images:', gridContainer.childNodes.length);
        } catch (error) {
            output.innerHTML = `Error: ${error}`;
            console.error('❌ Error:', error);
        }
    };

    reader.readAsDataURL(file);
});
