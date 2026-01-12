const fs = require('fs');

try {
    // Copy Black Blazer (assuming image 0)
    fs.copyFileSync(
        'C:/Users/Hager/.gemini/antigravity/brain/b16a0fc8-1ce4-4968-9262-3571750608e8/uploaded_image_0_1768221247415.jpg',
        'd:/Zoomcamp/virtual-wardrobe-joy/frontend/public/assets/clothing-2-black.jpg'
    );
    console.log("Copied clothing-2-black.jpg");

    // Copy Charcoal Blazer (assuming image 1)
    fs.copyFileSync(
        'C:/Users/Hager/.gemini/antigravity/brain/b16a0fc8-1ce4-4968-9262-3571750608e8/uploaded_image_1_1768221247415.jpg',
        'd:/Zoomcamp/virtual-wardrobe-joy/frontend/public/assets/clothing-2-charcoal.jpg'
    );
    console.log("Copied clothing-2-charcoal.jpg");
} catch (error) {
    console.error("Error copying files:", error);
}
