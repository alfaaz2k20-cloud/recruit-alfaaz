import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function C2_CanvasCoordination({ onGameEnd, gameId }) {
    const [section, setSection] = useState(1);
    const [promptActive, setPromptActive] = useState(false);
    const promptTimerRef = useRef(null);
    
    useEffect(() => {
        if (section > 2) return;
        
        emit_event(gameId, section.toString(), 'section_start', {}, {});
        setPromptActive(false);
        
        // Partner pauses at unpredictable point (e.g. 4s)
        const pauseTimeout = setTimeout(() => {
            setPromptActive(true);
            emit_event(gameId, section.toString(), 'coord_prompt', {}, {});
            
            promptTimerRef.current = setTimeout(() => {
                // Auto dismiss
                if (promptActive) {
                    handleChoice('Keep painting');
                }
            }, 4000);
        }, 4000);
        
        const sectionTimeout = setTimeout(() => {
            emit_event(gameId, section.toString(), 'section_end', {}, {});
            if (section < 2) {
                setSection(s => s + 1);
            } else {
                onGameEnd();
            }
        }, 10000);
        
        return () => {
            clearTimeout(pauseTimeout);
            clearTimeout(promptTimerRef.current);
            clearTimeout(sectionTimeout);
        };
    }, [section]);

    const handleChoice = (choice) => {
        clearTimeout(promptTimerRef.current);
        setPromptActive(false);
        emit_event(gameId, section.toString(), 'coord_choice', {}, { choice });
    };

    if (section > 2) return null;

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
            <p>Paint your half. Coordinate with partner.</p>
            
            {promptActive ? (
                <div style={{ border: '1px solid red', padding: '10px', margin: '20px 0' }}>
                    <p>Partner paused...</p>
                    <button onClick={() => handleChoice('Wait')}>Wait</button>
                    <button onClick={() => handleChoice('Keep painting')}>Keep painting</button>
                    <button onClick={() => handleChoice('Signal')}>Send signal</button>
                </div>
            ) : (
                <div style={{ height: '100px', margin: '20px 0', border: '1px solid #ccc', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    Painting...
                </div>
            )}
        </div>
    );
}
