import React, { useState, useEffect, useRef } from 'react';
import { emit_event } from '../telemetry';

export default function F1_Frequency({ onGameEnd, gameId }) {
    const [round, setRound] = useState(1);
    const [sliderVal, setSliderVal] = useState(50);
    const [cue, setCue] = useState(null);
    const roundTimerRef = useRef(null);
    const cueTimerRef = useRef(null);
    
    const rounds = [
        { id: 1, peak: 80, comfort: 40, text: "A bit sharp." },
        { id: 2, peak: 70, comfort: 70, text: "That's good here." },
        { id: 3, peak: 20, comfort: 60, text: "Hmm, it's a lot." }
    ];

    const currentRound = rounds[round - 1];

    useEffect(() => {
        if (!currentRound) return;
        
        emit_event(gameId, round.toString(), 'round_start', {}, { peak: currentRound.peak, comfort: currentRound.comfort });
        setSliderVal(50);
        setCue(null);
        
        cueTimerRef.current = setTimeout(() => {
            setCue(currentRound.text);
            emit_event(gameId, round.toString(), 'cue_shown', {}, { text: currentRound.text });
        }, 2000);
        
        roundTimerRef.current = setTimeout(() => {
            handleLockIn(sliderVal);
        }, 6000);
        
        return () => {
            clearTimeout(cueTimerRef.current);
            clearTimeout(roundTimerRef.current);
        };
    }, [round]);

    const handleLockIn = (val) => {
        clearTimeout(cueTimerRef.current);
        clearTimeout(roundTimerRef.current);
        emit_event(gameId, round.toString(), 'lock_in', {}, { x_final: val });
        emit_event(gameId, round.toString(), 'round_end', {}, {});
        if (round < 3) {
            setRound(r => r + 1);
        } else {
            onGameEnd();
        }
    };

    if (!currentRound) return null;

    return (
        <div style={{ textAlign: 'center', width: '300px' }}>
            <p>Tune the channel. A producer is listening.</p>
            <div style={{ height: '40px' }}>{cue && <strong>{cue}</strong>}</div>
            <input 
                type="range" min="0" max="100" value={sliderVal} 
                onChange={(e) => {
                    const val = parseInt(e.target.value, 10);
                    setSliderVal(val);
                    emit_event(gameId, round.toString(), 'slider_change', {}, { value: val });
                }} 
                style={{ width: '100%', margin: '20px 0' }}
            />
            <button onClick={() => handleLockIn(sliderVal)}>Lock in</button>
            <p>Round {round} of 3</p>
        </div>
    );
}
