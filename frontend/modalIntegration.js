async function openCollegeModal(schoolId) {
    try {
        modal.openModal('<div class="loading">Loading school information...</div>');
        
        const schoolData = await schoolService.getSchoolById(schoolId);
        
        const content = `
            <div class="school-info">
                <div class="school-header">
                    <h3>${schoolData.name || 'Unknown School'}</h3>
                    <div class="school-details-line">
                        ${schoolData.division || 'Division Unknown'} • ${schoolData.conference || 'Conference Unknown'} • ${schoolData.city && schoolData.state ? `${schoolData.city}, ${schoolData.state}` : 'Location Unknown'}
                    </div>
                </div>
                
                <div class="school-details">
                    <div class="info-section">
                        <h4>Athletic Requirements</h4>
                        <div class="info-grid">
                            <div class="info-item">
                                <span class="label">RecruitScore Range:</span>
                                <span class="value">${schoolData.athletic_threshold && schoolData.athletic_maximum ? `${schoolData.athletic_threshold} - ${schoolData.athletic_maximum}` : 'Not specified'}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h4>Academic Requirements</h4>
                        <div class="info-grid">
                            <div class="info-item">
                                <span class="label">GPA Range:</span>
                                <span class="value">${schoolData.gpa_min && schoolData.gpa_max ? `${schoolData.gpa_min} - ${schoolData.gpa_max}` : 'Not specified'}</span>
                            </div>
                            <div class="info-item">
                                <span class="label">SAT Range:</span>
                                <span class="value">${schoolData.sat_min && schoolData.sat_max ? `${schoolData.sat_min} - ${schoolData.sat_max}` : 'Not specified'}</span>
                            </div>
                        </div>
                    </div>
                    
                    ${schoolData.interest_clusters && schoolData.interest_clusters.length > 0 ? `
                    <div class="info-section">
                        <h4>Academic Strengths</h4>
                        <div class="clusters">
                            ${schoolData.interest_clusters.map(cluster => `<span class="cluster-tag">${cluster}</span>`).join('')}
                        </div>
                    </div>
                    ` : ''}
                    
                    ${schoolData.notes ? `
                    <div class="info-section">
                        <h4>Notes</h4>
                        <p>${schoolData.notes}</p>
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
        
        const modalTitle = document.querySelector('.modal-title');
        if (modalTitle) modalTitle.textContent = schoolData.name || 'School Details';
        
        const modalContent = document.querySelector('.modal-content');
        if (modalContent) modalContent.innerHTML = content;

    } catch (error) {
        const errorContent = `
            <div class="error">
                <h4>Unable to load school information</h4>
                <p>Error: ${error.message}</p>
                <p>Please try again later.</p>
            </div>
        `;
        const modalContent = document.querySelector('.modal-content');
        if (modalContent) modalContent.innerHTML = errorContent;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', (e) => {
        const collegeLink = e.target.closest('.college-item a[data-id]');
        if (collegeLink) {
            e.preventDefault();
            const schoolId = parseInt(collegeLink.dataset.id);
            if (schoolId && schoolId > 0) {
                openCollegeModal(schoolId);
            }
        }
    });
});