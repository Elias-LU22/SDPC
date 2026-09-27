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
    let isHandsFree = true;
    let isMuted = false;
    let currentGender = 'M';
    let availableVoices = [];

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

    // Seleccionar voz en español acorde al género del prospecto
    function selectVoice(gender) {
        if (!availableVoices || availableVoices.length === 0) {
            loadVoices();
        }
        
        const spanishVoices = availableVoices.filter(v => v.lang && (v.lang.startsWith('es') || v.lang.includes('ES')));
        if (spanishVoices.length === 0) {
            return availableVoices[0] || null;
        }

        const isFemale = (gender || '').toUpperCase() === 'F';
        
        // Criterios de búsqueda por nombre de voz
        const femaleKeywords = ['female', 'paulina', 'monica', 'sabina', 'helena', 'laura', 'lucia', 'elena', 'sofia', 'paloma', 'hilda'];
        const maleKeywords = ['male', 'jorge', 'pablo', 'raul', 'diego', 'enrique', 'carlos', 'miguel', 'juan'];

        if (isFemale) {
            const foundFemale = spanishVoices.find(v => femaleKeywords.some(kw => v.name.toLowerCase().includes(kw)));
            if (foundFemale) return foundFemale;
        } else {
            const foundMale = spanishVoices.find(v => maleKeywords.some(kw => v.name.toLowerCase().includes(kw)));
            if (foundMale) return foundMale;
        }

        // Si no hay específica por género, usar la primera en español de la región
        const preferredLocale = spanishVoices.find(v => v.lang === 'es-US' || v.lang === 'es-MX');
        return preferredLocale || spanishVoices[0];
    }

    // Vocalizar respuesta del residente
    function speak(text, gender = 'M', onFinishCallback = null) {
        if (!('speechSynthesis' in window)) {
            console.warn('[VoiceIntercom] SpeechSynthesis no soportado');
            if (onFinishCallback) onFinishCallback();
            return;
        }

        if (isMuted) {
            updateStatusBadge('Voz silenciada (Modo texto)', 'slate');
            if (isHandsFree) {
                setTimeout(startListening, 600);
            }
            if (onFinishCallback) onFinishCallback();
            return;
        }

        window.speechSynthesis.cancel(); // Detener cualquier locución previa
        stopListening();

        const cleanText = text.replace(/[*_#`]/g, '').trim();
        if (!cleanText) return;

        const utterance = new SpeechSynthesisUtterance(cleanText);
        const voice = selectVoice(gender);
        if (voice) {
            utterance.voice = voice;
            utterance.lang = voice.lang || 'es-US';
        } else {
            utterance.lang = 'es-US';
        }

        utterance.rate = 1.02;
        utterance.pitch = (gender || '').toUpperCase() === 'F' ? 1.08 : 0.95;

        utterance.onstart = function() {
            isSpeaking = true;
            setWaveVisualizer(true, 'speaking');
            updateStatusBadge('Residente hablando...', 'amber');
        };

        utterance.onend = function() {
            isSpeaking = false;
            setWaveVisualizer(false, 'idle');
            updateStatusBadge('Listo para hablar', 'teal');

            if (onFinishCallback) onFinishCallback();
            if (isHandsFree) {
                setTimeout(startListening, 450);
            }
        };

        utterance.onerror = function(err) {
            console.warn('[VoiceIntercom] Error en síntesis:', err);
            isSpeaking = false;
            setWaveVisualizer(false, 'idle');
            updateStatusBadge('Listo', 'slate');
            if (onFinishCallback) onFinishCallback();
            if (isHandsFree) {
                setTimeout(startListening, 500);
            }
        };

        window.speechSynthesis.speak(utterance);
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
        rec.lang = 'es-US';

        rec.onstart = function() {
            isListening = true;
            updateMicButtonUI(true, true);
            setWaveVisualizer(true, 'listening');
            updateStatusBadge('Escuchándote (Hable ahora)...', 'emerald');
        };

        rec.onresult = function(event) {
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
                const currentText = finalTranscript || interimTranscript;
                if (currentText) {
                    inputField.value = currentText;
                }
            }

            // Reiniciar timer de silencio para auto-envío en Manos Libres
            if (isHandsFree && (finalTranscript || interimTranscript)) {
                clearTimeout(silenceTimer);
                silenceTimer = setTimeout(function() {
                    const textToSend = (inputField ? inputField.value : '').trim();
                    if (textToSend.length > 2) {
                        stopListening();
                        updateStatusBadge('Enviando propuesta a Gemini...', 'teal');
                        submitCurrentMessage();
                    }
                }, 1300); // 1.3s de pausa natural tras hablar
            }
        };

        rec.onerror = function(event) {
            console.warn('[VoiceIntercom] Error en reconocimiento:', event.error);
            if (event.error !== 'no-speech') {
                isListening = false;
                updateMicButtonUI(false, true);
                setWaveVisualizer(false, 'idle');
            }
        };

        rec.onend = function() {
            isListening = false;
            updateMicButtonUI(false, true);
            setWaveVisualizer(false, 'idle');
        };

        return rec;
    }

    // Comenzar captura de voz
    function startListening() {
        if (isSpeaking) {
            window.speechSynthesis.cancel();
            isSpeaking = false;
        }

        if (!recognition) {
            recognition = initSpeechRecognition();
        }

        if (recognition && !isListening) {
            try {
                recognition.start();
            } catch (e) {
                // Si ya estaba en curso
            }
        }
    }

    // Detener captura de voz
    function stopListening() {
        clearTimeout(silenceTimer);
        if (recognition && isListening) {
            try {
                recognition.stop();
            } catch (e) {}
        }
        isListening = false;
        updateMicButtonUI(false, true);
        setWaveVisualizer(false, 'idle');
    }

    // Alternar estado de escucha manual
    function toggleListening() {
        if (isListening) {
            stopListening();
            const inputField = document.getElementById('message-input');
            if (inputField && inputField.value.trim().length > 1) {
                submitCurrentMessage();
            } else {
                updateStatusBadge('Micrófono en pausa', 'slate');
            }
        } else {
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

        if (!btn) return;

        if (!supported) {
            btn.classList.add('opacity-40', 'cursor-not-allowed');
            btn.title = 'Reconocimiento de voz no soportado en este navegador';
            return;
        }

        if (listening) {
            btn.className = 'w-11 h-11 rounded-2xl bg-rose-500 text-white shadow-lg shadow-rose-900/50 ring-2 ring-rose-400 ring-offset-2 ring-offset-slate-950 flex items-center justify-center flex-shrink-0 transition-all';
            btn.title = 'Escuchando tu voz... Clic para detener';
            if (iconMic) iconMic.classList.add('hidden');
            if (iconPulse) iconPulse.classList.remove('hidden');
        } else {
            btn.className = 'w-11 h-11 rounded-2xl liquid-pill text-slate-300 hover:text-white flex items-center justify-center flex-shrink-0 transition-all';
            btn.title = 'Activar micrófono para hablar';
            if (iconMic) iconMic.classList.remove('hidden');
            if (iconPulse) iconPulse.classList.add('hidden');
        }
    }

    // Conmutar modo Manos Libres
    function toggleHandsFree() {
        isHandsFree = !isHandsFree;
        const btn = document.getElementById('toggle-handsfree-btn');
        if (btn) {
            if (isHandsFree) {
                btn.className = 'liquid-pill px-3 py-1.5 rounded-full text-teal-300 border-teal-500/30 bg-teal-950/40 text-xs font-medium';
                btn.textContent = 'Manos Libres: Activo';
                updateStatusBadge('Modo Manos Libres encendido', 'teal');
            } else {
                btn.className = 'liquid-pill px-3 py-1.5 rounded-full text-slate-400 border-white/5 bg-white/5 text-xs font-medium';
                btn.textContent = 'Manos Libres: Manual';
                updateStatusBadge('Modo Manual (Usa el botón de micrófono)', 'slate');
                stopListening();
            }
        }
    }

    // Conmutar silencio de audio
    function toggleMute() {
        isMuted = !isMuted;
        const btn = document.getElementById('toggle-mute-btn');
        if (btn) {
            if (isMuted) {
                window.speechSynthesis.cancel();
                isSpeaking = false;
                setWaveVisualizer(false, 'idle');
                btn.className = 'liquid-pill px-3 py-1.5 rounded-full text-rose-300 border-rose-500/30 bg-rose-950/40 text-xs font-medium flex items-center gap-1.5';
                btn.innerHTML = `
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2"/>
                    </svg>
                    <span>Voz Silenciada</span>
                `;
                updateStatusBadge('Voz apagada', 'slate');
            } else {
                btn.className = 'liquid-pill px-3 py-1.5 rounded-full text-slate-300 hover:text-white transition flex items-center gap-1.5 text-xs';
                btn.innerHTML = `
                    <svg class="w-3.5 h-3.5 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                    </svg>
                    <span>Voz Activa</span>
                `;
                updateStatusBadge('Voz habilitada', 'teal');
            }
        }
    }

    // Disparador cuando HTMX actualiza el chat
    function onChatContentSwapped() {
        const chatCard = document.getElementById('chat-card');
        if (!chatCard) return;

        const gender = chatCard.dataset.gender || 'M';
        currentGender = gender;

        // Extraer el último mensaje del prospecto
        const prospectMessages = document.querySelectorAll('.prospect-bubble-text');
        if (prospectMessages.length > 0) {
            const latestMsg = prospectMessages[prospectMessages.length - 1].textContent.trim();
            if (latestMsg) {
                // Pequeño retardo para asegurar renderizado visual
                setTimeout(() => {
                    speak(latestMsg, currentGender);
                }, 150);
            }
        }
    }

    // Iniciar llamada/interacción inicial con timbre
    function ringAndStart() {
        playDoorbell();
        setTimeout(() => {
            const prospectMessages = document.querySelectorAll('.prospect-bubble-text');
            if (prospectMessages.length > 0) {
                const latestMsg = prospectMessages[0].textContent.trim();
                speak(latestMsg, currentGender);
            }
        }, 750);
    }

    return {
        playDoorbell,
        speak,
        startListening,
        stopListening,
        toggleListening,
        toggleHandsFree,
        toggleMute,
        onChatContentSwapped,
        ringAndStart
    };
})();
