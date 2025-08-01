let BASE_URL = window.location.href;
BASE_URL = BASE_URL[BASE_URL.length - 1] === '/' ? BASE_URL.substring(0, BASE_URL.length - 1) : BASE_URL;

const output_container = document.getElementById('output-container');
const form = document.getElementById('predict-form');
const fileInput = document.getElementById('resume');
const textInput = document.getElementById('text');
const currentFile = document.getElementById('selected-file');
let file = undefined;

output_container.innerHTML = `
    <div class="welcome-container">
        <h1>
            Welcome to AI Job Recommender
        </h1>
        <p>Please type the kind of job you're looking for and also mention about your experience</p>
        <p>OR</p>
        <p>Upload your resume</p>
    </div>
`;

fileInput.addEventListener('change', (e) => {
    file = e.target.files[0];

    if (!file) return;

    currentFile.innerHTML = `
        <div class="show-file">
            <p>${file.name}</p>
            <i class="bi bi-x-circle" onclick="removeFile()"></i>
        </div>
    `;
});

function removeFile() {
    fileInput.value = "";
    file = undefined;
    currentFile.innerHTML = "";
}

form.addEventListener("submit", async function(e) {
    e.preventDefault();

    if (!file && !textInput.value) {
        alert('Either upload your resume or give text input');
        return;
    }

    output_container.innerHTML = `
        <span class="loader"></span>
    `;

    try {
        let prediction = undefined;
        if (file) {
            const formData = new FormData();
            formData.append('file', file, file.name);
            const response = await fetch(`${BASE_URL}/predict-from-pdf`,
                {
                    method: 'POST',
                    body: formData,
                }
            );

            if (response.ok) {
                const responseData = await response.json();
                prediction = responseData;
            } else {
                throw Error('Failed to fetch data');
            }
        } else {
            const response = await fetch(`${BASE_URL}/predict-from-text`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        text: textInput.value,
                    }),
                }
            );

            if (response.ok) {
                const responseData = await response.json();
                prediction = responseData;
            } else {
                throw Error('Failed to fetch data');
            }

            textInput.value = '';
        }

        output_container.innerHTML = '<div id="recommendation-output"></div>';
        const recommendation = document.getElementById('recommendation-output');

        prediction.forEach(pred => {
            recommendation.innerHTML += `
                <div>
                    <h3>${pred.company}</h3>
                    <p>${pred.positionName}</p>
                    <p>Rating: ${pred.rating}</p>
                    <p>Location: ${pred.location}</p>
                    <p>Salary: ${pred.salary === -1 ? 'Not Available' : pred.salary}</p>
                    <p>Job Type: ${pred.job_type}</p>
                    <p>${pred.description}</p>
                    <div>
                        <a href="${pred.url}">Apply Link</a>
                        ${
                            pred.externalApplyLink === -1 ?
                            '' :
                            `<a href="${pred.externalApplyLink}">External Apply Link</a>`
                        }
                    </div>
                </div>
            `;
        });
    } catch(e) {
        output_container.innerHTML = `
            <div class="welcome-container">
                <h1>
                    Welcome to AI Job Recommender
                </h1>
                <p>Please type the kind of job you're looking for and also mention about your experience</p>
                <p>OR</p>
                <p>Upload your resume</p>
            </div>
        `;
        alert(e);
    }
});
