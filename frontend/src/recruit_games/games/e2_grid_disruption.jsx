import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function E2_GridDisruption({ onGameEnd, gameId }) {
    const [stimulus, setStimulus] = useState(null);
    const [feedback, setFeedback] = useState(null);
    const [stutter, setStutter] = useState(false);
    const [trialCount, setTrialCount] = useState(0);
    const trialTimerRef = useRef(null);
    const feedbackTimerRef = useRef(null);
    const lastInputs = useRef([]);
    const omissions = useRef(0);
    
    useEffect(() => {
        if (trialCount >= 10) {
            onGameEnd();
            return;
        }
        
        const shape = Math.random() > 0.5 ? 'circle' : 'square';
        setStimulus(shape);
        setFeedback(null);
        setStutter(false);
        emit_event(gameId, trialCount.toString(), 'stimulus_on', {}, { shape });
        
        trialTimerRef.current = setTimeout(() => {
            handleResponse(null); // Omission
        }, 2000);
        
        return () => {
            clearTimeout(trialTimerRef.current);
            clearTimeout(feedbackTimerRef.current);
        };
    }, [trialCount]);

    const handleResponse = (side) => {
        const now = performance.now();
        lastInputs.current.push(now);
        lastInputs.current = lastInputs.current.filter(t => now - t <= 1000);
        if (lastInputs.current.length >= 4) {
            emit_event(gameId, trialCount.toString(), 'burst', {}, {});
            lastInputs.current = []; // reset to prevent spamming
        }
        
        if (!side) {
            omissions.current += 1;
            if (omissions.current >= 2) {
                emit_event(gameId, trialCount.toString(), 'idle_gap', {}, {});
                omissions.current = 0;
            }
            setTrialCount(tc => tc + 1);
            return;
        }
        
        omissions.current = 0;
        clearTimeout(trialTimerRef.current);
        emit_event(gameId, trialCount.toString(), 'response', {}, { side, rt: 1000 });
        
        let correct = (stimulus === 'circle' && side === 'left') || (stimulus === 'square' && side === 'right');
        
        // Disruption logic: two glitches total (say at trial 3 and 7)
        let isGlitch = (trialCount === 3 || trialCount === 7);
        if (isGlitch) {
            emit_event(gameId, trialCount.toString(), 'glitch_marker', {}, {});
            correct = false; // unfair reject
            setStutter(true);
        }
        
        emit_event(gameId, trialCount.toString(), 'feedback', {}, { correct });
        setFeedback(correct ? '✓' : '✗');
        setStimulus(null);
        
        feedbackTimerRef.current = setTimeout(() => {
            setTrialCount(tc => tc + 1);
        }, 400); // 400ms stutter/feedback
    };

    return (
        <div style={{ textAlign: 'center', width: '300px', opacity: stutter ? 0.5 : 1 }}>
            <p>Sort shapes left or right.</p>
            
            <div style={{ height: '100px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '40px' }}>
                {feedback ? (
                    <span style={{ color: feedback === '✓' ? 'green' : 'red' }}>{feedback}</span>
                ) : (
                    stimulus === 'circle' ? '🟡' : (stimulus === 'square' ? '🟦' : '')
                )}
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0 20px' }}>
                <button onClick={() => handleResponse('left')} disabled={!!feedback}>Left</button>
                <button onClick={() => handleResponse('right')} disabled={!!feedback}>Right</button>
            </div>
        </div>
    );
}
