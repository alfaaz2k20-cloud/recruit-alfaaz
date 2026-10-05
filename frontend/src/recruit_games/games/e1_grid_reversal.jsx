import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function E1_GridReversal({ onGameEnd, gameId }) {
    const [stimulus, setStimulus] = useState(null);
    const [feedback, setFeedback] = useState(null);
    const [trialCount, setTrialCount] = useState(0);
    const reversed = useRef(false);
    const trialTimerRef = useRef(null);
    const feedbackTimerRef = useRef(null);
    
    // We want ~10-14 stimuli in 24s. We can trigger a new one every 2s (total 12).
    useEffect(() => {
        if (trialCount >= 12) {
            onGameEnd();
            return;
        }
        
        if (trialCount === 6 && !reversed.current) {
            reversed.current = true;
            emit_event(gameId, trialCount.toString(), 'reversal_marker', {}, {});
        }
        
        const shape = Math.random() > 0.5 ? 'circle' : 'square';
        setStimulus(shape);
        setFeedback(null);
        emit_event(gameId, trialCount.toString(), 'stimulus_on', {}, { shape });
        
        trialTimerRef.current = setTimeout(() => {
            // Missed response
            handleResponse(null);
        }, 2000); // 2s per trial
        
        return () => {
            clearTimeout(trialTimerRef.current);
            clearTimeout(feedbackTimerRef.current);
        };
    }, [trialCount]);

    const handleResponse = (side) => {
        clearTimeout(trialTimerRef.current);
        
        const rt = 1000; // Simulated RT for now, could use performance.now()
        
        if (side) {
            emit_event(gameId, trialCount.toString(), 'response', {}, { side, rt });
            
            let correct = false;
            if (!reversed.current) {
                correct = (stimulus === 'circle' && side === 'left') || (stimulus === 'square' && side === 'right');
            } else {
                correct = (stimulus === 'circle' && side === 'right') || (stimulus === 'square' && side === 'left');
            }
            
            emit_event(gameId, trialCount.toString(), 'feedback', {}, { correct });
            setFeedback(correct ? '✓' : '✗');
        }
        
        setStimulus(null); // hide shape
        
        feedbackTimerRef.current = setTimeout(() => {
            setTrialCount(tc => tc + 1);
        }, 400); // 400ms feedback
    };

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
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
