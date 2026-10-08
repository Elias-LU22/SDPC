/**
 * voice_intercom.js - Motor de voz e intercomunicador para simulador Puerta a Puerta de TXU Energy
 * Implementa Web Speech API (STT + TTS) y Web Audio API para timbre residencial sin dependencias externas.
 */

const VoiceIntercom = (function() {
    let audioCtx = null;
    let recognition = null;
    let isListening = false;
    let isSpeaking = false;
    let silenceTimer = null;
    let resumeListeningTimer = null;
    let activeUtterance = null;
    let currentAudioElement = null;
    let sharedAudio = null;
    let isAudioUnlocked = false;
    let ttsAbortController = null;
    let lastSpokenText = '';
    let isHandsFree = true;
    let isMuted = false;
    let currentGender = 'M';
    let availableVoices = [];

    const FEMALE_NAMES = [
        'Carmen Morales',
        'Patricia Ortiz',
        'Andrea Salazar',
        'Beatriz Luna',
        'Elena Ramos',
        'Valeria Ríos',
        'Marcela Beltrán',
        'Laura Cárdenas',
        'Gloria Hinojosa',
        'Verónica Trejo'
    ];

    // Instancia única y compartida de audio para evitar bloqueos de autoplay en móviles
    function getSharedAudio() {
        if (!sharedAudio) {
            sharedAudio = new Audio();
            sharedAudio.preload = 'auto';
        }
        return sharedAudio;
    }

    // Inicializar AudioContext de forma perezosa tras el primer gesto del usuario
    function getAudioContext() {
        if (!audioCtx) {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            if (AudioContextClass) {
                audioCtx = new AudioContextClass();
            }
        }
        if (audioCtx && audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
        return audioCtx;
    }

    // Desbloqueo seguro de audio en navegadores móviles (iOS Safari / Android Chrome)
    function unlockAudio() {
        if (isAudioUnlocked) return;
        try {
            const ctx = getAudioContext();
            if (ctx && ctx.state === 'suspended') {
                ctx.resume();
            }
        } catch (e) {}

        try {
            const audio = getSharedAudio();
            // Data URI de 1 muestra de audio silencioso para registrar la autorización del usuario
            audio.src = 'data:audio/wav;base64,UklGRigAAABXQVZFZm10IBIAAAABAAEARKwAAIhYAQACABAAAABkYXRhAgAAAAEA';
            const playPromise = audio.play();
            if (playPromise !== undefined) {
                playPromise.then(() => {
                    audio.pause();
                    audio.currentTime = 0;
                    isAudioUnlocked = true;
                }).catch(() => {});
            }
        } catch (e) {}

        if ('speechSynthesis' in window) {
            try {
                window.speechSynthesis.resume();
            } catch (e) {}
        }
    }

    // Escuchar el primer gesto en la pantalla para activar el subsistema de audio móvil
    ['click', 'touchstart', 'touchend', 'keydown'].forEach(evtName => {
        document.addEventListener(evtName, unlockAudio, { passive: true });
    });

    // Detener cualquier audio activo (HTML5 Audio, fetch de TTS o SpeechSynthesis)
    function stopActiveAudio() {
        if (ttsAbortController) {
            try { ttsAbortController.abort(); } catch (e) {}
            ttsAbortController = null;
        }
        if (sharedAudio) {
            try {
                sharedAudio.pause();
                sharedAudio.currentTime = 0;
                sharedAudio.removeAttribute('src');
                sharedAudio.load();
            } catch (e) {}
        }
        if (currentAudioElement && currentAudioElement !== sharedAudio) {
            try {
                currentAudioElement.pause();
                currentAudioElement.currentTime = 0;
                currentAudioElement.removeAttribute('src');
                currentAudioElement.load();
            } catch (e) {}
        }
        currentAudioElement = null;

        if ('speechSynthesis' in window) {
            try {
                window.speechSynthesis.cancel();
            } catch (e) {}
        }
        activeUtterance = null;
        window._activeUtterance = null;
        isSpeaking = false;
    }

    function isResidentSpeaking() {
        return isSpeaking || currentAudioElement !== null || (window.speechSynthesis && window.speechSynthesis.speaking);
    }

    // Efecto de timbre acústico residencial (Web Audio API sintético: Mi5 + Do5)
    function playDoorbell() {
        try {
            const ctx = getAudioContext();
            if (!ctx) return;

            const now = ctx.currentTime;
            
            // Primer tono (Ding - 659.25 Hz / E5)
            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(659.25, now);
            gain1.gain.setValueAtTime(0, now);
            gain1.gain.linearRampToValueAtTime(0.28, now + 0.04);
            gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.65);
            osc1.connect(gain1);
            gain1.connect(ctx.destination);
            osc1.start(now);
            osc1.stop(now + 0.65);

            // Segundo tono (Dong - 523.25 Hz / C5)
            const osc2 = ctx.createOscillator();
            const gain2 = ctx.createGain();
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(523.25, now + 0.32);
            gain2.gain.setValueAtTime(0, now + 0.32);
            gain2.gain.linearRampToValueAtTime(0.32, now + 0.36);
            gain2.gain.exponentialRampToValueAtTime(0.001, now + 1.25);
            osc2.connect(gain2);
            gain2.connect(ctx.destination);
            osc2.start(now + 0.32);
            osc2.stop(now + 1.25);

            updateStatusBadge('Timbre sonando...', 'teal');
        } catch (e) {
            console.warn('[VoiceIntercom] Web Audio no disponible:', e);
        }
    }

    // Efecto de audio para abordaje en tienda retail (Web Audio API: Fa5 698.46 Hz + La5 880 Hz)
    function playStoreChime() {
        try {
            const ctx = getAudioContext();
            if (!ctx) return;

            const now = ctx.currentTime;
            
            // Primer tono (Fa5 - 698.46 Hz)
            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = 'triangle';
            osc1.frequency.setValueAtTime(698.46, now);
            gain1.gain.setValueAtTime(0, now);
            gain1.gain.linearRampToValueAtTime(0.24, now + 0.03);
            gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
            osc1.connect(gain1);
            gain1.connect(ctx.destination);
            osc1.start(now);
            osc1.stop(now + 0.55);

            // Segundo tono (La5 - 880 Hz)
            const osc2 = ctx.createOscillator();
            const gain2 = ctx.createGain();
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(880.0, now + 0.22);
            gain2.gain.setValueAtTime(0, now + 0.22);
            gain2.gain.linearRampToValueAtTime(0.28, now + 0.26);
            gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.95);
            osc2.connect(gain2);
            gain2.connect(ctx.destination);
            osc2.start(now + 0.22);
            osc2.stop(now + 0.95);

            updateStatusBadge('Abordando comprador en tienda...', 'teal');
        } catch (e) {
            console.warn('[VoiceIntercom] Web Audio tienda no disponible:', e);
        }
    }


    // Cargar voces del sintetizador del navegador
    function loadVoices() {
        if ('speechSynthesis' in window) {
            availableVoices = window.speechSynthesis.getVoices();
        }
    }

    if ('speechSynthesis' in window) {
        loadVoices();
        window.speechSynthesis.onvoiceschanged = loadVoices;
    }

    // Obtener género del residente actual desde el DOM o por catálogo
    function getResidentGender(overrideGender) {
        if (overrideGender && (overrideGender === 'F' || overrideGender === 'M')) {
            return overrideGender;
        }

        const chatCard = document.getElementById('chat-card');
        if (chatCard) {
            const cardGender = chatCard.dataset.gender;
            if (cardGender && (cardGender === 'F' || cardGender === 'M')) {
                return cardGender;
            }

            const residentName = (chatCard.dataset.resident || '').trim();
            if (FEMALE_NAMES.includes(residentName)) {
                return 'F';
            }
            if (residentName) {
                return 'M';
            }
        }

        return currentGender || 'M';
    }

    function isNeuralVoice(voice) {
        const name = (voice.name || '').toLowerCase();
        return name.includes('natural') || name.includes('neural') || name.includes('online') || name.includes('google') || name.includes('enhanced');
    }

    function getAppLanguage() {
        const card = document.getElementById('chat-card');
        if (card && card.getAttribute('data-lang')) {
            return card.getAttribute('data-lang').toLowerCase().startsWith('en') ? 'en' : 'es';
        }
        const container = document.getElementById('chat-container');
        if (container && container.getAttribute('data-lang')) {
            return container.getAttribute('data-lang').toLowerCase().startsWith('en') ? 'en' : 'es';
        }
        const htmlLang = (document.documentElement.lang || 'es').toLowerCase();
        return htmlLang.startsWith('en') ? 'en' : 'es';
    }

    function getLocalizedStatus(key, isFemale) {
        const lang = getAppLanguage();
        if (lang === 'en') {
            const role = isFemale ? 'Customer (Female Voice)' : 'Customer (Male Voice)';
            switch (key) {
                case 'preparing': return `${role} preparing audio...`;
                case 'speaking': return `${role} speaking...`;
                case 'listening': return 'Listening to you (Speak now)...';
                case 'ready': return 'Ready to speak (Your turn)...';
                case 'sending': return 'Sending proposal to Gemini...';
                case 'mic_paused': return 'Microphone paused';
                case 'voice_muted': return 'Voice Muted';
                case 'voice_active': return 'Voice Active';
                default: return '';
            }
        } else {
            const role = isFemale ? 'Residente (Voz Femenina)' : 'Residente (Voz Masculina)';
            switch (key) {
                case 'preparing': return `${role} preparando audio...`;
                case 'speaking': return `${role} hablando...`;
                case 'listening': return 'Escuchándote (Hable ahora)...';
                case 'ready': return 'Listo para hablar (Tu turno)...';
                case 'sending': return 'Enviando propuesta a Gemini...';
                case 'mic_paused': return 'Micrófono en pausa';
                case 'voice_muted': return 'Voz Silenciada';
                case 'voice_active': return 'Voz Activa';
                default: return '';
            }
        }
    }

    // Seleccionar voz acorde al idioma y género del prospecto, priorizando motores neuronales
    function selectVoice(gender) {
        if (!availableVoices || availableVoices.length === 0) {
            loadVoices();
        }

        const lang = getAppLanguage();
        const isEnglish = (lang === 'en');
        const langVoices = (availableVoices || []).filter(v => {
            if (!v.lang) return false;
            return isEnglish
                ? (v.lang.startsWith('en') || v.lang.includes('EN'))
                : (v.lang.startsWith('es') || v.lang.includes('ES'));
        });

        if (langVoices.length === 0) {
            return {
                voice: availableVoices && availableVoices.length > 0 ? availableVoices[0] : null,
                isExplicitGender: false
            };
        }

        const isFemale = (gender || '').toUpperCase() === 'F';

        const femaleKeywords = isEnglish ? [
            'female', 'jenny', 'zira', 'samantha', 'aria', 'ava', 'emma', 'olivia', 'victoria', 'karen', 'cathy', 'susan', 'linda'
        ] : [
            'female', 'mujer', 'paulina', 'monica', 'sabina', 'helena', 'laura', 'lucia',
            'elena', 'sofia', 'paloma', 'hilda', 'dalia', 'elvira', 'angela', 'angelica',
            'carmen', 'valeria', 'rosa', 'patricia', 'marta', 'conchita', 'jimena',
            'francisca', 'marina', 'victoria'
        ];

        const maleKeywords = isEnglish ? [
            'male', 'guy', 'david', 'mark', 'george', 'ryan', 'eric', 'brian', 'andrew', 'christopher', 'alex', 'fred'
        ] : [
            'male', 'hombre', 'jorge', 'pablo', 'raul', 'diego', 'enrique', 'carlos',
            'miguel', 'juan', 'alvaro', 'gonzalo', 'alonso', 'alberto', 'pedro',
            'manuel', 'mateo', 'tomas', 'javier', 'david', 'antonio', 'luis',
            'ignacio', 'rodrigo', 'fernando', 'hector', 'sergio'
        ];

        const targetKeywords = isFemale ? femaleKeywords : maleKeywords;
        const targetGenderStr = isFemale ? 'female' : 'male';

        // 1. Buscar voces que coincidan con el género objetivo
        const genderVoices = langVoices.filter(v => {
            const nameLower = (v.name || '').toLowerCase();
            const vGender = (v.gender || '').toLowerCase();
            return vGender === targetGenderStr || targetKeywords.some(kw => nameLower.includes(kw));
        });

        // 2. Prioridad máxima: Voz del género correcto con tecnología Neural / Natural / Online / Google
        const neuralGenderVoice = genderVoices.find(v => isNeuralVoice(v));
        if (neuralGenderVoice) {
            return { voice: neuralGenderVoice, isExplicitGender: true };
        }
        if (genderVoices.length > 0) {
            return { voice: genderVoices[0], isExplicitGender: true };
        }

        // 3. Si no hay del género, buscar cualquier voz neuronal en el idioma
        const anyNeuralVoice = langVoices.find(v => isNeuralVoice(v));
        if (anyNeuralVoice) {
            return { voice: anyNeuralVoice, isExplicitGender: false };
        }

        // 4. Fallback a locale preferente de la región
        const preferredLocale = isEnglish
            ? langVoices.find(v => v.lang === 'en-US')
            : langVoices.find(v => v.lang === 'es-US' || v.lang === 'es-MX');

        return {
            voice: preferredLocale || langVoices[0],
            isExplicitGender: false
        };
    }

    // Respaldo mediante sintetizador del navegador con tonos naturales calibrados (sin distorsión robótica)
    function speakWebSpeechFallback(cleanText, resolvedGender, onFinishCallback) {
        if (!('speechSynthesis' in window)) {
            isSpeaking = false;
            setWaveVisualizer(false, 'idle');
            updateStatusBadge(getLocalizedStatus('ready', false), 'teal');
            if (onFinishCallback) onFinishCallback();
            return;
        }

        const utterance = new SpeechSynthesisUtterance(cleanText);
        const { voice, isExplicitGender } = selectVoice(resolvedGender);
        const lang = getAppLanguage();
        const defaultLocale = lang === 'en' ? 'en-US' : 'es-US';

        if (voice) {
            utterance.voice = voice;
            utterance.lang = voice.lang || defaultLocale;
        } else {
            utterance.lang = defaultLocale;
        }

        const isFemale = (resolvedGender === 'F');

        // Calibración acústica natural: NUNCA usar pitch < 0.90 para evitar artefactos metálicos
        if (isFemale) {
            utterance.pitch = 1.02;
            utterance.rate = 1.0;
        } else {
            utterance.pitch = 0.98;
            utterance.rate = 0.98;
        }

        activeUtterance = utterance;
        window._activeUtterance = utterance;

        utterance.onstart = function() {
            isSpeaking = true;
            setWaveVisualizer(true, 'speaking');
            updateStatusBadge(getLocalizedStatus('speaking', isFemale), 'amber');
        };

        const handleSpeechEnd = function() {
            isSpeaking = false;
            activeUtterance = null;
            window._activeUtterance = null;
            setWaveVisualizer(false, 'idle');
            updateStatusBadge('Listo para hablar (Tu turno)...', 'teal');

            if (onFinishCallback) onFinishCallback();

            if (isHandsFree && !isMuted) {
                clearTimeout(resumeListeningTimer);
                resumeListeningTimer = setTimeout(function() {
                    if (!isResidentSpeaking()) {
                        startListening();
                    }
                }, 850);
            }
        };

        utterance.onend = handleSpeechEnd;
        utterance.onerror = function(err) {
            console.warn('[VoiceIntercom] Error en síntesis fallback:', err);
            handleSpeechEnd();
        };

        setTimeout(() => {
            try {
                if (window.speechSynthesis.paused) {
                    window.speechSynthesis.resume();
                }
                window.speechSynthesis.speak(utterance);
            } catch (e) {
                console.warn('[VoiceIntercom] Excepción en speechSynthesis.speak:', e);
                handleSpeechEnd();
            }
        }, 40);
    }

    // Vocalizar respuesta del residente con audio neuronal de alta fidelidad
    function speak(text, gender = null, force = false, onFinishCallback = null) {
        if (typeof force === 'function') {
            onFinishCallback = force;
            force = false;
        }

        const resolvedGender = getResidentGender(gender);
        currentGender = resolvedGender;

        clearTimeout(resumeListeningTimer);
        clearTimeout(silenceTimer);

        if (isMuted) {
            updateStatusBadge('Voz silenciada (Modo texto)', 'slate');
            if (isHandsFree) {
                resumeListeningTimer = setTimeout(startListening, 600);
            }
            if (onFinishCallback) onFinishCallback();
            return;
        }

        // Limpiar texto de acotaciones entre corchetes [Abre la puerta] y marcas de formato
        const cleanText = text.replace(/\[.*?\]/g, '').replace(/[*_#`~]/g, '').trim();
        if (!cleanText) {
            isSpeaking = false;
            return;
        }

        // Prevenir duplicación si es exactamente el mismo texto ya procesado
        if (!force && cleanText === lastSpokenText) {
            console.log('[VoiceIntercom] Mensaje ya vocalizado o en proceso, omitiendo duplicado.');
            return;
        }
        lastSpokenText = cleanText;

        isSpeaking = true;
        stopListening(true);
        stopActiveAudio();

        const isFemale = (resolvedGender === 'F');

        // Desbloquear audio si es posible
        unlockAudio();

        const lang = getAppLanguage();
        // 1. Obtener audio neuronal MP3 desde Django (/tts/) mediante fetch()
        // Esto previene bloqueos por 204 No Content y evita colisiones de dos fuentes de audio simultáneas
        const ttsUrl = `/tts/?gender=${encodeURIComponent(resolvedGender)}&text=${encodeURIComponent(cleanText)}&lang=${encodeURIComponent(lang)}`;

        ttsAbortController = new AbortController();
        const signal = ttsAbortController.signal;

        updateStatusBadge(getLocalizedStatus('preparing', isFemale), 'amber');

        fetch(ttsUrl, { signal })
            .then(async response => {
                if (!response.ok || response.status === 204) {
                    throw new Error('TTS_FALLBACK_STATUS_' + response.status);
                }
                const blob = await response.blob();
                if (!blob || blob.size < 64) {
                    throw new Error('TTS_EMPTY_PAYLOAD');
                }
                const blobUrl = URL.createObjectURL(blob);
                playBlobAudio(blobUrl, cleanText, resolvedGender, onFinishCallback);
            })
            .catch(err => {
                if (err.name === 'AbortError') {
                    return; // Cancelado explícitamente
                }
                console.warn('[VoiceIntercom] Servidor TTS no disponible o error:', err.message, '- Usando sintetizador local');
                speakWebSpeechFallback(cleanText, resolvedGender, onFinishCallback);
            });
    }

    function playBlobAudio(blobUrl, cleanText, resolvedGender, onFinishCallback) {
        const audio = getSharedAudio();
        currentAudioElement = audio;

        const isFemale = (resolvedGender === 'F');

        const cleanup = function() {
            audio.onplay = null;
            audio.onended = null;
            audio.onerror = null;
            try {
                URL.revokeObjectURL(blobUrl);
            } catch (e) {}
        };

        const handleAudioEnd = function() {
            cleanup();
            isSpeaking = false;
            currentAudioElement = null;
            setWaveVisualizer(false, 'idle');
            updateStatusBadge(getLocalizedStatus('ready', false), 'teal');

            if (onFinishCallback) onFinishCallback();

            if (isHandsFree && !isMuted) {
                clearTimeout(resumeListeningTimer);
                resumeListeningTimer = setTimeout(function() {
                    if (!isResidentSpeaking()) {
                        startListening();
                    }
                }, 850);
            }
        };

        audio.onplay = function() {
            isSpeaking = true;
            setWaveVisualizer(true, 'speaking');
            updateStatusBadge(getLocalizedStatus('speaking', isFemale), 'amber');
        };

        audio.onended = handleAudioEnd;

        audio.onerror = function(err) {
            console.warn('[VoiceIntercom] Error en reproducción de audio blob:', err);
            cleanup();
            currentAudioElement = null;
            speakWebSpeechFallback(cleanText, resolvedGender, onFinishCallback);
        };

        audio.src = blobUrl;
        const playPromise = audio.play();
        if (playPromise !== undefined) {
            playPromise.catch(function(playErr) {
                console.warn('[VoiceIntercom] Reproducción bloqueada por navegador:', playErr);
                cleanup();
                try {
                    audio.pause();
                    audio.removeAttribute('src');
                    audio.load();
                } catch (e) {}
                currentAudioElement = null;
                speakWebSpeechFallback(cleanText, resolvedGender, onFinishCallback);
            });
        }
    }

    // Inicializar SpeechRecognition (STT)
    function initSpeechRecognition() {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) {
            console.warn('[VoiceIntercom] SpeechRecognition no soportado en este navegador');
            updateMicButtonUI(false, false);
            return null;
        }

        const rec = new SpeechRec();
        rec.continuous = true;
        rec.interimResults = true;
        rec.lang = (getAppLanguage() === 'en' ? 'en-US' : 'es-US');

        rec.onstart = function() {
            isListening = true;
            updateMicButtonUI(true, true);
            setWaveVisualizer(true, 'listening');
            updateStatusBadge(getLocalizedStatus('listening', false), 'emerald');
        };

        rec.onresult = function(event) {
            // FILTRO HALF-DUPLEX: Si el sintetizador o audio MP3 está activo,
            // descartar inmediatamente cualquier sonido captado (evita que el micrófono se escuche a sí mismo)
            if (isResidentSpeaking()) {
                return;
            }

            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }

            const inputField = document.getElementById('message-input');
            if (inputField) {
                const currentText = (finalTranscript || interimTranscript).trim();
                if (currentText) {
                    inputField.value = currentText;
                }
            }

            // Reiniciar timer de silencio para auto-envío en Manos Libres
            if (isHandsFree && (finalTranscript || interimTranscript)) {
                clearTimeout(silenceTimer);
                silenceTimer = setTimeout(function() {
                    // Verificar nuevamente que no esté hablando el residente
                    if (isResidentSpeaking()) {
                        return;
                    }

                    const textToSend = (inputField ? inputField.value : '').trim();
                    if (textToSend.length > 2) {
                        stopListening(true);
                        updateStatusBadge(getLocalizedStatus('sending', false), 'teal');
                        submitCurrentMessage();
                    }
                }, 1400); // 1.4s de pausa natural tras hablar
            }
        };

        rec.onerror = function(event) {
            if (event.error !== 'no-speech' && event.error !== 'aborted') {
                console.warn('[VoiceIntercom] Error en reconocimiento:', event.error);
                isListening = false;
                updateMicButtonUI(false, true);
                setWaveVisualizer(false, 'idle');
            }
        };

        rec.onend = function() {
            isListening = false;
            updateMicButtonUI(false, true);
            if (!isSpeaking) {
                setWaveVisualizer(false, 'idle');
            }
        };

        return rec;
    }

    // Comenzar captura de voz
    function startListening() {
        // Si el residente está hablando o reproduciendo audio, NO abrir el micrófono para evitar interrupciones o ecos
        if (isResidentSpeaking()) {
            return;
        }

        clearTimeout(resumeListeningTimer);

        if (!recognition) {
            recognition = initSpeechRecognition();
        }

        if (recognition && !isListening) {
            try {
                recognition.start();
            } catch (e) {
                // Si ya estaba en curso, ignorar error de estado
            }
        }
    }

    // Detener captura de voz (forceAbort descarta buffers activos)
    function stopListening(forceAbort = false) {
        clearTimeout(silenceTimer);
        clearTimeout(resumeListeningTimer);

        if (recognition && isListening) {
            try {
                if (forceAbort && typeof recognition.abort === 'function') {
                    recognition.abort();
                } else {
                    recognition.stop();
                }
            } catch (e) {}
        }

        isListening = false;
        updateMicButtonUI(false, true);
        if (!isSpeaking) {
            setWaveVisualizer(false, 'idle');
        }
    }

    // Alternar estado de escucha manual
    function toggleListening() {
        if (isListening) {
            stopListening(false);
            const inputField = document.getElementById('message-input');
            if (inputField && inputField.value.trim().length > 1) {
                submitCurrentMessage();
            } else {
                updateStatusBadge(getLocalizedStatus('mic_paused', false), 'slate');
            }
        } else {
            // Si el usuario activa el micrófono manualmente mientras el residente habla, interrumpir
            if (isSpeaking || isResidentSpeaking()) {
                stopActiveAudio();
                isSpeaking = false;
            }
            startListening();
        }
    }

    // Enviar el formulario del chat actual a través de HTMX
    function submitCurrentMessage() {
        const form = document.getElementById('message-form');
        if (form) {
            const input = document.getElementById('message-input');
            if (input && input.value.trim()) {
                if (typeof htmx !== 'undefined') {
                    htmx.trigger(form, 'submit');
                } else {
                    form.submit();
                }
            }
        }
    }

    // Actualizar visualizador de ondas sonoras
    function setWaveVisualizer(active, mode) {
        const waveContainer = document.getElementById('voice-wave-container');
        if (!waveContainer) return;

        const bars = waveContainer.querySelectorAll('.wave-bar');
        bars.forEach((bar, idx) => {
            if (active) {
                bar.classList.remove('h-1.5', 'bg-slate-700');
                if (mode === 'speaking') {
                    bar.classList.add('bg-amber-400', 'animate-pulse');
                    bar.style.height = `${Math.min(24, 8 + ((idx % 3) + 1) * 5)}px`;
                } else if (mode === 'listening') {
                    bar.classList.add('bg-teal-400', 'animate-pulse');
                    bar.style.height = `${Math.min(24, 10 + ((idx % 4) + 1) * 4)}px`;
                }
            } else {
                bar.classList.remove('bg-amber-400', 'bg-teal-400', 'animate-pulse');
                bar.classList.add('bg-slate-700', 'h-1.5');
                bar.style.height = '6px';
            }
        });
    }

    // Actualizar indicador de estado en pantalla
    function updateStatusBadge(text, color) {
        const badge = document.getElementById('intercom-status-text');
        const dot = document.getElementById('intercom-status-dot');
        if (badge) badge.textContent = text;
        if (dot) {
            dot.className = 'w-2 h-2 rounded-full transition-colors duration-300';
            if (color === 'emerald') dot.classList.add('bg-emerald-400', 'animate-ping');
            else if (color === 'teal') dot.classList.add('bg-teal-400');
            else if (color === 'amber') dot.classList.add('bg-amber-400', 'animate-pulse');
            else dot.classList.add('bg-slate-500');
        }
    }

    // Actualizar aspecto visual del botón del micrófono
    function updateMicButtonUI(listening, supported) {
        const btn = document.getElementById('voice-mic-btn');
        const iconMic = document.getElementById('icon-mic-normal');
        const iconPulse = document.getElementById('icon-mic-active');
        const isEnglish = (getAppLanguage() === 'en');

        if (!btn) return;

        if (!supported) {
            btn.classList.add('opacity-40', 'cursor-not-allowed');
            btn.title = isEnglish ? 'Speech recognition not supported in this browser' : 'Reconocimiento de voz no soportado en este navegador';
            return;
        }

        if (listening) {
            btn.className = 'w-11 h-11 rounded-2xl bg-rose-500 text-white shadow-lg shadow-rose-900/50 ring-2 ring-rose-400 ring-offset-2 ring-offset-slate-950 flex items-center justify-center flex-shrink-0 transition-all';
            btn.title = isEnglish ? 'Listening to your voice... Click to stop' : 'Escuchando tu voz... Clic para detener';
            if (iconMic) iconMic.classList.add('hidden');
            if (iconPulse) iconPulse.classList.remove('hidden');
        } else {
            btn.className = 'w-11 h-11 rounded-2xl liquid-pill text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white flex items-center justify-center flex-shrink-0 transition-all';
            btn.title = isEnglish ? 'Activate microphone to speak' : 'Activar micrófono para hablar';
            if (iconMic) iconMic.classList.remove('hidden');
            if (iconPulse) iconPulse.classList.add('hidden');
        }
    }

    // Conmutar modo Manos Libres
    function toggleHandsFree() {
        isHandsFree = !isHandsFree;
        const btn = document.getElementById('toggle-handsfree-btn');
        const isEnglish = (getAppLanguage() === 'en');
        if (btn) {
            if (isHandsFree) {
                btn.className = 'liquid-pill px-3 py-1.5 rounded-full text-teal-700 dark:text-teal-300 border-teal-500/30 bg-teal-500/10 dark:bg-teal-950/40 text-xs font-medium';
                btn.textContent = isEnglish ? 'Hands-Free: Active' : 'Manos Libres: Activo';
                updateStatusBadge(isEnglish ? 'Hands-Free Mode On' : 'Modo Manos Libres encendido', 'teal');
            } else {
                btn.className = 'liquid-pill px-3 py-1.5 rounded-full text-slate-500 dark:text-slate-400 border-slate-200 dark:border-white/5 bg-slate-100/50 dark:bg-white/5 text-xs font-medium';
                btn.textContent = isEnglish ? 'Hands-Free: Manual' : 'Manos Libres: Manual';
                updateStatusBadge(isEnglish ? 'Manual Mode (Use mic button)' : 'Modo Manual (Usa el botón de micrófono)', 'slate');
                stopListening(true);
            }
        }
    }

    // Conmutar silencio de audio
    function toggleMute() {
        isMuted = !isMuted;
        const btn = document.getElementById('toggle-mute-btn');
        const isEnglish = (getAppLanguage() === 'en');
        if (btn) {
            if (isMuted) {
                stopActiveAudio();
                isSpeaking = false;
                setWaveVisualizer(false, 'idle');
                btn.className = 'liquid-pill px-3 py-1.5 rounded-full text-rose-700 dark:text-rose-300 border-rose-500/30 bg-rose-500/10 dark:bg-rose-950/40 text-xs font-medium flex items-center gap-1.5';
                btn.innerHTML = `
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2"/>
                    </svg>
                    <span>${isEnglish ? 'Voice Muted' : 'Voz Silenciada'}</span>
                `;
                updateStatusBadge(isEnglish ? 'Voice muted' : 'Voz apagada', 'slate');
            } else {
                btn.className = 'liquid-pill px-3 py-1.5 rounded-full text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition flex items-center gap-1.5 text-xs';
                btn.innerHTML = `
                    <svg class="w-3.5 h-3.5 text-teal-600 dark:text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                    </svg>
                    <span>${isEnglish ? 'Voice Active' : 'Voz Activa'}</span>
                `;
                updateStatusBadge(isEnglish ? 'Voice enabled' : 'Voz habilitada', 'teal');
            }
        }
    }

    // Inicialización al cargar la página por primera vez (evita autohabla indeseada y bloqueos de autoplay)
    function initOnPageLoad() {
        currentGender = getResidentGender();
        const prospectMessages = document.querySelectorAll('.prospect-bubble-text');
        if (prospectMessages.length > 0) {
            const latestMsg = prospectMessages[prospectMessages.length - 1].textContent.trim();
            if (latestMsg) {
                lastSpokenText = latestMsg.replace(/\[.*?\]/g, '').replace(/[*_#`~]/g, '').trim();
            }
        }
    }

    // Disparador cuando HTMX actualiza el chat
    function onChatContentSwapped() {
        const chatCard = document.getElementById('chat-card');
        if (!chatCard) return;

        const lang = getAppLanguage();
        if (document.documentElement.lang !== lang) {
            document.documentElement.lang = lang;
        }
        if (speechRecInstance) {
            speechRecInstance.lang = (lang === 'en' ? 'en-US' : 'es-US');
        }

        currentGender = getResidentGender();

        // Extraer el último mensaje del prospecto
        const prospectMessages = document.querySelectorAll('.prospect-bubble-text');
        if (prospectMessages.length > 0) {
            const latestMsg = prospectMessages[prospectMessages.length - 1].textContent.trim();
            if (latestMsg) {
                // Retardo breve para permitir renderizado fluido del DOM antes de hablar
                setTimeout(() => {
                    speak(latestMsg, currentGender, false);
                }, 150);
            }
        } else {
            // No hay mensajes del prospecto aún (el vendedor está en el pórtico)
            const waitingHook = document.getElementById('porch-waiting-hook');
            if (waitingHook && isHandsFree && !isListening) {
                const isEnglish = (getAppLanguage() === 'en');
                setTimeout(() => {
                    startListening();
                    updateStatusBadge(isEnglish ? 'Microphone active: Deliver your opening hook' : 'Micrófono activo: Presenta tu gancho de apertura', 'emerald');
                }, 400);
            }
        }
    }

    // Iniciar llamada/interacción tocando el timbre de la residencia
    function ringAndStart() {
        unlockAudio();
        playDoorbell();
        currentGender = getResidentGender();
        updateStatusBadge('Timbre sonando...', 'amber');

        // Tras el timbre acústico, activar el micrófono para que el vendedor hable primero
        setTimeout(() => {
            if (!isListening) {
                startListening();
            }
            updateStatusBadge('Micrófono activo: Presenta tu gancho de apertura', 'emerald');
        }, 900);
    }

    // Iniciar abordaje a un comprador en tienda comercial
    function approachAndStart() {
        unlockAudio();
        playStoreChime();
        currentGender = getResidentGender();
        updateStatusBadge('Abordaje iniciado en tienda...', 'amber');

        // Tras el tono de tienda, activar el micrófono para que el vendedor hable primero
        setTimeout(() => {
            if (!isListening) {
                startListening();
            }
            updateStatusBadge('Micrófono activo: Presenta tu gancho de abordaje', 'emerald');
        }, 750);
    }

    return {
        playDoorbell,
        playStoreChime,
        speak,
        startListening,
        stopListening,
        toggleListening,
        toggleHandsFree,
        toggleMute,
        onChatContentSwapped,
        initOnPageLoad,
        ringAndStart,
        approachAndStart,
        selectVoice,
        getResidentGender,
        isHandsFreeMode: () => isHandsFree,
        unlockAudio
    };
})();

