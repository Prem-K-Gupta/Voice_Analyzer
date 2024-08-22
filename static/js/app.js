document.getElementById('start-btn').addEventListener('click', function() {
    const startBtn = document.getElementById('start-btn');
    startBtn.disabled = true;

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;

        fetch('/upload', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ text: text, language: 'en' })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('transcription').innerText = `Transcription: ${data.transcription}`;
            document.getElementById('word-frequency').innerText = `Word Frequency: ${JSON.stringify(data.word_frequency)}`;
            document.getElementById('top-phrases').innerText = `Top 3 Unique Phrases: ${data.top_phrases.join(', ')}`;
        })
        .finally(() => {
            startBtn.disabled = false;
        });
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error detected: ' + event.error);
        startBtn.disabled = false;
    };

    recognition.onspeechend = function() {
        recognition.stop();
    };
});
