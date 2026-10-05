let session_id = crypto.randomUUID();
let seq = 0;
let events_buffer = [];
let session_start = performance.now();

export function emit_event(game, trial, action, state, data) {
    const ev = {
        seq: seq++,
        t_ms: performance.now() - session_start,
        session_id: session_id,
        game: game,
        trial: trial,
        action: action,
        input_type: "mouse", // Simplifying to just mouse for this build, though touch/keyboard logic could be added
        state: state || {},
        data: data || {}
    };
    events_buffer.push(ev);
    
    // In-memory buffer size check, though the prompt says flush every 2.5s and on game end
    // For now, we will handle the interval in index.js or shell.js
}

export async function flush_events() {
    if (events_buffer.length === 0) return;
    
    const events_to_send = [...events_buffer];
    events_buffer = [];
    
    try {
        await fetch('http://localhost:8000/recruit/telemetry/events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ events: events_to_send })
        });
    } catch (e) {
        // Retry logic should be here, put back if failed
        events_buffer = [...events_to_send, ...events_buffer];
    }
}

// Set up 2.5s interval
setInterval(flush_events, 2500);
