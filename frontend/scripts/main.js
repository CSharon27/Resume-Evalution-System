// HireLens - Main JavaScript

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// State
let uploadedFile = null;
let currentEvaluation = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    setupSmoothScrolling();
    initMobileMenu();
    initScrollReveal();
    addPageTransition();
});

// Event Listeners
function setupEventListeners() {
    // File upload
    const resumeFile = document.getElementById('resumeFile');
    const uploadBox = document.getElementById('uploadBox');

    if (resumeFile) {
        resumeFile.addEventListener('change', handleFileSelect);
    }

    // Click to upload
    if (uploadBox && resumeFile) {
        uploadBox.addEventListener('click', () => {
            resumeFile.click();
        });
    }

    // Drag and drop
    if (uploadBox) {
        uploadBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadBox.classList.add('dragover');
        });

        uploadBox.addEventListener('dragleave', () => {
            uploadBox.classList.remove('dragover');
        });

        uploadBox.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadBox.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                resumeFile.files = files;
                handleFileSelect({ target: { files } });
            }
        });
    }

    // Batch file upload
    const batchFiles = document.getElementById('batchFiles');
    if (batchFiles) {
        batchFiles.addEventListener('change', handleBatchFilesSelect);
    }
}

// Smooth scrolling
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });

                // Update active nav link
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });
}

// File handling
function handleFileSelect(event) {
    const file = event.target.files[0];

    if (!file) return;

    // Validate file type
    const validTypes = ['.pdf', '.docx', '.doc'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();

    if (!validTypes.includes(fileExt)) {
        showNotification('Please upload a PDF or DOCX file', 'error');
        return;
    }

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showNotification('File size must be less than 10MB', 'error');
        return;
    }

    uploadedFile = file;

    // Show file info
    const fileInfo = document.getElementById('fileInfo');
    if (fileInfo) {
        const fileName = fileInfo.querySelector('.file-name');
        const fileSize = fileInfo.querySelector('.file-size');

        if (fileName) fileName.textContent = file.name;
        if (fileSize) fileSize.textContent = formatFileSize(file.size);

        fileInfo.classList.remove('hidden');
    }

    showNotification('Resume uploaded successfully', 'success');
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function removeFile() {
    uploadedFile = null;
    document.getElementById('resumeFile').value = '';
    document.getElementById('fileInfo').classList.add('hidden');
}

// Batch file handling
function handleBatchFilesSelect(event) {
    const files = Array.from(event.target.files);
    const filesList = document.getElementById('batchFilesList');

    filesList.innerHTML = '';

    files.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'batch-file-item';
        fileItem.innerHTML = `
            <span>${file.name}</span>
            <button class="btn-remove" onclick="removeBatchFile(${index})">×</button>
        `;
        filesList.appendChild(fileItem);
    });
}

// Evaluation
async function evaluateResume() {
    // Validate inputs
    if (!uploadedFile) {
        showNotification('Please upload a resume', 'error');
        return;
    }

    const jobDescription = document.getElementById('jobDescription').value;
    if (!jobDescription.trim()) {
        showNotification('Please enter a job description', 'error');
        return;
    }

    const evaluateBtn = document.getElementById('evaluateBtn');
    const btnText = evaluateBtn.querySelector('.btn-text');
    const btnLoader = evaluateBtn.querySelector('.btn-loader');

    // Show loading state
    evaluateBtn.disabled = true;
    btnText.classList.add('hidden');
    btnLoader.classList.remove('hidden');

    try {
        showNotification('Uploading resume...', 'info');

        // Step 1: Upload resume
        const formData = new FormData();
        formData.append('file', uploadedFile);

        const uploadResponse = await fetch(`${API_BASE_URL}/upload-resume`, {
            method: 'POST',
            body: formData
        });

        if (!uploadResponse.ok) {
            const errorData = await uploadResponse.json();
            console.error('Upload error:', errorData);
            throw new Error(errorData.detail || 'Failed to upload resume');
        }

        const uploadData = await uploadResponse.json();
        console.log('Upload successful:', uploadData);

        showNotification('Analyzing resume...', 'info');

        // Step 2: Evaluate using the file path in uploads directory
        const resumePath = `uploads/${uploadedFile.name}`;
        console.log('Evaluating with path:', resumePath);

        const evaluateResponse = await fetch(`${API_BASE_URL}/evaluate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_file_path: resumePath,
                job_description: jobDescription
            })
        });

        if (!evaluateResponse.ok) {
            const errorData = await evaluateResponse.json();
            console.error('Evaluation error:', errorData);
            throw new Error(errorData.detail || 'Evaluation failed');
        }

        const evaluationData = await evaluateResponse.json();
        console.log('Evaluation successful:', evaluationData);
        currentEvaluation = evaluationData;

        // Display results
        displayResults(evaluationData);

        // Scroll to results
        setTimeout(() => {
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
        }, 300);

        showNotification('Evaluation complete!', 'success');

    } catch (error) {
        console.error('Full error:', error);
        showNotification(`Error: ${error.message}`, 'error');
    } finally {
        // Reset button state
        evaluateBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}

// Display results
function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.classList.remove('hidden');

    // Score
    displayScore(data.score, data.classification);

    // Skills
    displaySkills(data);

    // Feedback
    displayFeedback(data.feedback);

    // Recommendations
    displayRecommendations(data.recommendations);

    // Roadmap
    displayRoadmap(data.feedback.learning_roadmap);
}

function displayScore(score, classification) {
    // Animate score
    const scoreNumber = document.getElementById('scoreNumber');
    const scoreRing = document.getElementById('scoreRing');
    const scoreClassification = document.getElementById('scoreClassification');
    const scoreDescription = document.getElementById('scoreDescription');

    // Animate number
    animateNumber(scoreNumber, 0, Math.round(score), 1500);

    // Animate ring
    const circumference = 2 * Math.PI * 85;
    const offset = circumference - (score / 100) * circumference;
    scoreRing.style.strokeDashoffset = offset;

    // Add SVG gradient
    if (!document.getElementById('score-gradient')) {
        const svg = document.querySelector('.score-ring');
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        defs.innerHTML = `
            <linearGradient id="score-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#F56565"/>
                <stop offset="100%" stop-color="#C53030"/>
            </linearGradient>
        `;
        svg.insertBefore(defs, svg.firstChild);
    }

    // Classification
    scoreClassification.textContent = `${classification} Match`;
    scoreClassification.className = `classification ${classification.toLowerCase()}`;

    // Description
    const descriptions = {
        'High': 'Excellent match! You possess most of the required skills.',
        'Medium': 'Good potential. Focus on key skill gaps to become a strong candidate.',
        'Low': 'Significant gaps exist. Consider this a long-term career goal.'
    };
    scoreDescription.textContent = descriptions[classification] || '';
}

function displaySkills(data) {
    const matchedSkills = document.getElementById('matchedSkills');
    const missingSkills = document.getElementById('missingSkills');

    // Display matched skills
    matchedSkills.innerHTML = '';
    if (data.matched_skills && data.matched_skills.length > 0) {
        data.matched_skills.forEach(skill => {
            const skillBadge = document.createElement('span');
            skillBadge.className = 'skill-badge matched';
            skillBadge.innerHTML = `<span class="skill-icon">✓</span> ${skill}`;
            matchedSkills.appendChild(skillBadge);
        });
    } else {
        matchedSkills.innerHTML = '<p class="text-muted">No matched skills identified. Consider adding more relevant keywords to your resume.</p>';
    }

    // Display missing skills
    missingSkills.innerHTML = '';
    if (data.skill_gaps && data.skill_gaps.length > 0) {
        data.skill_gaps.forEach(skill => {
            const skillBadge = document.createElement('span');
            skillBadge.className = 'skill-badge missing';
            skillBadge.innerHTML = `<span class="skill-icon">✗</span> ${skill}`;
            missingSkills.appendChild(skillBadge);
        });
    } else {
        missingSkills.innerHTML = '<p class="text-muted">✅ Great! You have all the required skills!</p>';
    }
}

function displayFeedback(feedback) {
    // Strengths
    const strengthsList = document.getElementById('strengthsList');
    strengthsList.innerHTML = '';
    feedback.strengths.forEach(strength => {
        const li = document.createElement('li');
        li.textContent = strength;
        strengthsList.appendChild(li);
    });

    // Weaknesses
    const weaknessesList = document.getElementById('weaknessesList');
    weaknessesList.innerHTML = '';
    feedback.weaknesses.forEach(weakness => {
        const li = document.createElement('li');
        li.textContent = weakness;
        weaknessesList.appendChild(li);
    });
}

function displayRecommendations(recommendations) {
    const coursesList = document.getElementById('coursesList');
    coursesList.innerHTML = '';

    // recommendations is an object like { "Python": [...courses], "Docker": [...courses] }
    Object.entries(recommendations).forEach(([skill, courses]) => {
        courses.slice(0, 2).forEach(course => { // Show max 2 courses per skill
            const courseCard = document.createElement('div');
            courseCard.className = 'course-card';
            courseCard.innerHTML = `
                <div class="course-skill">${skill}</div>
                <h4 class="course-title">${course.title}</h4>
                <div class="course-provider">${course.provider}</div>
                <div class="course-meta">
                    <span>⭐ ${course.rating}</span>
                    <span>⏱️ ${course.duration || 'N/A'}</span>
                    <span>📊 ${course.level || 'All levels'}</span>
                </div>
                <a href="${course.url}" target="_blank" class="course-link">
                    View Course →
                </a>
            `;
            coursesList.appendChild(courseCard);
        });
    });

    if (coursesList.children.length === 0) {
        coursesList.innerHTML = '<p class="text-muted">No course recommendations available</p>';
    }
}

function displayRoadmap(roadmap) {
    // Immediate
    const immediateList = document.getElementById('roadmapImmediate');
    immediateList.innerHTML = '';
    roadmap.immediate.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        immediateList.appendChild(li);
    });

    // Short-term
    const shortTermList = document.getElementById('roadmapShortTerm');
    shortTermList.innerHTML = '';
    roadmap.short_term.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        shortTermList.appendChild(li);
    });

    // Long-term
    const longTermList = document.getElementById('roadmapLongTerm');
    longTermList.innerHTML = '';
    roadmap.long_term.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        longTermList.appendChild(li);
    });
}

// Batch evaluation
async function batchEvaluate() {
    const batchFiles = document.getElementById('batchFiles').files;
    const jobDescription = document.getElementById('batchJobDescription').value;

    if (batchFiles.length === 0) {
        showNotification('Please select resume files', 'error');
        return;
    }

    if (!jobDescription.trim()) {
        showNotification('Please enter a job description', 'error');
        return;
    }

    const btn = document.getElementById('batchEvaluateBtn');
    btn.disabled = true;
    btn.textContent = 'Evaluating...';

    try {
        // Upload all files first
        const filePaths = [];
        const failedUploads = [];

        for (const file of batchFiles) {
            try {
                const formData = new FormData();
                formData.append('file', file);

                const uploadResponse = await fetch(`${API_BASE_URL}/upload-resume`, {
                    method: 'POST',
                    body: formData
                });

                if (uploadResponse.ok) {
                    filePaths.push(file.name);
                } else {
                    console.error(`Failed to upload ${file.name}: ${uploadResponse.status}`);
                    failedUploads.push(file.name);
                }
            } catch (err) {
                console.error(`Error uploading ${file.name}:`, err);
                failedUploads.push(file.name);
            }
        }

        if (failedUploads.length > 0) {
            showNotification(`Failed to upload ${failedUploads.length} files. Proceeding with ${filePaths.length} files.`, 'warning');
        }

        if (filePaths.length === 0) {
            showNotification('All uploads failed. Aborting evaluation.', 'error');
            return;
        }

        // Batch evaluate
        const response = await fetch(`${API_BASE_URL}/batch-evaluate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_file_paths: filePaths,
                job_description: jobDescription
            })
        });

        if (!response.ok) {
            throw new Error('Batch evaluation failed');
        }

        const data = await response.json();

        // Store globally for download
        window.currentBatchResults = data;

        displayBatchResults(data);
        displayBatchDownloadButton();

        showNotification(`Successfully evaluated ${data.total_evaluated} resumes`, 'success');

    } catch (error) {
        console.error('Batch evaluation error:', error);
        showNotification('An error occurred during batch evaluation', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Evaluate All Resumes';
    }
}

function displayBatchDownloadButton() {
    // This function is kept for compatibility but logic is moved to displayBatchResults
}

function displayBatchResults(data) {
    const resultsContainer = document.getElementById('batchResults');
    resultsContainer.classList.remove('hidden');

    resultsContainer.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3>Batch Evaluation Results</h3>
            <button onclick="downloadBatchReport()" class="btn btn-primary" style="background: var(--primary); color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">
                Download PDF Report
            </button>
        </div>
        
        <div class="charts-container" style="display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap;">
            <div class="chart-wrapper" style="flex: 1; min-width: 300px; background: white; padding: 15px; border-radius: 8px; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                <h4 style="text-align: center; margin-bottom: 10px;">Classification Distribution</h4>
                <div style="position: relative; height: 250px;">
                    <canvas id="classificationChart"></canvas>
                </div>
            </div>
            <div class="chart-wrapper" style="flex: 1; min-width: 300px; background: white; padding: 15px; border-radius: 8px; box-shadow: var(--shadow-sm); border: 1px solid var(--border-color);">
                <h4 style="text-align: center; margin-bottom: 10px;">Score Overview</h4>
                <div style="position: relative; height: 250px;">
                    <canvas id="scoreChart"></canvas>
                </div>
            </div>
        </div>

        <p>Total Evaluated: ${data.total_evaluated} | Average Score: ${data.average_score.toFixed(1)}</p>
        <div class="batch-results-table">
            <table id="batchTable" style="width: 100%; border-collapse: collapse; margin-top: 1rem;">
                <thead>
                    <tr style="background: var(--bg-secondary);">
                        <th style="padding: 0.75rem; text-align: left;">#</th>
                        <th style="padding: 0.75rem; text-align: left;">Resume File</th>
                        <th style="padding: 0.75rem; text-align: left;">Score</th>
                        <th style="padding: 0.75rem; text-align: left;">Classification</th>
                        <th style="padding: 0.75rem; text-align: left;">Top Gaps</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.results.map((result, index) => {
        // Always show filename (PDF name)
        const displayName = result.filename || result.evaluation_id || 'Unknown';

        return `
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 0.75rem;">${index + 1}</td>
                            <td style="padding: 0.75rem; font-weight: 500;">${displayName}</td>
                            <td style="padding: 0.75rem;">${result.score.toFixed(1)}</td>
                            <td style="padding: 0.75rem;">
                                <span class="classification ${result.classification.toLowerCase().replace(' ', '-')}" style="font-size: 0.875rem;">
                                    ${result.classification}
                                </span>
                            </td>
                            <td style="padding: 0.75rem;">${Array.isArray(result.skill_gaps) ? result.skill_gaps.slice(0, 3).join(', ') : 'None'}</td>
                        </tr>
                        `;
    }).join('')}
                </tbody>
            </table>
        </div>
    `;

    // Render Charts
    setTimeout(() => {
        renderBatchCharts(data);
    }, 100);
}

function downloadBatchReport() {
    if (!window.currentBatchResults) {
        showNotification('No batch results to download', 'error');
        return;
    }

    try {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        const pageWidth = doc.internal.pageSize.getWidth();

        // Header
        doc.setFillColor(245, 101, 101); // Red theme
        doc.rect(0, 0, pageWidth, 40, 'F');

        doc.setTextColor(255, 255, 255);
        doc.setFontSize(24);
        doc.setFont('helvetica', 'bold');
        doc.text('HireLens Batch Report', 20, 25);

        // Info
        doc.setTextColor(100, 100, 100);
        doc.setFontSize(10);
        doc.text(`Generated: ${new Date().toLocaleString()}`, 20, 50);
        doc.text(`Total Candidates: ${window.currentBatchResults.total_evaluated}`, 20, 55);
        doc.text(`Average Score: ${window.currentBatchResults.average_score.toFixed(1)}`, 20, 60);

        // Table Data - Always use filename (PDF name)
        const tableBody = window.currentBatchResults.results.map((r, i) => [
            i + 1,
            r.filename || r.evaluation_id || 'Unknown',
            r.score.toFixed(1),
            r.classification,
            r.skill_gaps ? r.skill_gaps.slice(0, 3).join(', ') : ''
        ]);

        // AutoTable
        doc.autoTable({
            startY: 70,
            head: [['#', 'Resume File', 'Score', 'Class', 'Missing Skills']],
            body: tableBody,
            headStyles: { fillColor: [245, 101, 101] }, // Red theme
            alternateRowStyles: { fillColor: [255, 245, 245] },
            margin: { top: 70 }
        });

        doc.save(`HireLens_Batch_Report_${Date.now()}.pdf`);
        showNotification('Batch report downloaded!', 'success');

    } catch (err) {
        console.error('PDF Generation Error:', err);
        showNotification('Failed to generate PDF', 'error');
    }
}

// Download results
function downloadResults() {
    if (!currentEvaluation) {
        showNotification('No evaluation results to download', 'error');
        return;
    }

    try {
        // Create new jsPDF instance
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();
        const margin = 20;
        let yPos = 20;

        // Header - Company Branding
        doc.setFillColor(245, 101, 101); // Red theme
        doc.rect(0, 0, pageWidth, 40, 'F');

        doc.setTextColor(255, 255, 255);
        doc.setFontSize(28);
        doc.setFont('helvetica', 'bold');
        doc.text('HireLens', margin, 25);

        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
        doc.text('AI-Powered Resume Evaluation Report', margin, 33);

        yPos = 50;

        // Report Info
        doc.setTextColor(100, 100, 100);
        doc.setFontSize(10);
        doc.text(`Generated: ${new Date().toLocaleString()}`, pageWidth - margin, yPos, { align: 'right' });
        doc.text(`Evaluation ID: ${currentEvaluation.evaluation_id}`, pageWidth - margin, yPos + 5, { align: 'right' });

        yPos += 20;

        // Score Section
        doc.setFillColor(248, 249, 250);
        doc.roundedRect(margin, yPos, pageWidth - 2 * margin, 35, 3, 3, 'F');

        doc.setTextColor(0, 0, 0);
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('Overall Match Score', margin + 10, yPos + 12);

        doc.setFontSize(32);
        const scoreColor = currentEvaluation.score >= 75 ? [72, 187, 120] :
            currentEvaluation.score >= 50 ? [237, 137, 54] : [245, 101, 101];
        doc.setTextColor(...scoreColor);
        doc.text(`${currentEvaluation.score.toFixed(1)}`, margin + 10, yPos + 30);

        doc.setFontSize(12);
        doc.setTextColor(100, 100, 100);
        doc.text('/ 100', margin + 35, yPos + 30);

        const classificationText = currentEvaluation.classification + ' Match';
        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.text(classificationText, pageWidth - margin - 10, yPos + 22, { align: 'right' });

        yPos += 50;

        // Matched Skills Section
        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(72, 187, 120);
        doc.text('Matched Skills', margin, yPos);
        yPos += 8;

        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(60, 60, 60);

        const matchedSkills = currentEvaluation.matched_skills || [];
        if (matchedSkills.length > 0) {
            const skillsText = doc.splitTextToSize(matchedSkills.join(' • '), pageWidth - 2 * margin);
            doc.text(skillsText, margin + 5, yPos);
            yPos += skillsText.length * 5 + 5;
        } else {
            doc.setTextColor(150, 150, 150);
            doc.text('No matched skills identified', margin + 5, yPos);
            yPos += 10;
        }

        // Missing Skills Section
        yPos += 5;
        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(245, 101, 101);
        doc.text('Skills Gap', margin, yPos);
        yPos += 8;

        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(60, 60, 60);

        const missingSkills = currentEvaluation.skill_gaps || [];
        if (missingSkills.length > 0) {
            const missingText = doc.splitTextToSize(missingSkills.join(' • '), pageWidth - 2 * margin);
            doc.text(missingText, margin + 5, yPos);
            yPos += missingText.length * 5 + 5;
        } else {
            doc.setTextColor(72, 187, 120);
            doc.text('Great! You have all the required skills!', margin + 5, yPos);
            yPos += 10;
        }

        // Check if we need a new page
        if (yPos > pageHeight - 60) {
            doc.addPage();
            yPos = 20;
        }

        // Strengths Section
        yPos += 10;
        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(102, 126, 234);
        doc.text('Strengths', margin, yPos);
        yPos += 8;

        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(60, 60, 60);

        const strengths = currentEvaluation.feedback?.strengths || [];
        strengths.slice(0, 5).forEach((strength, index) => {
            if (yPos > pageHeight - 30) {
                doc.addPage();
                yPos = 20;
            }
            const wrappedText = doc.splitTextToSize(`${index + 1}. ${strength}`, pageWidth - 2 * margin - 10);
            doc.text(wrappedText, margin + 5, yPos);
            yPos += wrappedText.length * 5 + 3;
        });

        // Weaknesses Section
        yPos += 7;
        if (yPos > pageHeight - 40) {
            doc.addPage();
            yPos = 20;
        }

        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(237, 137, 54);
        doc.text('Areas for Improvement', margin, yPos);
        yPos += 8;

        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(60, 60, 60);

        const weaknesses = currentEvaluation.feedback?.weaknesses || [];
        weaknesses.slice(0, 5).forEach((weakness, index) => {
            if (yPos > pageHeight - 30) {
                doc.addPage();
                yPos = 20;
            }
            const wrappedText = doc.splitTextToSize(`${index + 1}. ${weakness}`, pageWidth - 2 * margin - 10);
            doc.text(wrappedText, margin + 5, yPos);
            yPos += wrappedText.length * 5 + 3;
        });

        // Course Recommendations (if any)
        const recommendations = currentEvaluation.recommendations || {};
        const recSkills = Object.keys(recommendations);

        if (recSkills.length > 0) {
            if (yPos > pageHeight - 40) {
                doc.addPage();
                yPos = 20;
            }

            yPos += 7;
            doc.setFontSize(14);
            doc.setFont('helvetica', 'bold');
            doc.setTextColor(102, 126, 234);
            doc.text('Recommended Courses', margin, yPos);
            yPos += 10;

            doc.setFontSize(10);
            doc.setFont('helvetica', 'normal');

            recSkills.slice(0, 3).forEach(skill => {
                if (yPos > pageHeight - 40) {
                    doc.addPage();
                    yPos = 20;
                }

                doc.setFont('helvetica', 'bold');
                doc.setTextColor(0, 0, 0);
                doc.text(`${skill}:`, margin + 5, yPos);
                yPos += 6;

                const courses = recommendations[skill].slice(0, 2);
                courses.forEach(course => {
                    if (yPos > pageHeight - 30) {
                        doc.addPage();
                        yPos = 20;
                    }

                    doc.setFont('helvetica', 'normal');
                    doc.setTextColor(60, 60, 60);
                    const courseText = `  • ${course.title} (${course.provider}) - ${course.level}`;
                    const wrappedCourse = doc.splitTextToSize(courseText, pageWidth - 2 * margin - 10);
                    doc.text(wrappedCourse, margin + 7, yPos);
                    yPos += wrappedCourse.length * 5 + 2;
                });

                yPos += 3;
            });
        }

        // Footer
        const totalPages = doc.internal.getNumberOfPages();
        for (let i = 1; i <= totalPages; i++) {
            doc.setPage(i);
            doc.setFontSize(8);
            doc.setTextColor(150, 150, 150);
            doc.setFont('helvetica', 'normal');
            doc.text(
                `HireLens Evaluation Report | Page ${i} of ${totalPages} | Confidential`,
                pageWidth / 2,
                pageHeight - 10,
                { align: 'center' }
            );
        }

        // Download the PDF
        const fileName = `HireLens_Report_${new Date().toISOString().split('T')[0]}.pdf`;
        doc.save(fileName);

        showNotification('PDF report downloaded successfully!', 'success');
    } catch (error) {
        console.error('Error generating PDF:', error);
        showNotification('Error generating PDF report. Please try again.', 'error');
    }
}

// Utilities
function animateNumber(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            element.textContent = Math.round(end);
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, 16);
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? 'var(--success)' : type === 'error' ? 'var(--error)' : 'var(--info)'};
        color: white;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animations to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

async function loadAllCourses() {
    const container = document.getElementById('allCoursesContainer');
    if (!container) return; // Not on courses page

    try {
        const response = await fetch(`${API_BASE_URL}/courses`);
        if (!response.ok) throw new Error('Failed to fetch courses');
        const coursesData = await response.json();

        container.innerHTML = '';

        // Iterate over categories
        Object.entries(coursesData).forEach(([category, courses]) => {
            if (courses.length === 0) return;

            const section = document.createElement('div');
            section.className = 'course-category-section';

            section.innerHTML = `
                <h2 class="category-title">${category}</h2>
                <div class="full-courses-grid">
                    ${courses.map(course => `
                        <div class="course-card">
                            <h4 class="course-title">${course.title}</h4>
                            <div class="course-provider">${course.provider}</div>
                            <div class="course-meta">
                                <span>⭐ ${course.rating}</span>
                                <span>⏱️ ${course.duration || 'N/A'}</span>
                                <span>📊 ${course.level || 'All levels'}</span>
                            </div>
                            <div style="margin-top: 15px;">
                                <a href="${course.url}" target="_blank" class="course-link">View Course →</a>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
            container.appendChild(section);
        });

    } catch (err) {
        console.error(err);
        container.innerHTML = `<p style="color: var(--error); text-align: center;">Failed to load courses. Please try again later.</p>`;
    }
}

function renderBatchCharts(data) {
    if (window.batchCharts) {
        window.batchCharts.forEach(chart => chart.destroy());
    }
    window.batchCharts = [];

    // Data prep
    const classifications = {};
    const scores = data.results.map(r => r.score);

    data.results.forEach(r => {
        classifications[r.classification] = (classifications[r.classification] || 0) + 1;
    });

    // 1. Classification Pie Chart
    const ctxPie = document.getElementById('classificationChart');
    if (ctxPie) {
        const colors = {
            'High Match': '#48BB78',
            'Medium Match': '#ECC94B',
            'Low Match': '#ED8936',
            'Not Fit': '#F56565'
        };
        const bgColors = Object.keys(classifications).map(k => colors[k] || '#CBD5E0');

        const pieChart = new Chart(ctxPie, {
            type: 'pie',
            data: {
                labels: Object.keys(classifications),
                datasets: [{
                    data: Object.values(classifications),
                    backgroundColor: bgColors
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
        window.batchCharts.push(pieChart);
    }

    // 2. Score Bar Chart (Buckets)
    const ctxBar = document.getElementById('scoreChart');
    if (ctxBar) {
        // Create buckets
        const buckets = ['0-20', '21-40', '41-60', '61-80', '81-100'];
        const bucketCounts = [0, 0, 0, 0, 0];

        scores.forEach(score => {
            if (score <= 20) bucketCounts[0]++;
            else if (score <= 40) bucketCounts[1]++;
            else if (score <= 60) bucketCounts[2]++;
            else if (score <= 80) bucketCounts[3]++;
            else bucketCounts[4]++;
        });

        const barChart = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: buckets,
                datasets: [{
                    label: 'Number of Candidates',
                    data: bucketCounts,
                    backgroundColor: '#FC8181', // Red 400
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
        window.batchCharts.push(barChart);
    }
}

// Uploads management
async function loadUploadedFiles() {
    const tableBody = document.getElementById('filesTableBody');
    if (!tableBody) return;

    const noFilesMsg = document.getElementById('noFilesMessage');
    const loadingDiv = document.getElementById('loadingFiles');

    tableBody.innerHTML = '';
    noFilesMsg.classList.add('hidden');
    loadingDiv.classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE_URL}/uploads`);
        if (!response.ok) throw new Error('Failed to fetch files');
        const files = await response.json();

        loadingDiv.classList.add('hidden');

        if (files.length === 0) {
            noFilesMsg.classList.remove('hidden');
            return;
        }

        files.forEach(file => {
            const row = document.createElement('tr');
            row.style.borderBottom = '1px solid var(--border-color)';

            const sizeMB = (file.size / (1024 * 1024)).toFixed(2) + ' MB';
            const date = new Date(file.modified * 1000).toLocaleString();

            row.innerHTML = `
                <td style="padding: 12px 16px;">${file.filename}</td>
                <td style="padding: 12px 16px;">${sizeMB}</td>
                <td style="padding: 12px 16px;">${date}</td>
                <td style="padding: 12px 16px; text-align: right;">
                    <button class="btn-delete" onclick="deleteFile('${file.filename}')">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });

    } catch (err) {
        console.error(err);
        loadingDiv.classList.add('hidden');
        showNotification('Failed to load files', 'error');
    }
}

async function deleteFile(filename) {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) return;

    try {
        const response = await fetch(`${API_BASE_URL}/uploads/${filename}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete file');

        showNotification('File deleted successfully', 'success');
        loadUploadedFiles(); // Refresh
    } catch (err) {
        console.error(err);
        showNotification('Failed to delete file', 'error');
    }
}

// Mobile Menu Toggle
function initMobileMenu() {
    // Create mobile menu toggle button if it doesn't exist
    const navContainer = document.querySelector('.nav-container');
    if (!navContainer) return;

    let menuToggle = document.querySelector('.mobile-menu-toggle');
    if (!menuToggle) {
        menuToggle = document.createElement('button');
        menuToggle.className = 'mobile-menu-toggle';
        menuToggle.innerHTML = '<span></span><span></span><span></span>';
        menuToggle.setAttribute('aria-label', 'Toggle menu');
        navContainer.appendChild(menuToggle);
    }

    const navLinks = document.querySelector('.nav-links');

    menuToggle.addEventListener('click', () => {
        menuToggle.classList.toggle('active');
        navLinks.classList.toggle('active');
        document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
    });

    // Close menu when clicking a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            menuToggle.classList.remove('active');
            navLinks.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navLinks.contains(e.target) && !menuToggle.contains(e.target)) {
            menuToggle.classList.remove('active');
            navLinks.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

// Scroll Reveal Animation
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.feature-card, .process-step, .result-card, .course-card');

    const revealOnScroll = () => {
        revealElements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            if (elementTop < windowHeight - 100) {
                el.classList.add('scroll-reveal', 'active');
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Check on load
}

// Page Transition
function addPageTransition() {
    const mainContent = document.querySelector('.container, .hero');
    if (mainContent) {
        mainContent.classList.add('page-transition');
    }
}

// Enhanced Notification with Slide Animation
const originalShowNotification = showNotification;
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? 'var(--success)' : type === 'error' ? 'var(--error)' : 'var(--info)'};
        color: white;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        max-width: 350px;
    `;

    const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';
    notification.innerHTML = `<span style="font-size: 1.2rem;">${icon}</span><span>${message}</span>`;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}
