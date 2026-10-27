(() => {
    'use strict';
    const $ = (selector, root = document) => root.querySelector(selector);
    const form = $('#scanForm');
    const input = $('#cropImage');
    const zone = $('#uploadZone');
    const preview = $('#imagePreview');
    const status = $('#scanStatus');
    const reportContent = $('#reportContent');
    const emptyReport = $('#emptyReport');
    let currentScanId = 0;
    let lastAnswer = '';

    function setStatus(message, type = 'loading') {
        status.textContent = message;
        status.className = `scan-status show ${type}`;
    }
    function clearStatus() { status.className = 'scan-status'; status.textContent = ''; }
    function showPreview(file) {
        if (!file) return;
        if (!/^image\//.test(file.type)) { setStatus('Please select a valid crop image.', 'error'); return; }
        preview.src = URL.createObjectURL(file);
        zone.classList.add('has-image');
        clearStatus();
    }
    input.addEventListener('change', () => showPreview(input.files[0]));
    ['dragenter', 'dragover'].forEach(name => zone.addEventListener(name, e => { e.preventDefault(); zone.classList.add('dragging'); }));
    ['dragleave', 'drop'].forEach(name => zone.addEventListener(name, e => { e.preventDefault(); zone.classList.remove('dragging'); }));
    zone.addEventListener('drop', e => {
        const file = e.dataTransfer.files[0];
        if (!file) return;
        const dt = new DataTransfer(); dt.items.add(file); input.files = dt.files; showPreview(file);
    });

    function listSection(title, items) {
        if (!Array.isArray(items) || !items.length) return '';
        return `<section class="report-section"><h3>${title}</h3><ul>${items.map(() => '<li></li>').join('')}</ul></section>`;
    }
    function fillList(section, values) {
        if (!section) return;
        section.querySelectorAll('li').forEach((node, i) => { node.textContent = values[i] || ''; });
    }
    function renderReport(report, inspectionDate, scanId) {
        currentScanId = scanId || currentScanId;
        const symptoms = Array.isArray(report.visible_symptoms) ? report.visible_symptoms : [];
        const care = Array.isArray(report.crop_care) ? report.crop_care : [];
        const fertilizer = Array.isArray(report.fertilizer_guidance) ? report.fertilizer_guidance : [];
        const irrigation = Array.isArray(report.irrigation_guidance) ? report.irrigation_guidance : [];
        const prevention = Array.isArray(report.preventive_care) ? report.preventive_care : [];
        const limitations = Array.isArray(report.limitations) ? report.limitations : [];
        const issues = Array.isArray(report.possible_issues) ? report.possible_issues : [];
        const statusName = ['healthy','attention','urgent','uncertain'].includes(report.overall_status) ? report.overall_status : 'uncertain';
        reportContent.innerHTML = `
            <div class="report-head"><div><span class="status-pill status-${statusName}">${statusName}</span><h2 id="reportCrop"></h2><div class="confidence" id="reportConfidence"></div></div><div class="confidence" id="reportStage"></div></div>
            <div class="report-summary" id="reportSummary"></div>
            ${listSection('Visible symptoms', symptoms)}
            <section class="report-section issues-section"><h3>Possible issues</h3><div class="issues-list"></div></section>
            ${listSection('Recommended crop care', care)}
            ${listSection('Fertilizer guidance', fertilizer)}
            ${listSection('Irrigation guidance', irrigation)}
            ${listSection('Preventive care', prevention)}
            <section class="report-section"><h3>Expert guidance & follow-up</h3><ul><li id="expertAdvice"></li><li id="inspectionDate"></li></ul></section>
            ${listSection('Important limitations', limitations)}
            <div class="report-actions"><a id="downloadReport" href="#">Download report</a><button type="button" id="scanAgain">Scan again</button></div>`;
        $('#reportCrop').textContent = report.crop_name || 'Unknown crop';
        $('#reportConfidence').textContent = `Crop identification confidence: ${Number(report.crop_confidence || 0)}%`;
        $('#reportStage').textContent = report.growth_stage || 'Stage not identifiable';
        $('#reportSummary').textContent = report.summary || report.image_quality_note || 'No summary supplied.';
        const sections = reportContent.querySelectorAll('.report-section');
        let listIndex = 0;
        [symptoms].forEach(values => fillList(sections[listIndex++], values));
        const issueList = $('.issues-list', reportContent);
        if (!issues.length) issueList.textContent = 'No issue could be responsibly identified from this image.';
        issues.forEach(issue => {
            const card = document.createElement('div'); card.className = 'issue-card';
            const row = document.createElement('div'); row.className = 'issue-row';
            const name = document.createElement('span'); name.textContent = issue.name || 'Possible issue';
            const confidence = document.createElement('span'); confidence.textContent = `${Number(issue.confidence || 0)}% confidence`;
            row.append(name, confidence); card.append(row);
            const evidence = document.createElement('p'); evidence.textContent = `Visible evidence: ${issue.evidence || 'Not specified'}`; card.append(evidence);
            const causes = document.createElement('p'); causes.textContent = `Possible causes: ${issue.causes || 'Not established'}`; card.append(causes);
            issueList.append(card);
        });
        listIndex++;
        [care, fertilizer, irrigation, prevention].forEach(values => fillList(sections[listIndex++], values));
        $('#expertAdvice').textContent = report.expert_advice || 'Seek local expert advice if symptoms spread or worsen.';
        $('#inspectionDate').textContent = `Suggested next inspection: ${inspectionDate || 'within the advised interval'}`;
        listIndex++;
        fillList(sections[listIndex], limitations);
        $('#downloadReport').href = `/api/crop-doctor/scans/${currentScanId}/download`;
        $('#scanAgain').addEventListener('click', () => { form.reset(); zone.classList.remove('has-image'); preview.removeAttribute('src'); form.scrollIntoView({behavior:'smooth'}); });
        emptyReport.hidden = true; reportContent.hidden = false;
    }

    form.addEventListener('submit', async e => {
        e.preventDefault();
        if (!input.files[0]) { setStatus('Take or upload a crop photo first.', 'error'); return; }
        const button = $('.analyze-btn', form); button.disabled = true;
        let dots = 0; setStatus('Securely uploading and analyzing the visible crop symptoms…');
        const ticker = setInterval(() => { dots = (dots + 1) % 4; status.textContent = `Analyzing image and field context${'.'.repeat(dots)}`; }, 650);
        try {
            const response = await fetch('/api/crop-doctor/analyze', {method:'POST', body:new FormData(form)});
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Analysis could not be completed.');
            renderReport(data.report, data.next_inspection_date, data.scan_id);
            setStatus('Analysis complete. Review the uncertainty notes before taking action.', 'loading');
            window.setTimeout(clearStatus, 5000);
        } catch (error) { setStatus(error.message, 'error'); }
        finally { clearInterval(ticker); button.disabled = !window.CROP_DOCTOR_CONFIG.aiConfigured; }
    });

    document.addEventListener('click', async e => {
        const button = e.target.closest('.view-scan'); if (!button) return;
        const card = button.closest('[data-scan-id]'); const id = card.dataset.scanId;
        button.disabled = true; button.textContent = 'Loading…';
        try {
            const response = await fetch(`/api/crop-doctor/scans/${id}`); const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Report unavailable.');
            renderReport(data.report, data.next_inspection_date, data.id); $('#reportPanel').scrollIntoView({behavior:'smooth'});
        } catch (error) { setStatus(error.message, 'error'); }
        finally { button.disabled = false; button.textContent = 'View report'; }
    });

    $('#chatForm').addEventListener('submit', async e => {
        e.preventDefault(); const field = $('#chatInput'); const question = field.value.trim(); if (!question) return;
        const messages = $('#chatMessages');
        const user = document.createElement('div'); user.className = 'chat-bubble user'; user.textContent = question; messages.append(user); field.value = '';
        const waiting = document.createElement('div'); waiting.className = 'chat-bubble assistant'; waiting.textContent = 'Checking the available crop context…'; messages.append(waiting); messages.scrollTop = messages.scrollHeight;
        try {
            const response = await fetch('/api/crop-doctor/chat', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question,language:$('#chatLanguage').value,scan_id:currentScanId})});
            const data = await response.json(); if (!response.ok) throw new Error(data.error || 'Assistant unavailable.');
            lastAnswer = data.answer || ''; waiting.textContent = lastAnswer; $('#speakAnswer').disabled = !lastAnswer;
        } catch (error) { waiting.textContent = error.message; }
        messages.scrollTop = messages.scrollHeight;
    });
    $('#speakAnswer').addEventListener('click', () => {
        if (!lastAnswer || !('speechSynthesis' in window)) return;
        speechSynthesis.cancel(); const utterance = new SpeechSynthesisUtterance(lastAnswer);
        utterance.lang = {en:'en-IN',hi:'hi-IN',mr:'mr-IN'}[$('#chatLanguage').value] || 'en-IN'; speechSynthesis.speak(utterance);
    });
})();
