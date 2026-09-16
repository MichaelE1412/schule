function showHints(taskId) {
    // Verstecke alle Aufgabeninhalte. Damit bleiben die Hinweise nicht offen.
    document.querySelectorAll('.task').forEach(task => task.style.display = 'none');
    // Setze alle Hinweise zurück
    document.querySelectorAll('.hint').forEach(hint => hint.classList.remove('visible'));
    // Zeige die gewählte Aufgabe an
    document.getElementById(taskId).style.display = 'block';
}

function showNextHint(taskId) {
    const hints = document.querySelectorAll(`#${taskId} .hint`);
    for (let i = 0; i < hints.length; i++) {
        if (!hints[i].classList.contains('visible')) {
            hints[i].classList.add('visible');
            break;
        }
    }
}
