

// Variables to store user selections
let userSelections = {
    gender: '',
    body_type: '',
    occasion: ''
};

// Body types for male and female
const bodyTypes = {
    male: ["Trapazoid", "Oval", "Rectangle", "Triangle", "Inverted Triangle"],
    female: ["Pear", "Hourglass", "Rectangle", "Apple", "Inverted Triangle"]
};

// Step 1: Select Gender
function selectGender(gender) {
    userSelections.gender = gender;
    updateBodyTypes(gender);
    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'block';
}

// Step 2: Update Body Types and Show Next Question
function updateBodyTypes(gender) {
    const bodyTypeSelect = document.getElementById('bodyType');
    bodyTypeSelect.innerHTML = ''; // Clear existing options

    // Populate options based on selected gender
    bodyTypes[gender].forEach(type => {
        const option = document.createElement('option');
        option.value = type.toLowerCase();
        option.textContent = type;
        bodyTypeSelect.appendChild(option);
    });
}

// Proceed to Step 3 after body type selection
function goToOccasion() {
    userSelections.body_type = document.getElementById('bodyType').value;
    document.getElementById('step2').style.display = 'none';
    document.getElementById('step3').style.display = 'block';
}

// Step 3: Select Occasion
function selectOccasion(occasion) {
    userSelections.occasion = occasion;
    document.getElementById('step3').style.display = 'none';
    document.getElementById('output').style.display = 'block';
    getRecommendation(); // Finalize quiz and get recommendation
}

// Get Recommendation from Flask Backend
function getRecommendation() {
    fetch('/recommend-outfit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userSelections)
    })
    .then(response => response.json())
    .then(data => {
        // Hide quiz container
        const quizContainer = document.querySelector('.quiz-container');
        if (quizContainer) {
            quizContainer.style.display = 'none';
        }

        // Display the recommendation
        const recommendationContainer = document.getElementById('recommendation');
        recommendationContainer.innerHTML = ''; // Clear previous results

        data.images.forEach(imagePath => {
            const img = document.createElement('img');
            img.src = imagePath; // Set image source
            img.alt = "Recommended Outfit"; // Add alt text
            img.style.maxWidth = "200px"; // Style the image
            img.style.margin = "10px"; // Add spacing
            recommendationContainer.appendChild(img);
        });

        // Show the output container
        document.getElementById('output').style.display = 'block';
    })
    .catch(error => {
        console.error('Error fetching recommendations:', error);
    });
}

// Navigation: Go Back to Step 1 (Gender Selection)
function goBackToGender() {
    document.getElementById('step2').style.display = 'none';
    document.getElementById('step1').style.display = 'block';
}

// Navigation: Go Back to Step 2 (Body Type Selection)
function goBackToBodyType() {
    document.getElementById('step3').style.display = 'none';
    document.getElementById('step2').style.display = 'block';
}

// Navigation: Go Back to Step 3 (Occasion Selection)
function goBackToSelectOccasion() {
    // Hide the output section
    document.getElementById('output').style.display = 'none';

    // Show quiz container and Step 3
    document.querySelector('.quiz-container').style.display = 'block';
    const step3 = document.getElementById('step3');
    step3.style.display = 'block';
    step3.classList.add('active');

    // Hide other steps
    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'none';
}
