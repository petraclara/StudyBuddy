document.addEventListener('DOMContentLoaded', () => {
    const addExamBtn = document.getElementById('addExamBtn');
    const examList = document.getElementById('examList');
    const generateBtn = document.getElementById('generateBtn');
    const resultsArea = document.getElementById('resultsArea');
    const loading = document.getElementById('loading');
    const planContent = document.getElementById('planContent');

    let examCount = 1;

    addExamBtn.addEventListener('click', () => {
        const div = document.createElement('div');
        div.className = 'exam-item';
        div.id = `exam-${examCount}`;
        div.innerHTML = `
            <div class="input-group">
                <label>Subject</label>
                <input type="text" class="subject-input" placeholder="e.g. History">
            </div>
            <div class="input-group">
                <label>Exam Date</label>
                <input type="date" class="date-input">
            </div>
            <div class="input-group">
                <label>Confidence (1-5)</label>
                <input type="range" class="confidence-input" min="1" max="5" value="3" oninput="this.nextElementSibling.value = this.value">
                <output>3</output>
            </div>
        `;
        examList.appendChild(div);
        examCount++;
        
        // Scroll to new item
        div.scrollIntoView({ behavior: 'smooth' });
    });

    generateBtn.addEventListener('click', async () => {
        const exams = [];
        const items = document.querySelectorAll('.exam-item');
        
        items.forEach(item => {
            const subject = item.querySelector('.subject-input').value;
            const date = item.querySelector('.date-input').value;
            const confidence = item.querySelector('.confidence-input').value;

            if (subject && date) {
                exams.push({
                    subject,
                    exam_date: date,
                    confidence_level: parseInt(confidence)
                });
            }
        });

        if (exams.length === 0) {
            alert('Please add at least one exam with valid details.');
            return;
        }

        // Show UI state
        resultsArea.classList.remove('hidden');
        loading.classList.remove('hidden');
        planContent.innerHTML = '';
        generateBtn.disabled = true;

        try {
            // Call API
            const response = await fetch('/plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ exams })
            });

            if (!response.ok) {
                throw new Error('Failed to generate plan');
            }

            const data = await response.json();
            renderPlan(data);

        } catch (error) {
            console.error(error);
            planContent.innerHTML = `<p style="color: #ef4444; text-align: center;">Error: ${error.message}. Is the backend running?</p>`;
        } finally {
            loading.classList.add('hidden');
            generateBtn.disabled = false;
        }
    });

    function renderPlan(plan) {
        let html = `
            <div class="plan-header">
                <h3>${plan.plan_name}</h3>
                <p>${plan.advice}</p>
            </div>
        `;

        plan.sessions.forEach(session => {
            html += `
                <div class="session-card">
                    <div class="session-date">${session.date} • ${session.duration_minutes} min</div>
                    <div class="session-subject">${session.subject}</div>
                    <div class="session-topic">${session.topic}</div>
                    <div class="session-advice">💡 ${session.focus_area}</div>
                </div>
            `;
        });

        planContent.innerHTML = html;
        resultsArea.scrollIntoView({ behavior: 'smooth' });
    }
});
