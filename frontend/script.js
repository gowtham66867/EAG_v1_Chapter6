document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('wellness-form');
    const resultsContainer = document.getElementById('results-container');
    const loadingSpinner = document.getElementById('loading-spinner');
    const planOutput = document.getElementById('plan-output');
    const submitBtn = document.getElementById('submit-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Get form data
        const formData = new FormData(form);
        const userProfile = {
            goals: formData.get('goals'),
            sleep: formData.get('sleep'),
            schedule: formData.get('schedule'),
            diet: formData.get('diet'),
        };

        // 2. Show loading state
        resultsContainer.classList.remove('hidden');
        loadingSpinner.classList.remove('hidden');
        planOutput.innerHTML = '';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Generating...';

        try {
            // 3. Call the backend API
            const response = await fetch('http://127.0.0.1:5002/api/generate-plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userProfile),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const plan = await response.json();

            // 4. Render the plan
            renderPlan(plan);

        } catch (error) {
            console.error('Error fetching wellness plan:', error);
            planOutput.innerHTML = `<p style="color: red; text-align: center;">An error occurred while generating your plan. Please check the console and make sure the backend server is running.</p>`;
        } finally {
            // 5. Hide loading state
            loadingSpinner.classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Generate My Plan';
        }
    });

    function renderPlan(plan) {
        if (!plan || !plan.weekPlan) {
            planOutput.innerHTML = `<p style="color: red; text-align: center;">Received an invalid plan structure from the server.</p>`;
            return;
        }

        let html = `<h2>Your 7-Day Wellness Plan</h2>`;
        html += `<p style="text-align: center; margin-bottom: 2rem;"><strong>High-Level Strategy:</strong> ${plan.highLevelStrategy}</p>`;

        plan.weekPlan.forEach(day => {
            html += `
                <h3>${day.day}</h3>
                <ul>
                    <li><strong>Diet:</strong> ${day.diet}</li>
                    <li><strong>Exercise:</strong> ${day.exercise}</li>
                    <li><strong>Rest:</strong> ${day.rest}</li>
                    <li><strong>Nutrition Tip:</strong> ${day.nutrition_tip}</li>
                    <li><strong>De-stress:</strong> ${day.destress_activity}</li>
                    <li><strong>Social:</strong> ${day.social_association}</li>
                </ul>
            `;
        });

        planOutput.innerHTML = html;
    }
});
