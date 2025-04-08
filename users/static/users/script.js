document.getElementById('resumeForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const resumeData = {
        user_id: 1, // Здесь должен быть ID текущего пользователя
        job_title: document.getElementById('jobTitle').value,
        experience: document.getElementById('experience').value,
        education: document.getElementById('education').value,
        skills: document.getElementById('skills').value,
    };

    fetch('http://localhost:3000/create-resume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(resumeData)
    })
    .then(response => response.json())
    .then(data => {
        alert('Резюме успешно сохранено!');
        window.location.href = "resume-result.html";
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
});